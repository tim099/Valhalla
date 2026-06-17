#!/usr/bin/env python3
"""
workflow_notes.py — Workflow 眉批層 CLI (2026-06-17, Tim 10-token task; design 經 summit 拍磚加固)

職責: 對某個 workflow 留「使用時踩坑 / tip / 前置提醒」的眉批，**不直接改 workflow 本體**；
      之後讀 workflow 前用 `show` 把眉批浮現出來。

與 workflow_patch.py 的分工 (刻意平行雙層，共用 slug resolver):
  - note  (本檔)  = 使用者眉批 —— workflow 沒錯，只是使用踩坑。無上限、不需 QA 確認、越常駐越值錢。
  - patch (那檔)  = 確認 bug 的修補 —— 假設 workflow 是錯的。3-cap 逼 refactor、終要 fold 回 workflow。
  一條 note 若反覆出現、確認是 workflow 真缺陷 → 可升級成 patch（共用 slug 即 cross-link）。

設計重心 (summit 加固):
  - slug ≠ 檔名: slug 是「顯式穩定身份」，當主鍵 / 目錄名；workflow 檔 rename 不動 slug。
  - target = 可解析位置 (檔案路徑 OR skill:<name>#<section>)，記在 slug index；rename 只重指 target。
  - doctor: 掃所有 slug 的 target 解不解析得到，斷鏈標出 → 防 silent 孤兒 (registry drift 被接住)。
  - show 帶 invocation 計數: 用數據驗證「一行 pointer convention」死活，不是用信心 (N 週 0 read = 該砍)。

子命令:
  add  --workflow <slug> --kind <pitfall|tip|precondition|gotcha> --note "<踩坑一句>"
       --by <agent_id> [--target <path|skill:...>] [--context "<什麼情境會撞>"]
       [--howto "<該怎麼做>"] [--why "<為何>"]
  show --workflow <slug>            列該 slug 的 active 眉批 (讀 workflow 前跑這個) + 累計 show 計數
  list-all                          跨 slug 掃: 眉批數 / show 次數 / target 健康
  fold --workflow <slug> --id <N>   標某條 note 已 fold 進 workflow 本體 (status=folded, 不刪留 audit)
  doctor                            掃所有 slug 的 target 解析狀態, 斷鏈標 BROKEN

storage: docs/Workflows/_notes/<slug>/  ( _index.json + NNN_<short>.md )
"""

import argparse
import datetime
import json
import os
import sys

# Windows console UTF-8 fallback
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# 區塊職責：載入共用層 — repo_root（路徑錨）+ workflow_slug（slug 正規化 / target 解析）
# 物理意義：summit 拍板「共用的是 slug resolver 本身，不只 repo_root」——patch 跟 note 走同一份，
#          否則兩邊認的「同一 workflow」不一致 = 又一個層次混淆。故 normalize_slug / resolve_target
#          一律從 _lib 取，本檔不自己再寫一份。
# 數值影響：純 import。
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _lib.repo_root import find_repo_root  # noqa: E402
from _lib.workflow_slug import normalize_slug, resolve_target  # noqa: E402

PROJECT_ROOT = find_repo_root()
WORKFLOWS_DIR = os.path.join(PROJECT_ROOT, "docs", "Workflows")
NOTES_ROOT = os.path.join(WORKFLOWS_DIR, "_notes")

VALID_KINDS = ("pitfall", "tip", "precondition", "gotcha")


def _notes_dir(slug: str) -> str:
    return os.path.join(NOTES_ROOT, slug)


def _index_path(slug: str) -> str:
    return os.path.join(_notes_dir(slug), "_index.json")


def _utc_now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# 區塊職責：讀 / 存某 slug 的 index（無上限、append-only；跟 patch 的 3-cap 哲學刻意相反）
# 物理意義：note 越常駐越值錢，故無 count 上限；show_invocations 為浮現 convention 的存活度量。
# 數值影響：JSON 讀寫。
def _load_index(slug: str) -> dict:
    p = _index_path(slug)
    if not os.path.exists(p):
        return {
            "workflow_slug": slug,
            "target": None,
            "note_count": 0,
            "show_invocations": 0,
            "last_shown_at": None,
            "notes": [],
        }
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def _save_index(slug: str, idx: dict) -> None:
    os.makedirs(_notes_dir(slug), exist_ok=True)
    with open(_index_path(slug), "w", encoding="utf-8") as f:
        json.dump(idx, f, indent=2, ensure_ascii=False)


# ---------------- add ----------------
# 區塊職責：register 一條眉批 —— 寫 NNN_<short>.md + 累加 index entry（無上限）
# 物理意義：把「使用 workflow 時踩的坑 / tip」沉澱成資料，下次讀 workflow 用 show 浮現。
#          target 設在 slug 層（同一 workflow 所有 note 共用一個位置），rename 只需 add --target 重指。
# 數值影響：寫 1 個 .md + 更新 _index.json。
def cmd_add(args):
    slug = normalize_slug(args.workflow)
    if args.kind not in VALID_KINDS:
        print(f"❌ kind 須為 {VALID_KINDS} 其一，收到 '{args.kind}'", file=sys.stderr)
        return 2

    idx = _load_index(slug)
    # target: 首次 add 帶入 / 之後 add --target 可重指（rename workflow 時用）
    if args.target:
        idx["target"] = args.target.strip()

    note_id = idx["note_count"] + 1
    short = normalize_slug(args.note[:40])
    filename = f"{note_id:03d}_{short}.md"
    os.makedirs(_notes_dir(slug), exist_ok=True)

    ts = _utc_now()
    body = (
        f"---\n"
        f"note_id: {note_id:03d}\n"
        f"workflow_slug: {slug}\n"
        f"target: {idx.get('target') or '(unset)'}\n"
        f"kind: {args.kind}\n"
        f"trigger_context: {json.dumps(args.context or '', ensure_ascii=False)}\n"
        f"added_by: {args.by}\n"
        f"added_at: {ts}\n"
        f"status: active\n"
        f"---\n\n"
        f"# {args.kind.upper()}: {args.note}\n\n"
        f"**踩坑 / 提醒**：{args.note}\n\n"
        f"**該怎麼做**：{args.howto or '_(待補)_'}\n\n"
        f"**為何**：{args.why or '_(待補)_'}\n"
    )
    if args.context:
        body += f"\n**觸發情境**：{args.context}\n"
    with open(os.path.join(_notes_dir(slug), filename), "w", encoding="utf-8") as f:
        f.write(body)

    idx["note_count"] = note_id
    idx["notes"].append({
        "id": note_id,
        "filename": filename,
        "kind": args.kind,
        "trigger_context": args.context or "",
        "added_by": args.by,
        "added_at": ts,
        "status": "active",
        "summary": args.note,
    })
    _save_index(slug, idx)

    print(f"[ok] note {note_id:03d} added → workflow `{slug}` ({args.kind})")
    print(f"     path: docs/Workflows/_notes/{slug}/{filename}")
    print(f"     target: {idx.get('target') or '(unset — 建議 add --target 指明 workflow 位置, doctor 才查得到)'}")
    if idx.get("target"):
        ok, _, _, reason = resolve_target(idx["target"], PROJECT_ROOT)
        print(f"     target check: {'✅' if ok else '⚠ BROKEN'} {reason}")
    return 0


# ---------------- show ----------------
# 區塊職責：浮現某 slug 的 active 眉批（讀 workflow 前跑）+ 累加 show invocation 計數（instrument convention）
# 物理意義：這是整個機制的 read-time 觸點 —— 「一行 pointer → 跑 show」的落地。
#          show_invocations 量「pointer convention 有沒有人真的用」：N 週後仍 0 read = convention 死了該砍，
#          用數據答而非信心（summit 加固點）。
# 數值影響：讀全部 note + 更新 _index.json 的 show_invocations / last_shown_at（讀亦寫，刻意為之）。
def cmd_show(args):
    slug = normalize_slug(args.workflow)
    p = _index_path(slug)
    if not os.path.exists(p):
        print(f"📝 workflow `{slug}` 無眉批 (no notes)。")
        return 0
    idx = _load_index(slug)

    # instrument: 累加 show 計數（除非 --no-count，給自動化/測試用）
    if not args.no_count:
        idx["show_invocations"] = idx.get("show_invocations", 0) + 1
        idx["last_shown_at"] = _utc_now()
        _save_index(slug, idx)

    active = [n for n in idx["notes"] if n.get("status") == "active"]
    print(f"# 📝 Workflow 眉批 — `{slug}`  (active {len(active)} / total {idx['note_count']}; shown {idx.get('show_invocations', 0)}x)")
    if idx.get("target"):
        ok, _, _, reason = resolve_target(idx["target"], PROJECT_ROOT)
        print(f"- target: {idx['target']}  {'✅' if ok else '⚠ BROKEN — 跑 doctor'}")
    print()
    if not active:
        print("_(無 active 眉批)_")
        return 0
    for n in active:
        ctx = f" — 情境: {n['trigger_context']}" if n.get("trigger_context") else ""
        print(f"## [{n['kind']}] {n['summary']}{ctx}")
        print(f"   ↳ 詳: docs/Workflows/_notes/{slug}/{n['filename']}  (by {n['added_by']} @ {n['added_at']})")
    return 0


# ---------------- list-all ----------------
# 區塊職責：跨所有 slug 掃 — 眉批數 / show 次數 / target 健康，一覽
# 物理意義：給維護者看「哪些 workflow 累積眉批、哪些 pointer 沒人用（show=0）、哪些 target 斷了」。
# 數值影響：純讀。
def cmd_list_all(args):
    if not os.path.exists(NOTES_ROOT):
        print("_(尚無 _notes 目錄)_")
        return 0
    rows = []
    for slug in sorted(os.listdir(NOTES_ROOT)):
        if not os.path.isdir(_notes_dir(slug)):
            continue
        idx = _load_index(slug)
        active = sum(1 for n in idx["notes"] if n.get("status") == "active")
        tgt_ok = "—"
        if idx.get("target"):
            ok, _, _, _ = resolve_target(idx["target"], PROJECT_ROOT)
            tgt_ok = "✅" if ok else "⚠ BROKEN"
        rows.append((slug, active, idx["note_count"], idx.get("show_invocations", 0), tgt_ok))
    if not rows:
        print("_(尚無任何 workflow 眉批)_")
        return 0
    print("# Workflow 眉批總覽")
    print()
    print("| Workflow slug | Active/Total | Shown | Target |")
    print("|---|---|---|---|")
    for slug, act, total, shown, tgt in rows:
        flag = "  ← 0 read (convention 可能沒人用)" if shown == 0 else ""
        print(f"| `{slug}` | {act}/{total} | {shown}x{flag} | {tgt} |")
    return 0


# ---------------- fold ----------------
# 區塊職責：把某條 note 標為已 fold 進 workflow 本體（status=folded-into-workflow, 不刪留 audit）
# 物理意義：眉批被正式收進 workflow / 升級成 patch 後，標記但保留歷史（同 patch archive 不刪原則）。
# 數值影響：改 _index.json 對應 note 的 status + 同步該 .md frontmatter。
def cmd_fold(args):
    slug = normalize_slug(args.workflow)
    idx = _load_index(slug)
    hit = next((n for n in idx["notes"] if n["id"] == args.id), None)
    if not hit:
        print(f"❌ workflow `{slug}` 無 note id={args.id}", file=sys.stderr)
        return 2
    hit["status"] = "folded-into-workflow"
    hit["folded_at"] = _utc_now()
    _save_index(slug, idx)
    # 同步 .md frontmatter 的 status（best-effort）
    mp = os.path.join(_notes_dir(slug), hit["filename"])
    if os.path.exists(mp):
        with open(mp, encoding="utf-8") as f:
            txt = f.read()
        txt = txt.replace("status: active", "status: folded-into-workflow", 1)
        with open(mp, "w", encoding="utf-8") as f:
            f.write(txt)
    print(f"[ok] note {args.id:03d} of `{slug}` → folded-into-workflow (保留 audit, 未刪)")
    return 0


# ---------------- doctor ----------------
# 區塊職責：掃所有 slug 的 target 解析狀態，斷鏈標 BROKEN（防 silent 孤兒）
# 物理意義：slug 是穩定身份、target 是會變位置；workflow rename/move/拆檔後 target 會斷，
#          但 slug 還在 → note 變孤兒沒人發現。doctor 主動掃出來逼人重指 target（summit 加固）。
# 數值影響：純讀；回非零 exit code 當 broken 數 > 0（給 CI/hook 用）。
def cmd_doctor(args):
    if not os.path.exists(NOTES_ROOT):
        print("_(尚無 _notes 目錄, nothing to check)_")
        return 0
    broken = []
    unset = []
    checked = 0
    for slug in sorted(os.listdir(NOTES_ROOT)):
        if not os.path.isdir(_notes_dir(slug)):
            continue
        idx = _load_index(slug)
        checked += 1
        tgt = idx.get("target")
        if not tgt:
            unset.append(slug)
            continue
        ok, _, _, reason = resolve_target(tgt, PROJECT_ROOT)
        if not ok:
            broken.append((slug, tgt, reason))
    print(f"# 🩺 workflow_notes doctor — 掃 {checked} 個 slug")
    print()
    if not broken and not unset:
        print("✅ 全部 target 解析正常，無孤兒。")
        return 0
    if broken:
        print(f"## ⚠ BROKEN target ({len(broken)}) — workflow 可能被 rename/move, 重指 target:")
        for slug, tgt, reason in broken:
            print(f"- `{slug}`  target=`{tgt}`  → {reason}")
            print(f"    修: python AgentCommands/Tools/workflow_notes.py add --workflow {slug} --target <新位置> ...（或手動改 _index.json target）")
        print()
    if unset:
        print(f"## ℹ target 未設 ({len(unset)}) — doctor 無從檢查, 建議補:")
        for slug in unset:
            print(f"- `{slug}`")
    return 1 if broken else 0


def main():
    parser = argparse.ArgumentParser(
        prog="workflow_notes.py",
        description="Workflow 眉批層 CLI — add / show / list-all / fold / doctor (不改 workflow 本體)",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="register 一條眉批")
    p_add.add_argument("--workflow", required=True, help="穩定 slug (顯式命名, 非檔名)")
    p_add.add_argument("--kind", required=True, help=f"{VALID_KINDS}")
    p_add.add_argument("--note", required=True, help="踩坑 / 提醒一句 (filename 用)")
    p_add.add_argument("--by", required=True, help="agent / persona id")
    p_add.add_argument("--target", default=None, help="workflow 位置: repo 相對路徑 OR skill:<name>#<section>")
    p_add.add_argument("--context", default=None, help="什麼情境會撞到")
    p_add.add_argument("--howto", default=None, help="該怎麼做")
    p_add.add_argument("--why", default=None, help="為何")
    p_add.set_defaults(func=cmd_add)

    p_show = sub.add_parser("show", help="浮現 slug 的 active 眉批 (讀 workflow 前跑) + 計數")
    p_show.add_argument("--workflow", required=True)
    p_show.add_argument("--no-count", action="store_true", help="不累加 show 計數 (自動化/測試用)")
    p_show.set_defaults(func=cmd_show)

    p_la = sub.add_parser("list-all", help="跨 slug 總覽")
    p_la.set_defaults(func=cmd_list_all)

    p_fold = sub.add_parser("fold", help="標某 note 已 fold 進 workflow (不刪)")
    p_fold.add_argument("--workflow", required=True)
    p_fold.add_argument("--id", required=True, type=int)
    p_fold.set_defaults(func=cmd_fold)

    p_doc = sub.add_parser("doctor", help="掃 target 解析狀態, 斷鏈標 BROKEN")
    p_doc.set_defaults(func=cmd_doctor)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
