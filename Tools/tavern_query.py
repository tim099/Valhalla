#!/usr/bin/env python3
"""
T56 tavern_query.py — Read-only Tavern message query tool

職責：純檢視酒館訊息（不發訊息），支援 DB-like 查詢介面。
物理意義：直讀 AgentCommands/ChatTavern/rooms/<room>/messages/<date>/*.json filesystem，
        不依賴 Editor / Cmd queue，Editor offline 時也能用。

子命令：
  rooms                     列所有房間 + 最後活動時間（預設 24h 內）
  tail <room> [--limit N]   印某房最後 N 則訊息（預設 20）
  search <keyword> [...]    跨房關鍵字檢索
  by-sender <sender_id>     某 sender 的所有訊息
  timeline [--limit N]      跨房時序流（最新 N 則）
  stats [--since 24h]       訊息數統計（per room / per sender）
  seq [N] [--range A-B] [...]  依 seq / 範圍 / 篩選條件撈（seq 與 op=read 的 [seq N] 一致）

範例：
  python tavern_query.py rooms
  python tavern_query.py tail tavern --limit 10
  python tavern_query.py search "HP" --room tavern --since 24h
  python tavern_query.py by-sender claude-da-xiaojie --limit 5
  python tavern_query.py timeline --limit 30
  python tavern_query.py stats --since 24h
  python tavern_query.py seq 8363
  python tavern_query.py seq --range 8362-8364
  python tavern_query.py seq --range 8000-8366 --persona calli --grep 驗證 --full
  python tavern_query.py seq --last 5 --json
"""

import argparse
import datetime
import glob
import json
import os
import re
import sys
from typing import Iterator

# 區塊職責：強制 stdout/stderr 用 UTF-8（Windows cp950 預設無法 encode emoji / 中文 fullwidth）
# 物理意義：跨 platform 一致顯示效果；Linux/macOS 預設已 utf-8 不影響
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

# 路徑常數：相對 EOV repo root
TAVERN_ROOT = "AgentCommands/ChatTavern/rooms"
IDENTITIES_PATH = "AgentCommands/ChatTavern/identities.json"


def parse_since(s: str) -> datetime.timedelta:
    """解析 --since 參數：'24h' / '30m' / '7d' / '1w'。預設 24h。"""
    if not s:
        return datetime.timedelta(hours=24)
    m = re.match(r"^(\d+)([hmdw])$", s.lower())
    if not m:
        raise ValueError(f"無法解析 --since: {s}（格式範例: 24h / 30m / 7d / 1w）")
    n = int(m.group(1))
    unit = m.group(2)
    return {
        "h": datetime.timedelta(hours=n),
        "m": datetime.timedelta(minutes=n),
        "d": datetime.timedelta(days=n),
        "w": datetime.timedelta(weeks=n),
    }[unit]


def utcnow() -> datetime.datetime:
    """區塊職責：取得當前 UTC 時間（含 tzinfo）"""
    return datetime.datetime.now(datetime.timezone.utc)


def parse_ts(ts: str) -> datetime.datetime:
    """區塊職責：解析 ISO8601 ts 字串成 aware datetime"""
    # 支援尾隨 Z（UTC marker）
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    return datetime.datetime.fromisoformat(ts)


def list_rooms() -> list[str]:
    """區塊職責：列出 rooms 子目錄"""
    if not os.path.isdir(TAVERN_ROOT):
        return []
    return sorted(d for d in os.listdir(TAVERN_ROOT)
                  if os.path.isdir(os.path.join(TAVERN_ROOT, d)))


def iter_room_messages(room: str, since: datetime.datetime = None) -> Iterator[dict]:
    """
    區塊職責：generator 走某房的所有 message 檔，可選 since filter
    物理意義：T38 per-message file architecture，按檔名排序近似 ts 排序
    """
    msg_root = os.path.join(TAVERN_ROOT, room, "messages")
    if not os.path.isdir(msg_root):
        return
    # 列所有日期目錄按字典序（=按日期序）
    for date_dir in sorted(os.listdir(msg_root)):
        date_path = os.path.join(msg_root, date_dir)
        if not os.path.isdir(date_path):
            continue
        for fname in sorted(os.listdir(date_path)):
            if not fname.endswith(".json"):
                continue
            fpath = os.path.join(date_path, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    msg = json.load(f)
            except (json.JSONDecodeError, OSError):
                continue
            msg["_room"] = room
            msg["_filename"] = fname
            if since:
                try:
                    msg_ts = parse_ts(msg.get("ts", ""))
                    if msg_ts < since:
                        continue
                except (ValueError, TypeError):
                    continue
            yield msg


def load_identities() -> dict:
    """區塊職責：載 identities.json 用作 sender_id → display_name 解析"""
    try:
        with open(IDENTITIES_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {p["id"]: p.get("display_name", p["id"])
                for p in data.get("identities", [])}
    except (OSError, json.JSONDecodeError, KeyError):
        return {}


def resolve_sender_id(sid: str, identities: dict) -> str:
    """
    區塊職責：從 sender_id string 解析 display name (msg-less version 給 stats 用)
    物理意義：先查 identities.json；'-alter' suffix 自動 strip + ' (Alter)' suffix
    """
    if sid in identities:
        return identities[sid]
    if sid.endswith("-alter"):
        base_id = sid[:-len("-alter")]
        if base_id in identities:
            return f"{identities[base_id]} (Alter)"
    return sid


def resolve_sender(msg: dict, identities: dict) -> str:
    """
    區塊職責：從 msg dict 解析 display name
    物理意義：先用 resolve_sender_id；fallback msg sender_name 或 raw sender_id
    """
    sid = msg.get("sender_id", "?")
    resolved = resolve_sender_id(sid, identities)
    if resolved != sid:
        return resolved
    return msg.get("sender_name") or sid


def format_ts_local(ts_iso: str) -> str:
    """區塊職責：把 UTC ts 轉本地時區顯示"""
    try:
        dt_utc = parse_ts(ts_iso)
        dt_local = dt_utc.astimezone()
        return dt_local.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        return ts_iso


def truncate(s: str, n: int = 80) -> str:
    """區塊職責：截斷長字串，replace newlines with space"""
    if not s:
        return ""
    s = s.replace("\n", " ").replace("\r", "")
    if len(s) <= n:
        return s
    return s[:n - 1] + "…"


# ─────────────────────────── op handlers ───────────────────────────

def op_rooms(args):
    """
    印所有 room 的最後活動時間（24h 預設窗）。
    顯示：room / 最新 ts (本地) / 最新 sender / body 預覽
    格式照活動新→舊排序。
    """
    since_delta = parse_since(args.since)
    since = utcnow() - since_delta
    identities = load_identities()
    rooms = list_rooms()

    summary = []
    for room in rooms:
        last_msg = None
        msg_count = 0
        for msg in iter_room_messages(room, since):
            last_msg = msg
            msg_count += 1
        if last_msg:
            summary.append({
                "room": room,
                "last_ts": last_msg.get("ts", ""),
                "last_sender": resolve_sender(last_msg, identities),
                "last_body": truncate(last_msg.get("body", ""), 60),
                "count_window": msg_count,
            })

    # 排序：最新的在前
    summary.sort(key=lambda x: x["last_ts"], reverse=True)

    if not summary:
        print(f"⚠ 沒有房間在最近 {args.since} 內有活動")
        return

    print(f"# 🏨 Tavern Rooms — last {args.since} activity")
    print(f"# 共 {len(summary)} 個活躍房 / 總 {len(rooms)} 房\n")
    print(f"{'Room':<28} {'Last Active':<20} {'#msgs':>6}  Last Sender / Body")
    print("─" * 110)
    for s in summary:
        print(f"{s['room']:<28} {format_ts_local(s['last_ts']):<20} {s['count_window']:>6}  "
              f"{s['last_sender'][:14]:<14} | {s['last_body']}")


def op_tail(args):
    """印某房最後 N 則訊息"""
    identities = load_identities()
    if args.room not in list_rooms():
        print(f"❌ Room not found: {args.room}", file=sys.stderr)
        sys.exit(2)

    msgs = list(iter_room_messages(args.room))
    if not msgs:
        print(f"⚠ Room {args.room} 沒有訊息")
        return

    tail = msgs[-args.limit:] if args.limit > 0 else msgs

    print(f"# 📜 {args.room} — last {len(tail)} messages\n")
    for i, msg in enumerate(tail, start=len(msgs) - len(tail) + 1):
        sender = resolve_sender(msg, identities)
        ts_local = format_ts_local(msg.get("ts", ""))
        body = truncate(msg.get("body", ""), 200)
        meta = msg.get("meta") or {}
        meta_str = ""
        if meta:
            tag = meta.get("tag", "")
            cat = meta.get("category", "")
            if tag or cat:
                meta_str = f" [{','.join(x for x in [tag, cat] if x)}]"
        print(f"#{i} [{ts_local}] {sender}{meta_str}")
        print(f"  {body}\n")


def op_search(args):
    """跨房 / 單房關鍵字檢索"""
    identities = load_identities()
    pattern = args.keyword
    case_sensitive = args.case_sensitive
    if not case_sensitive:
        pattern_re = re.compile(re.escape(pattern), re.IGNORECASE)
    else:
        pattern_re = re.compile(re.escape(pattern))

    since = None
    if args.since:
        since = utcnow() - parse_since(args.since)

    rooms_to_search = [args.room] if args.room else list_rooms()
    hits = []
    for room in rooms_to_search:
        for msg in iter_room_messages(room, since):
            body = msg.get("body", "")
            if pattern_re.search(body):
                hits.append(msg)

    hits.sort(key=lambda m: m.get("ts", ""), reverse=True)
    hits = hits[:args.limit] if args.limit > 0 else hits

    print(f"# 🔍 Search '{pattern}'  (rooms={','.join(rooms_to_search)}, since={args.since or 'all'})")
    print(f"# 共 {len(hits)} hits\n")
    for msg in hits:
        sender = resolve_sender(msg, identities)
        ts_local = format_ts_local(msg.get("ts", ""))
        body = truncate(msg.get("body", ""), 150)
        print(f"[{ts_local}] {msg['_room']} / {sender}")
        # highlight match (terminal ANSI bold)
        highlighted = pattern_re.sub(lambda m: f"\033[1;33m{m.group(0)}\033[0m", body)
        print(f"  {highlighted}\n")


def op_by_sender(args):
    """印某 sender 的訊息"""
    identities = load_identities()
    since = None
    if args.since:
        since = utcnow() - parse_since(args.since)

    hits = []
    for room in list_rooms():
        for msg in iter_room_messages(room, since):
            if msg.get("sender_id") == args.sender_id:
                hits.append(msg)

    hits.sort(key=lambda m: m.get("ts", ""), reverse=True)
    hits = hits[:args.limit] if args.limit > 0 else hits

    if not hits:
        print(f"⚠ Sender {args.sender_id} 沒有訊息（since {args.since or 'all'}）")
        return

    sender_name = identities.get(args.sender_id, args.sender_id)
    print(f"# 👤 {sender_name} ({args.sender_id}) — last {len(hits)} messages")
    print(f"# since={args.since or 'all'}\n")
    for msg in hits:
        ts_local = format_ts_local(msg.get("ts", ""))
        body = truncate(msg.get("body", ""), 150)
        print(f"[{ts_local}] {msg['_room']}")
        print(f"  {body}\n")


def op_timeline(args):
    """跨房時序流（最新 N 則 across all rooms）"""
    identities = load_identities()
    since = None
    if args.since:
        since = utcnow() - parse_since(args.since)

    all_msgs = []
    for room in list_rooms():
        for msg in iter_room_messages(room, since):
            all_msgs.append(msg)

    all_msgs.sort(key=lambda m: m.get("ts", ""), reverse=True)
    tail = all_msgs[:args.limit] if args.limit > 0 else all_msgs

    print(f"# ⏱ Timeline (latest {len(tail)} across {len(list_rooms())} rooms, since={args.since or 'all'})\n")
    for msg in tail:
        sender = resolve_sender(msg, identities)
        ts_local = format_ts_local(msg.get("ts", ""))
        body = truncate(msg.get("body", ""), 100)
        print(f"[{ts_local}] {msg['_room']:<26} / {sender[:12]:<12} | {body}")


def op_stats(args):
    """訊息數統計：per room / per sender"""
    identities = load_identities()
    since = None
    if args.since:
        since = utcnow() - parse_since(args.since)

    by_room = {}
    by_sender = {}
    total = 0
    for room in list_rooms():
        room_count = 0
        for msg in iter_room_messages(room, since):
            sid = msg.get("sender_id", "?")
            by_sender[sid] = by_sender.get(sid, 0) + 1
            room_count += 1
            total += 1
        if room_count > 0:
            by_room[room] = room_count

    print(f"# 📊 Stats — since {args.since or 'all'}, total {total} messages\n")
    print("## By Room")
    for room, n in sorted(by_room.items(), key=lambda x: -x[1]):
        bar = "█" * min(40, n)
        print(f"  {room:<28} {n:>5}  {bar}")
    print("\n## By Sender")
    for sid, n in sorted(by_sender.items(), key=lambda x: -x[1]):
        name = resolve_sender_id(sid, identities)
        bar = "█" * min(40, n)
        print(f"  {name[:24]:<24} ({sid[:24]:<24}) {n:>5}  {bar}")


# 區塊職責：解析 --range "A-B" / "A:B" → (lo, hi)，端點自動排序
def _parse_range(s: str):
    sep = "-" if "-" in s else (":" if ":" in s else None)
    if not sep:
        raise argparse.ArgumentTypeError("range 格式需為 A-B 或 A:B")
    a, b = s.split(sep, 1)
    lo, hi = int(a), int(b)
    return (min(lo, hi), max(lo, hi))


def op_seq(args):
    """
    區塊職責：依 seq / seq 範圍 / 篩選條件撈訊息。
    物理意義：seq 是「渲染層流水號」、不存在訊息檔裡，是讀取時按『檔名字典序位置』derive。
            本命令**複用 _lib/tavern_io.read_messages**（C# UCL_ChatTavernIO_PerMsgFile.LoadAllMessages
            的 python mirror）取 seq，保證跟 op=read / catchup 的 [seq N] 同一套編號。
            → 不自己另排序（本檔其他子命令用的 iter_room_messages 順序近似但非 canonical；seq 查詢必須用 tavern_io）。
    數值影響：純讀取；多條件 = AND；seq 為位置流水號(可隨增刪漂移)，要穩定引用一筆請看輸出的 {uuid}。
    """
    # lazy import：只有 seq 子命令需要 _lib；path 用「本檔上兩層=AgentCommands」直接定位，
    # 不走 .git walk-up（那正是 2026-06-16 catchup 撞 submodule gitlink 靜默失效的禍根）
    _agentcmd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _agentcmd not in sys.path:
        sys.path.insert(0, _agentcmd)
    from _lib import tavern_io

    identities = load_identities()
    msgs = tavern_io.read_messages(args.room)
    if not msgs:
        print(f"⚠ Room {args.room} 讀不到訊息", file=sys.stderr)
        sys.exit(2)

    # 區塊：套用 selectors + 篩選（皆 AND）
    out = msgs
    if args.seq is not None:
        out = [m for m in out if m.get("seq") == args.seq]
    if args.range:
        lo, hi = args.range
        out = [m for m in out if lo <= m.get("seq", -1) <= hi]
    if args.persona:
        out = [m for m in out if (m.get("sender_persona") or "") == args.persona]
    if args.sender:
        out = [m for m in out if args.sender in (m.get("sender_id") or "")]
    if args.tag:
        out = [m for m in out if args.tag in ((m.get("meta") or {}).get("tag") or "")]
    if args.grep:
        rx = re.compile(args.grep, re.IGNORECASE)
        out = [m for m in out if rx.search(m.get("body") or "")]
    if args.last is not None:
        out = out[-args.last:]

    # 區塊：輸出
    if args.json:
        rows = []
        for m in out:
            rows.append({
                "seq": m.get("seq"), "ts": m.get("ts"), "uuid": m.get("uuid"),
                "sender_id": m.get("sender_id"), "sender_persona": m.get("sender_persona"),
                "tag": (m.get("meta") or {}).get("tag"), "body": m.get("body"),
            })
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return

    print(f"# 🔢 seq query (room={args.room}, 全量 {len(msgs)} 筆, 命中 {len(out)} 筆)\n")
    if not out:
        print("（無命中）")
        return
    for m in out:
        sender = resolve_sender(m, identities)
        ts_local = format_ts_local(m.get("ts", ""))
        tag = (m.get("meta") or {}).get("tag") or ""
        uuid = m.get("uuid", "")
        head = f"[seq {m.get('seq')}] [{ts_local}] {sender}"
        if tag:
            head += f"  «{tag}»"
        if uuid:
            head += f"  {{{uuid}}}"
        body = m.get("body", "") or ""
        print(head)
        print(f"  {body if args.full else truncate(body, 200)}\n")


# ─────────────────────────── main ───────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="T56 Tavern Query — read-only message viewer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="op", required=True)

    p_rooms = sub.add_parser("rooms", help="列所有房間 + 最後活動時間")
    p_rooms.add_argument("--since", default="24h", help="時間窗口，預設 24h")
    p_rooms.set_defaults(func=op_rooms)

    p_tail = sub.add_parser("tail", help="印某房最後 N 則訊息")
    p_tail.add_argument("room", help="房間 id")
    p_tail.add_argument("--limit", type=int, default=20, help="訊息數，預設 20，0=全部")
    p_tail.set_defaults(func=op_tail)

    p_search = sub.add_parser("search", help="關鍵字檢索")
    p_search.add_argument("keyword", help="搜尋關鍵字")
    p_search.add_argument("--room", help="限定單房")
    p_search.add_argument("--since", help="時間窗口（如 24h / 7d）")
    p_search.add_argument("--case-sensitive", action="store_true", help="大小寫敏感")
    p_search.add_argument("--limit", type=int, default=30, help="結果上限，預設 30")
    p_search.set_defaults(func=op_search)

    p_sender = sub.add_parser("by-sender", help="某 sender 的訊息")
    p_sender.add_argument("sender_id", help="sender_id")
    p_sender.add_argument("--since", help="時間窗口")
    p_sender.add_argument("--limit", type=int, default=20, help="訊息數，預設 20")
    p_sender.set_defaults(func=op_by_sender)

    p_timeline = sub.add_parser("timeline", help="跨房時序流")
    p_timeline.add_argument("--since", default="24h", help="時間窗口，預設 24h")
    p_timeline.add_argument("--limit", type=int, default=30, help="訊息數，預設 30")
    p_timeline.set_defaults(func=op_timeline)

    p_stats = sub.add_parser("stats", help="訊息數統計")
    p_stats.add_argument("--since", default="24h", help="時間窗口，預設 24h")
    p_stats.set_defaults(func=op_stats)

    p_seq = sub.add_parser("seq", help="依 seq/範圍/篩選撈訊息（canonical seq, 對齊 op=read）")
    p_seq.add_argument("seq", nargs="?", type=int, help="單一 seq（位置參數；省略則改用 --range/--last）")
    p_seq.add_argument("--range", type=_parse_range, help="seq 範圍 A-B（含端點）")
    p_seq.add_argument("--last", type=int, help="篩選後取最後 N 筆（最新）")
    p_seq.add_argument("--room", default="tavern", help="房間，預設 tavern")
    p_seq.add_argument("--persona", help="篩 sender_persona（精確）")
    p_seq.add_argument("--sender", help="篩 sender_id（substring）")
    p_seq.add_argument("--tag", help="篩 meta.tag（substring）")
    p_seq.add_argument("--grep", help="篩 body（regex, 不分大小寫）")
    p_seq.add_argument("--full", action="store_true", help="印完整 body（預設截斷 200）")
    p_seq.add_argument("--json", action="store_true", help="JSON 輸出（含 uuid/seq/ts）")
    p_seq.set_defaults(func=op_seq)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
