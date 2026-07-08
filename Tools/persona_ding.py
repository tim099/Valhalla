#!/usr/bin/env python3
"""
persona_ding.py — Persona ↔ Persona 自叮 (Self-Ding) CLI

職責: 同一 actor 不同 persona (e.g. basecamp / ridge-001) 之間的單次輕量 ping。
物理意義: 介於 letter (廣播) 跟 dialogue chain (深度 round-trip) 之間的中量機制。
        每筆 ding 寫進 personas/<to>/inbox.md, target persona 醒來必看必回。

對應 skill: ucl-persona-ding (跨 agent 通用)。

子命令:
  send --actor X --from A --to B --body "..." [--expects-reply true|false] [--session-context "..."] [--broadcast]
                                          發 ding (append 進 to-persona inbox)
  reply --actor X --persona P --ding-id ID --body "..." [--broadcast]
                                          回 ding (mark replied + append reply block)
  list --actor X --persona P [--unread-only]
                                          列某 persona 收到的所有 ding (audit)

範例:
  # basecamp 留 ding 給 ridge-001
  python persona_ding.py send --actor claude-da-xiaojie \\
    --from basecamp --to ridge-001 \\
    --body "妳的 thinking rule 真的緩解 reframe loop 嗎?" \\
    --expects-reply true --broadcast

  # ridge-001 醒來看 inbox
  python persona_ding.py list --actor claude-da-xiaojie --persona ridge-001 --unread-only

  # ridge-001 回 ding
  python persona_ding.py reply --actor claude-da-xiaojie --persona ridge-001 \\
    --ding-id a7f3c2 --body "確實緩解, 但 trade-off 是..."
"""

# 區塊職責: import + 路徑常量
# 物理意義: project-root 走 git rev-parse 反推, 確保跨工作目錄 invocation 都對
import argparse
import datetime
import os
import re
import secrets
import subprocess
import sys

# 區塊職責: Windows cp950 stdout fallback
# 物理意義: list 子命令用 emoji (🔔 / ✓), Windows console 預設 cp950 會炸 — 強制 UTF-8 stdout
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def _project_root() -> str:
    # 區塊職責: 反推 project root (git toplevel)
    # 物理意義: persona_ding 寫的 inbox.md 走絕對路徑, 不依賴 cwd
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return out
    except Exception:
        # fallback: 從本檔案位置反推 (Tools/ 上兩層 = project root)
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


PROJECT_ROOT = _project_root()
# T-PATH-02: run_cmd.py 走 layout-agnostic resolver, 不再寫死 CardGame/Assets/UCL/UCL_Core。
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from AgentCommands._lib import tavern_paths as _tp  # noqa: E402
CONSTITUTION_BASE = os.path.join(
    PROJECT_ROOT, "AgentCommands", "ChatTavern", "baton", "constitution"
)


def _persona_dir(actor: str, persona: str) -> str:
    """Persona overlay 目錄 (跟 ucl-self-constitution layout 對齊)。"""
    return os.path.join(CONSTITUTION_BASE, actor, "personas", persona)


def _inbox_path(actor: str, persona: str) -> str:
    return os.path.join(_persona_dir(actor, persona), "inbox.md")


def _utc_now_iso() -> str:
    # ISO 8601 UTC, 秒精度 (足夠 ding 排序)
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _gen_ding_id() -> str:
    # 6 字 hex (對齊 tavern message UUID6 慣例)
    return secrets.token_hex(3)


# 區塊職責: ding block 序列化
# 物理意義: 統一格式讓 list / reply 都能 parse, 不允許自由格式
def _format_ding_block(
    from_persona: str,
    to_persona: str,
    ding_id: str,
    ding_at: str,
    session_context: str,
    expects_reply: bool,
    body: str,
) -> str:
    # ding 格式: HTML comment marker + YAML frontmatter + body
    return (
        f"\n<!-- ding-{ding_id} -->\n"
        f"---\n"
        f"from_persona: {from_persona}\n"
        f"to_persona: {to_persona}\n"
        f"ding_id: {ding_id}\n"
        f"ding_at: {ding_at}\n"
        f"session_context: \"{session_context}\"\n"
        f"expects_reply: {'true' if expects_reply else 'false'}\n"
        f"replied: false\n"
        f"---\n\n"
        f"{body.strip()}\n\n"
        f"— {from_persona} @ {ding_at}\n\n"
        f"---\n"
    )


def _ensure_inbox(actor: str, persona: str) -> str:
    """確保 inbox.md 存在, 不存在則建 header 後 return path。"""
    inbox = _inbox_path(actor, persona)
    if not os.path.exists(inbox):
        os.makedirs(os.path.dirname(inbox), exist_ok=True)
        # 區塊職責: inbox 起始 header
        # 物理意義: 給未來醒來的 persona 看一眼即知檔案用途
        header = (
            f"# Persona Inbox: {persona}\n\n"
            f"> Self-ding 累積 — 來自 actor `{actor}` 內其他 persona 的單次 ping。\n"
            f"> 醒來時 cat 本檔, 看有沒有 unread ding (frontmatter `replied: false`)。\n"
            f"> 收到必回 (per ucl-persona-ding §收到自叮必回)。\n"
        )
        with open(inbox, "w", encoding="utf-8") as f:
            f.write(header)
    return inbox


# 區塊職責: send subcommand
# 物理意義: 把 ding append 進 target persona 的 inbox.md
def cmd_send(args: argparse.Namespace) -> int:
    actor = args.actor
    from_persona = getattr(args, "from")
    to_persona = args.to

    # Self-ding 不可 (沒意義 — 寫 letter 給自己用 letter)
    if from_persona == to_persona:
        print(f"[error] from == to ({from_persona}) — 自己叮自己沒意義, 改寫 letter。", file=sys.stderr)
        return 2

    # Target persona overlay 必須存在 (sanity check)
    target_overlay = os.path.join(_persona_dir(actor, to_persona), "_v1.md")
    if not os.path.exists(target_overlay):
        print(
            f"[warn] target persona overlay 不存在: {target_overlay}\n"
            f"        該 persona 尚未 spawn — 建議改寫 letter (ucl-letters-to-self) 給未來廣播。\n"
            f"        如確實要先 ping, 通過 --force 跳過。",
            file=sys.stderr,
        )
        if not args.force:
            return 3

    inbox = _ensure_inbox(actor, to_persona)
    ding_id = _gen_ding_id()
    ding_at = _utc_now_iso()
    block = _format_ding_block(
        from_persona=from_persona,
        to_persona=to_persona,
        ding_id=ding_id,
        ding_at=ding_at,
        session_context=args.session_context or "",
        expects_reply=args.expects_reply,
        body=args.body,
    )

    # Append (不覆寫)
    with open(inbox, "a", encoding="utf-8") as f:
        f.write(block)

    print(f"[ok] ding sent: {from_persona} → {to_persona}")
    print(f"     ding_id: {ding_id}")
    print(f"     ding_at: {ding_at}")
    print(f"     inbox:   {inbox}")

    if args.broadcast:
        _broadcast_ding(actor, from_persona, to_persona, ding_id, body=args.body[:120])

    return 0


# 區塊職責: reply subcommand
# 物理意義: 找對應 ding_id, mark replied + append reply block
def cmd_reply(args: argparse.Namespace) -> int:
    actor = args.actor
    persona = args.persona
    ding_id = args.ding_id

    inbox = _inbox_path(actor, persona)
    if not os.path.exists(inbox):
        print(f"[error] inbox 不存在: {inbox}", file=sys.stderr)
        return 4

    with open(inbox, "r", encoding="utf-8") as f:
        content = f.read()

    # 找 ding marker
    marker = f"<!-- ding-{ding_id} -->"
    if marker not in content:
        print(f"[error] ding_id `{ding_id}` 找不到於 {inbox}", file=sys.stderr)
        return 5

    # 區塊職責: 在該 ding 區塊裡把 replied: false → true
    # 數值影響: 只改第一個出現的, 因 ding_id 唯一
    block_start = content.index(marker)
    # 找下一個 ding marker 或檔尾, 限定 replied 欄位的 scope
    next_marker_search = content.find("<!-- ding-", block_start + len(marker))
    block_end = next_marker_search if next_marker_search != -1 else len(content)
    block_chunk = content[block_start:block_end]

    if "replied: false" not in block_chunk:
        print(f"[warn] ding `{ding_id}` 已 replied 過 (replied != false)。改 reply 還是繼續?", file=sys.stderr)
        if not args.force:
            return 6

    new_chunk = block_chunk.replace("replied: false", "replied: true", 1)

    # 在區塊結尾 (下一個 marker 或 EOF) 前 append reply block
    reply_at = _utc_now_iso()
    reply_block = (
        f"\n### reply by {persona} @ {reply_at}\n\n"
        f"{args.body.strip()}\n\n"
        f"— {persona} @ {reply_at}\n\n"
    )

    # 找 chunk 內最後一個 `---\n` (ding block 收尾) 之前插入 reply_block
    # 因 ding format 結尾固定 "\n---\n"
    last_sep_idx = new_chunk.rfind("\n---\n")
    if last_sep_idx == -1:
        # 萬一格式破壞, 純 append 到 chunk 尾
        new_chunk = new_chunk + reply_block
    else:
        # 插在最後 separator 之前
        new_chunk = new_chunk[:last_sep_idx] + "\n" + reply_block + new_chunk[last_sep_idx:]

    new_content = content[:block_start] + new_chunk + content[block_end:]
    with open(inbox, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"[ok] ding {ding_id} replied by {persona}")
    print(f"     reply_at: {reply_at}")

    if args.broadcast:
        _broadcast_ding_reply(actor, persona, ding_id, body=args.body[:120])

    return 0


# 區塊職責: list subcommand
# 物理意義: parse inbox.md 列所有 ding (或只 unread)
def cmd_list(args: argparse.Namespace) -> int:
    actor = args.actor
    persona = args.persona
    inbox = _inbox_path(actor, persona)

    if not os.path.exists(inbox):
        print(f"[info] inbox 不存在 (還沒收過 ding): {inbox}")
        return 0

    with open(inbox, "r", encoding="utf-8") as f:
        content = f.read()

    # 區塊職責: 用 regex 撈每個 ding block 的 frontmatter
    # 數值影響: 只 parse frontmatter 欄位, body 不展開 (避免 list 太長)
    pattern = re.compile(
        r"<!-- ding-(?P<id>[a-f0-9]+) -->\s*\n---\n(?P<fm>.*?)\n---\n",
        re.DOTALL,
    )
    matches = list(pattern.finditer(content))

    if not matches:
        print(f"[info] {inbox} 沒任何 ding")
        return 0

    print(f"# Persona Inbox: {actor}/{persona}")
    print(f"# Total dings: {len(matches)}\n")

    shown = 0
    for m in matches:
        fm = m.group("fm")
        ding_id = m.group("id")
        # 簡易 fm parser
        fm_dict = {}
        for line in fm.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm_dict[k.strip()] = v.strip().strip('"')

        replied = fm_dict.get("replied", "?") == "true"
        if args.unread_only and replied:
            continue

        status_icon = "✓" if replied else "🔔"
        print(
            f"{status_icon} {ding_id} | {fm_dict.get('from_persona', '?')} → {fm_dict.get('to_persona', '?')} "
            f"| {fm_dict.get('ding_at', '?')} | replied={replied}"
        )
        ctx = fm_dict.get("session_context", "")
        if ctx:
            print(f"   context: {ctx}")
        shown += 1

    print(f"\nShown: {shown} / Total: {len(matches)}")
    return 0


# 區塊職責: tavern broadcast (optional)
# 物理意義: 跟 ucl-chat-tavern 整合, 發一筆 meta-tagged post 廣播事件
def _broadcast_ding(actor: str, from_persona: str, to_persona: str, ding_id: str, body: str) -> None:
    msg = (
        f"[persona-ding] {from_persona} → {to_persona} (ding_id: {ding_id})\n\n"
        f"{body}{'...' if len(body) >= 120 else ''}\n\n"
        f"(完整內容於 personas/{to_persona}/inbox.md, 等該 persona 醒來必回)"
    )
    _tavern_post(
        sender=actor,
        persona=from_persona,
        body=msg,
        meta=f"tag:self-ding;to-persona:{to_persona};ding-id:{ding_id}",
    )


def _broadcast_ding_reply(actor: str, persona: str, ding_id: str, body: str) -> None:
    msg = (
        f"[persona-ding-reply] {persona} 回了 ding {ding_id}\n\n"
        f"{body}{'...' if len(body) >= 120 else ''}\n\n"
        f"(完整內容於 personas/{persona}/inbox.md)"
    )
    _tavern_post(
        sender=actor,
        persona=persona,
        body=msg,
        meta=f"tag:self-ding-reply;ding-id:{ding_id}",
    )


def _tavern_post(sender: str, persona: str, body: str, meta: str) -> None:
    # 區塊職責: 走 唯一合法 path (Cmd_Tavern), 不直寫訊息檔
    # 物理意義: 對齊 ucl-chat-tavern P0 鐵律, 守 UUID6 + UTF-8 + presence 七道機制
    # Phase 1 (Tim 2026-05-11): persona 走 first-class --arg persona, 不再塞 meta:from-persona
    run_cmd = str(_tp.RUN_CMD_PATH)
    cmd_args = [
        sys.executable, run_cmd,
        "run", "Tavern",
        "--arg", "op=post",
        "--arg", "room=tavern",
        "--arg", f"sender={sender}",
    ]
    if persona:
        cmd_args.extend(["--arg", f"persona={persona}"])
    cmd_args.extend([
        "--arg", f"body={body}",
        "--arg", f"meta={meta}",
        "--arg", "wait-reply=0",
    ])
    try:
        subprocess.check_call(cmd_args)
    except subprocess.CalledProcessError as e:
        print(f"[warn] tavern broadcast 失敗 (rc={e.returncode}) — ding 主檔已寫成功, 廣播是 best-effort", file=sys.stderr)


# 區塊職責: argparse setup
# 物理意義: subcommand dispatch
def main() -> int:
    parser = argparse.ArgumentParser(
        prog="persona_ding.py",
        description="Persona ↔ Persona 自叮 (Self-Ding) CLI — append/reply/list dings 於 personas/<persona>/inbox.md",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # send
    p_send = sub.add_parser("send", help="發 ding 給另一 persona")
    p_send.add_argument("--actor", required=True, help="actor id (e.g. claude-da-xiaojie)")
    p_send.add_argument("--from", dest="from", required=True, help="發送方 persona codename (e.g. basecamp)")
    p_send.add_argument("--to", required=True, help="接收方 persona codename (e.g. ridge-001)")
    p_send.add_argument("--body", required=True, help="ding 內文 (建議 < 300 字)")
    p_send.add_argument("--expects-reply", type=lambda x: x.lower() == "true", default=True,
                        help="是否要求回覆 (true|false, 預設 true)")
    p_send.add_argument("--session-context", default="", help="本 ding 的 session 主軸一句")
    p_send.add_argument("--broadcast", action="store_true", help="同時 tavern post 一筆廣播 meta:tag:self-ding")
    p_send.add_argument("--force", action="store_true", help="即使 target persona overlay 不存在也送")
    p_send.set_defaults(func=cmd_send)

    # reply
    p_reply = sub.add_parser("reply", help="回 ding (mark replied + append reply block)")
    p_reply.add_argument("--actor", required=True)
    p_reply.add_argument("--persona", required=True, help="回覆方 persona (= ding 的 to_persona)")
    p_reply.add_argument("--ding-id", required=True, help="6-char hex ding_id")
    p_reply.add_argument("--body", required=True)
    p_reply.add_argument("--broadcast", action="store_true")
    p_reply.add_argument("--force", action="store_true", help="即使 already replied 也再 append 新 reply")
    p_reply.set_defaults(func=cmd_reply)

    # list
    p_list = sub.add_parser("list", help="列某 persona inbox 內所有 ding")
    p_list.add_argument("--actor", required=True)
    p_list.add_argument("--persona", required=True)
    p_list.add_argument("--unread-only", action="store_true", help="只列 replied: false 的 ding")
    p_list.set_defaults(func=cmd_list)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
