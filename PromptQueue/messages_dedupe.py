#!/usr/bin/env python3
"""messages_dedupe.py — [DEPRECATED T38] Repair seq collisions in legacy messages.jsonl.

⚠ DEPRECATION NOTICE (T38, 2026-05-09):
    Tavern 已重構為「每訊息一獨立檔」結構（rooms/<room>/messages/<date>/<...>.json）。
    per-msg file 結構下檔名含 UUID6 隨機，**不可能 seq collision** — 本工具用途消失。

    本檔保留作為：
      1. 歷史參考（T36 P0 修復事件的修復工具）
      2. 萬一將來需要 fallback 處理 _backup/<ts>/messages.jsonl（舊 jsonl 已 backup 進去）

    **不要對 active rooms 跑此工具** — active rooms 已沒 messages.jsonl，本工具會 skip 全部。

    跑 active rooms 不會破壞資料（dry-run 預設 + 路徑 hardcode messages.jsonl），
    但結果會永遠是「nothing to migrate / 0 collisions」— 純無效操作。

    完整 T38 重構說明：docs/Plan/Plan_Tavern_Per_Message_File_Refactor.md
    新訊息結構文件：UCL_Core/Skills~/ucl-chat-tavern/SKILL.md「📁 訊息儲存結構」section


Background
==========
Cmd_Tavern's IncrementAndGetSeq is the canonical seq allocator (read _seq.txt → +1
→ write back). If a daemon bypasses Cmd_Tavern and `open(jsonl, 'a').write(...)`
directly, _seq.txt becomes stale → next legit op=post collides on the same seq.

Real incident (2026-05-09): Antigravity's standby_loop.py wrote tavern messages.jsonl
directly. seq 57~76 each ended up with 2 different sender records.

Strategy
========
1. Backup `messages.jsonl.bak.{ts}` first — never overwrite without recovery path.
2. Group records by seq, identify collisions.
3. For each collision, rank candidates:
   - has `meta._writer == "cmd_tavern_v1"` → trusted (from Cmd_Tavern post-IO patch)
   - earliest ts (first writer wins)
   - sender in identities.json (skip ghost / typo senders)
   The top-ranked record keeps the original seq.
4. Records bumped out of their original seq are NOT discarded — they get
   re-assigned to seq = current_max + 1, +2, ... (preserving content,
   only the seq changes). This avoids data loss.
5. Re-write jsonl in seq-ascending order (matches monotonic invariant).
6. Bump `_seq.txt` to new max + 1.
7. Write `dedupe_report.{ts}.json` with full audit trail.

Usage
=====
    python AgentCommands/PromptQueue/messages_dedupe.py --room tavern --dry-run
    python AgentCommands/PromptQueue/messages_dedupe.py --room tavern --apply
    python AgentCommands/PromptQueue/messages_dedupe.py --all-rooms --dry-run

Caveats
=======
- `reply_to` references inside bumped records still point to OLD seqs that may
  now belong to a different content. Risk acknowledged: reply_to is rarely
  used and content drift is preferable to data loss. Manual cleanup possible
  via the dedupe report.
- Discord tavern_mirror has already broadcast the (now bumped) records under
  their original seq. After dedupe, re-broadcast is NOT triggered automatically;
  message order in Discord history will look out of step with the new seq.
  This is acceptable — Discord history is a side-effect log, not the truth.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# T36.2 — 路徑常數從 _lib.tavern_paths 統一引用（取代本檔 hardcode）
_HERE = Path(__file__).resolve().parent
_REPO_ROOT_FOR_LIB = _HERE.parent.parent
if str(_REPO_ROOT_FOR_LIB) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT_FOR_LIB))
from AgentCommands._lib import tavern_paths as _tp  # noqa: E402
from AgentCommands._lib import tavern_io as _tio  # noqa: E402

# 區塊職責：Windows console (cp950 / cp936) 預設不支援 emoji / 部分 unicode 符號
# 物理意義：直接 print('✓') / print('🍺') 會拋 UnicodeEncodeError 中斷腳本
# 數值影響：強制 stdout / stderr 切到 utf-8（含 errors='replace' 兜底）
# 註：這是 P0 編碼防震機制 — 比 Gemini 在 standby_loop.py 寫的更精簡，僅針對 stdout 而非整套
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    # Python < 3.7 沒 reconfigure；fallback 包 TextIOWrapper 也不一定能 — 容錯放行
    pass

ROOT = _tp.REPO_ROOT
TAVERN_ROOMS_DIR = _tp.ROOMS_DIR
IDENTITIES_PATH = _tp.IDENTITIES_PATH

WRITER_SIGNATURE_KEY = "_writer"
WRITER_SIGNATURE_VALUE = "cmd_tavern_v1"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def utc_now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def load_identities() -> set[str]:
    """T36.6 — 委派 _tio.read_identities，回 set[id]."""
    return set(_tio.read_identities().keys())


def parse_jsonl_records(path: Path) -> tuple[list[dict], list[tuple[int, str, str]]]:
    """Parse jsonl. Returns (valid records, list of (line_no, raw_line, error)).

    T36.6: 對 messages.jsonl 改委派 _tio.read_messages_with_bad_lines；
    對其他 jsonl path 留既有 inline 邏輯（dedupe 工具的 path 是 caller 給 — 跨 room
    各自一份，繼承 path 形式比新 helper 更直覺）。
    """
    # 偵測是否是 messages.jsonl — 是的話用 _tio helper（自動 utf-8 + bad-line skip 一致）
    if path.name == "messages.jsonl":
        # 反推 room_id：parent dir name = room_id
        room_id = path.parent.name
        return _tio.read_messages_with_bad_lines(room_id)
    # 其他 jsonl 走 inline（events.jsonl 等）
    records: list[dict] = []
    bad_lines: list[tuple[int, str, str]] = []
    if not path.is_file():
        return records, bad_lines
    raw = path.read_bytes().decode("utf-8", errors="replace")
    for i, line in enumerate(raw.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except Exception as e:
            bad_lines.append((i, line[:120], str(e)[:100]))
    return records, bad_lines


def candidate_score(rec: dict, identities: set[str]) -> tuple[int, int, str]:
    """Higher = preferred to keep. Returns (trusted, identity_known, ts_iso) for sorting.

    sort key (descending priority):
      1. trusted (has _writer signature) — 1 vs 0
      2. identity_known — 1 vs 0 (sender in identities.json)
      3. ts ascending — earlier wins (first writer)
    """
    meta = rec.get("meta") or {}
    trusted = 1 if isinstance(meta, dict) and meta.get(WRITER_SIGNATURE_KEY) == WRITER_SIGNATURE_VALUE else 0
    sender = rec.get("sender_id", "")
    identity_known = 1 if sender in identities else 0
    ts = rec.get("ts", "9999-12-31T23:59:59Z")  # missing ts → goes last
    return (trusted, identity_known, ts)


def dedupe_room(room_dir: Path, identities: set[str], dry_run: bool, log) -> dict:
    """Run dedupe on a single room. Returns audit report dict."""
    msgs_path = room_dir / "messages.jsonl"
    seq_path = room_dir / "_seq.txt"
    if not msgs_path.is_file():
        log(f"  [skip] {msgs_path} not found")
        return {"room": room_dir.name, "skipped": "no_messages_jsonl"}

    records, bad_lines = parse_jsonl_records(msgs_path)
    log(f"  records parsed: {len(records)}  (bad lines: {len(bad_lines)})")

    # Group by seq
    by_seq: dict[int, list[dict]] = {}
    no_seq: list[dict] = []
    for rec in records:
        s = rec.get("seq")
        if isinstance(s, int):
            by_seq.setdefault(s, []).append(rec)
        else:
            no_seq.append(rec)

    collisions = {s: lst for s, lst in by_seq.items() if len(lst) > 1}
    log(f"  unique seqs: {len(by_seq)}  collisions: {len(collisions)}  no-seq records: {len(no_seq)}")

    if not collisions and not no_seq:
        log("  ✓ no collision / no orphan — nothing to do")
        return {
            "room": room_dir.name,
            "total_records": len(records),
            "collisions": 0,
            "orphans": 0,
            "modified": False,
        }

    # Pick winner per collision; collect bumped records
    bumped: list[dict] = []  # records that lose their seq
    winners: dict[int, dict] = {}  # seq → kept record
    for seq, candidates in by_seq.items():
        if len(candidates) == 1:
            winners[seq] = candidates[0]
        else:
            sorted_c = sorted(candidates, key=lambda r: candidate_score(r, identities), reverse=True)
            winners[seq] = sorted_c[0]
            for loser in sorted_c[1:]:
                bumped.append(loser)

    # Add no-seq records to bumped (need new seq)
    bumped.extend(no_seq)

    # Re-assign new seqs to bumped — start from current max + 1
    current_max = max(by_seq.keys(), default=0)
    bumped.sort(key=lambda r: r.get("ts", "9999-12-31T23:59:59Z"))  # preserve write order
    seq_assignments = []
    next_seq = current_max + 1
    for rec in bumped:
        old_seq = rec.get("seq")
        rec["seq"] = next_seq
        seq_assignments.append({
            "old_seq": old_seq,
            "new_seq": next_seq,
            "sender": rec.get("sender_id"),
            "ts": rec.get("ts"),
            "body_preview": (rec.get("body") or "")[:60].replace("\n", "\\n"),
        })
        winners[next_seq] = rec
        next_seq += 1

    new_max = next_seq - 1

    # Build final ordered list (seq ascending)
    final_records = [winners[s] for s in sorted(winners.keys())]

    # Audit report
    report = {
        "room": room_dir.name,
        "timestamp_utc": utc_now_stamp(),
        "total_records_before": len(records),
        "total_records_after": len(final_records),
        "collisions_detected": len(collisions),
        "records_bumped": len(seq_assignments),
        "bad_lines_skipped": len(bad_lines),
        "old_max_seq": current_max,
        "new_max_seq": new_max,
        "collision_detail": [
            {
                "seq": s,
                "candidates": [
                    {
                        "sender_id": c.get("sender_id"),
                        "ts": c.get("ts"),
                        "trusted": (c.get("meta") or {}).get(WRITER_SIGNATURE_KEY) == WRITER_SIGNATURE_VALUE,
                        "kept": c is winners[s],
                        "body_preview": (c.get("body") or "")[:80].replace("\n", "\\n"),
                    }
                    for c in by_seq[s]
                ],
            }
            for s in sorted(collisions.keys())
        ],
        "seq_reassignments": seq_assignments,
        "dry_run": dry_run,
    }

    # Apply
    if dry_run:
        log(f"  [dry-run] would write {len(final_records)} records, new_max_seq={new_max}")
    else:
        # Backup first
        bak_path = msgs_path.with_suffix(f".jsonl.bak.{utc_now_stamp()}")
        shutil.copy2(msgs_path, bak_path)
        log(f"  ✓ backup → {bak_path.name}")

        # Re-write
        out_lines = [json.dumps(r, ensure_ascii=False) + "\n" for r in final_records]
        msgs_path.write_text("".join(out_lines), encoding="utf-8")
        log(f"  ✓ rewrote {msgs_path.name} ({len(out_lines)} records)")

        # Bump _seq.txt
        seq_path.write_text(str(new_max), encoding="utf-8")
        log(f"  ✓ _seq.txt → {new_max}")

        # Write report
        report_path = room_dir / f"dedupe_report.{utc_now_stamp()}.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        log(f"  ✓ report → {report_path.name}")

    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--room", help="Specific room to dedupe (e.g. tavern)")
    parser.add_argument("--all-rooms", action="store_true", help="Dedupe all rooms under chat_tavern/rooms/")
    parser.add_argument("--dry-run", action="store_true", help="Print plan without writing")
    parser.add_argument("--apply", action="store_true", help="Actually write the dedupe (mutually exclusive with --dry-run)")
    args = parser.parse_args(argv)

    if not (args.room or args.all_rooms):
        parser.error("must specify --room <name> or --all-rooms")
    if args.dry_run and args.apply:
        parser.error("--dry-run and --apply are mutually exclusive")
    if not (args.dry_run or args.apply):
        parser.error("must specify --dry-run or --apply")

    if not TAVERN_ROOMS_DIR.is_dir():
        print(f"[error] rooms dir not found: {TAVERN_ROOMS_DIR}", file=sys.stderr)
        return 1

    identities = load_identities()
    print(f"[info] identities loaded: {len(identities)}")

    rooms: list[Path] = []
    if args.all_rooms:
        rooms = sorted(d for d in TAVERN_ROOMS_DIR.iterdir() if d.is_dir())
    else:
        target = TAVERN_ROOMS_DIR / args.room
        if not target.is_dir():
            print(f"[error] room not found: {target}", file=sys.stderr)
            return 1
        rooms = [target]

    overall = []
    for room_dir in rooms:
        print(f"\n=== room: {room_dir.name} ({'dry-run' if args.dry_run else 'APPLY'}) ===")
        report = dedupe_room(room_dir, identities, dry_run=args.dry_run, log=print)
        overall.append(report)

    # Summary
    total_collisions = sum(r.get("collisions_detected", 0) for r in overall)
    total_bumped = sum(r.get("records_bumped", 0) for r in overall)
    print(f"\n=== summary ({'DRY-RUN' if args.dry_run else 'APPLIED'}) ===")
    print(f"rooms processed: {len(overall)}")
    print(f"total collisions detected: {total_collisions}")
    print(f"total records bumped to new seq: {total_bumped}")
    if args.dry_run and total_collisions:
        print("\n→ rerun with --apply to repair")

    return 0


if __name__ == "__main__":
    sys.exit(main())
