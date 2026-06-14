#!/usr/bin/env python3
"""migrate_jsonl_to_per_msg.py — T38 一次性 migrate：把 messages.jsonl + events.jsonl 拆成 per-msg 獨立檔.

新檔名約定（per Plan_Tavern_Per_Message_File_Refactor.md §2.3）：
    rooms/<room>/messages/<YYYY-MM-DD>/<HHMMSS>_<MMM>_<UUID6>.json
    rooms/<room>/events/<YYYY-MM-DD>/<HHMMSS>_<MMM>_<UUID6>__<event_type>.json

舊檔 backup 到：
    rooms/<room>/_backup/<UTC_TS>/messages.jsonl
    rooms/<room>/_backup/<UTC_TS>/events.jsonl
    rooms/<room>/_backup/<UTC_TS>/_seq.txt
    rooms/<room>/_backup/<UTC_TS>/_events_seq.txt
    rooms/<room>/_backup/<UTC_TS>/migrate_report.json

Usage:
    python AgentCommands/PromptQueue/migrate_jsonl_to_per_msg.py --room tavern --dry-run
    python AgentCommands/PromptQueue/migrate_jsonl_to_per_msg.py --all-rooms --dry-run
    python AgentCommands/PromptQueue/migrate_jsonl_to_per_msg.py --all-rooms --apply

Caveats:
    - reply_to 整數 seq 在新格式下會繼續存在但 deprecated（reply_to_uuid 是新 reference）
      — 本工具遷移時不轉 reply_to → reply_to_uuid（人工後處理或留 deprecated）
    - dedupe_report.*.json / messages.jsonl.bak.* 等舊 audit 檔留在 _backup 內
    - 不刪原 jsonl — apply 模式也只改名為 _backup/<ts>/messages.jsonl，方便回溯
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

# T36 _lib import
_HERE = Path(__file__).resolve().parent
_REPO_ROOT_FOR_LIB = _HERE.parent.parent
if str(_REPO_ROOT_FOR_LIB) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT_FOR_LIB))
from AgentCommands._lib import tavern_paths as _tp  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


WRITER_SIGNATURE_VALUE_V2 = "cmd_tavern_v2"   # bump from v1


def utc_now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def derive_uuid6(seed: str) -> str:
    """從 (seq, ts, sender_id) seed 算 deterministic 6-char hex uuid。"""
    h = hashlib.sha1(seed.encode("utf-8")).hexdigest()
    return h[:6]


def parse_record_ts(rec: dict) -> datetime | None:
    """讀 record 的 ts 欄位 → UTC datetime；失敗 / 缺欄回 None。"""
    ts = rec.get("ts")
    if not ts:
        return None
    try:
        # ISO 8601 — 容忍 trailing Z
        if ts.endswith("Z"):
            ts = ts[:-1] + "+00:00"
        return datetime.fromisoformat(ts).astimezone(timezone.utc)
    except Exception:
        return None


def build_message_filename(dt: datetime, uuid6: str) -> str:
    """<HHMMSS>_<MMM>_<UUID6>.json — 跟 C# UCL_ChatTavernIO_PerMsgFile.BuildMessageFileName 對齊."""
    return f"{dt:%H%M%S}_{dt:%f}"[:13] + f"_{uuid6}.json"


def build_event_filename(dt: datetime, uuid6: str, event_type: str) -> str:
    safe = (event_type or "event").replace("/", "_").replace("\\", "_")
    return f"{dt:%H%M%S}_{dt:%f}"[:13] + f"_{uuid6}__{safe}.json"


def serialize_message_no_seq(rec: dict) -> str:
    """寫 per-msg file 時不寫 seq；其他欄位保留 + 確保 _writer 簽章升 v2."""
    out = dict(rec)
    out.pop("seq", None)   # T38: seq 是 reader derive
    # 確保 uuid 欄位（caller 已填 deterministic uuid）
    # 確保 _writer 升 v2（標記 migrate 來源）
    meta = dict(out.get("meta") or {})
    meta["_writer"] = WRITER_SIGNATURE_VALUE_V2
    meta["_migrate_source"] = "jsonl_v1"
    out["meta"] = meta
    return json.dumps(out, ensure_ascii=False)


def serialize_event_no_seq(rec: dict) -> str:
    """events.jsonl 同樣不寫 seq."""
    out = dict(rec)
    out.pop("seq", None)
    return json.dumps(out, ensure_ascii=False)


def migrate_room(room_dir: Path, dry_run: bool, log) -> dict:
    """Migrate one room. Returns audit report."""
    msgs_path = room_dir / "messages.jsonl"
    events_path = room_dir / "events.jsonl"
    seq_path = room_dir / "_seq.txt"
    events_seq_path = room_dir / "_events_seq.txt"

    has_msgs = msgs_path.is_file()
    has_events = events_path.is_file()
    if not has_msgs and not has_events:
        log(f"  [skip] no messages.jsonl / events.jsonl in {room_dir.name}")
        return {"room": room_dir.name, "skipped": "nothing_to_migrate"}

    backup_dir = room_dir / "_backup" / utc_now_stamp()

    msgs_count_in = 0
    msgs_count_out = 0
    msgs_skipped_bad = 0
    events_count_in = 0
    events_count_out = 0
    events_skipped_bad = 0
    fname_collisions: list[str] = []

    # ---------------------- messages.jsonl ----------------------
    if has_msgs:
        records = []
        try:
            raw = msgs_path.read_bytes().decode("utf-8", errors="replace")
            for line_no, line in enumerate(raw.splitlines(), start=1):
                line = line.strip()
                if not line:
                    continue
                msgs_count_in += 1
                try:
                    rec = json.loads(line)
                    records.append((line_no, rec))
                except Exception as e:
                    msgs_skipped_bad += 1
                    log(f"  [warn] bad message line {line_no}: {str(e)[:80]}")
        except Exception as e:
            log(f"  [error] read {msgs_path} fail: {e}")
            return {"room": room_dir.name, "error": str(e)}

        log(f"  messages.jsonl: {msgs_count_in} records ({msgs_skipped_bad} bad lines)")

        # 寫每筆為單獨 file
        for line_no, rec in records:
            dt = parse_record_ts(rec)
            if dt is None:
                msgs_skipped_bad += 1
                log(f"  [warn] line {line_no} no parseable ts; skip")
                continue
            # uuid：用 record meta._writer / sender / seq / ts 算 deterministic
            seed = f"{rec.get('seq')}_{rec.get('sender_id')}_{rec.get('ts')}"
            uuid6 = derive_uuid6(seed)
            # 確保跟 C# generate 格式相容：6 hex chars
            # 若新 uuid 已有則 retry 加序號（罕見）
            rec["uuid"] = uuid6

            date_dir = room_dir / "messages" / dt.strftime("%Y-%m-%d")
            filename = build_message_filename(dt, uuid6)
            full_path = date_dir / filename

            # 防撞檔（同 ts + 同 uuid → 換 uuid retry）
            retry = 0
            while full_path.exists() and retry < 10:
                # 加 line_no salt 重 hash
                uuid6 = derive_uuid6(seed + f"_r{retry}")
                rec["uuid"] = uuid6
                filename = build_message_filename(dt, uuid6)
                full_path = date_dir / filename
                retry += 1
            if full_path.exists():
                fname_collisions.append(str(full_path))
                msgs_skipped_bad += 1
                continue

            if not dry_run:
                date_dir.mkdir(parents=True, exist_ok=True)
                full_path.write_text(serialize_message_no_seq(rec), encoding="utf-8")
            msgs_count_out += 1

        log(f"  messages migrated: {msgs_count_out}/{msgs_count_in}{' (DRY-RUN)' if dry_run else ''}")

    # ---------------------- events.jsonl ----------------------
    if has_events:
        records = []
        try:
            raw = events_path.read_bytes().decode("utf-8", errors="replace")
            for line_no, line in enumerate(raw.splitlines(), start=1):
                line = line.strip()
                if not line:
                    continue
                events_count_in += 1
                try:
                    rec = json.loads(line)
                    records.append((line_no, rec))
                except Exception as e:
                    events_skipped_bad += 1
                    log(f"  [warn] bad event line {line_no}: {str(e)[:80]}")
        except Exception as e:
            log(f"  [error] read {events_path} fail: {e}")
            return {"room": room_dir.name, "error": str(e)}

        log(f"  events.jsonl: {events_count_in} records ({events_skipped_bad} bad lines)")

        for line_no, rec in records:
            dt = parse_record_ts(rec)
            if dt is None:
                events_skipped_bad += 1
                continue
            seed = f"{rec.get('seq')}_{rec.get('actor')}_{rec.get('type')}_{rec.get('ts')}"
            uuid6 = derive_uuid6(seed)

            date_dir = room_dir / "events" / dt.strftime("%Y-%m-%d")
            filename = build_event_filename(dt, uuid6, rec.get("type", "event"))
            full_path = date_dir / filename

            retry = 0
            while full_path.exists() and retry < 10:
                uuid6 = derive_uuid6(seed + f"_r{retry}")
                filename = build_event_filename(dt, uuid6, rec.get("type", "event"))
                full_path = date_dir / filename
                retry += 1
            if full_path.exists():
                fname_collisions.append(str(full_path))
                events_skipped_bad += 1
                continue

            if not dry_run:
                date_dir.mkdir(parents=True, exist_ok=True)
                full_path.write_text(serialize_event_no_seq(rec), encoding="utf-8")
            events_count_out += 1

        log(f"  events migrated: {events_count_out}/{events_count_in}{' (DRY-RUN)' if dry_run else ''}")

    # ---------------------- backup 舊檔 ----------------------
    audit = {
        "room": room_dir.name,
        "timestamp_utc": utc_now_stamp(),
        "messages_in": msgs_count_in,
        "messages_out": msgs_count_out,
        "messages_skipped_bad": msgs_skipped_bad,
        "events_in": events_count_in,
        "events_out": events_count_out,
        "events_skipped_bad": events_skipped_bad,
        "filename_collisions": fname_collisions,
        "dry_run": dry_run,
    }

    if not dry_run:
        backup_dir.mkdir(parents=True, exist_ok=True)
        # 移舊 jsonl + counter 進 backup（保留可回溯）
        for src in [msgs_path, events_path, seq_path, events_seq_path]:
            if src.is_file():
                shutil.move(str(src), str(backup_dir / src.name))
                log(f"  ✓ backed up {src.name}")
        # 順手 backup 任何 messages.jsonl.bak.* / dedupe_report.* 殘留
        for fp in room_dir.glob("messages.jsonl.bak.*"):
            shutil.move(str(fp), str(backup_dir / fp.name))
            log(f"  ✓ backed up {fp.name}")
        for fp in room_dir.glob("dedupe_report.*.json"):
            shutil.move(str(fp), str(backup_dir / fp.name))
            log(f"  ✓ backed up {fp.name}")
        # 寫 audit report
        (backup_dir / "migrate_report.json").write_text(
            json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        log(f"  ✓ migrate_report → _backup/{backup_dir.name}/migrate_report.json")

    return audit


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--room", help="Specific room to migrate")
    parser.add_argument("--all-rooms", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)

    if not (args.room or args.all_rooms):
        parser.error("must specify --room <name> or --all-rooms")
    if args.dry_run and args.apply:
        parser.error("--dry-run and --apply are mutually exclusive")
    if not (args.dry_run or args.apply):
        parser.error("must specify --dry-run or --apply")

    rooms_dir = _tp.ROOMS_DIR
    if not rooms_dir.is_dir():
        print(f"[error] rooms dir not found: {rooms_dir}", file=sys.stderr)
        return 1

    if args.all_rooms:
        rooms = sorted(d for d in rooms_dir.iterdir() if d.is_dir())
    else:
        target = rooms_dir / args.room
        if not target.is_dir():
            print(f"[error] room not found: {target}", file=sys.stderr)
            return 1
        rooms = [target]

    overall = []
    for room_dir in rooms:
        print(f"\n=== room: {room_dir.name} ({'DRY-RUN' if args.dry_run else 'APPLY'}) ===")
        report = migrate_room(room_dir, dry_run=args.dry_run, log=print)
        overall.append(report)

    print(f"\n=== summary ({'DRY-RUN' if args.dry_run else 'APPLIED'}) ===")
    for r in overall:
        if r.get("skipped"):
            continue
        msgs = f"msg {r.get('messages_out')}/{r.get('messages_in')}"
        events = f"event {r.get('events_out')}/{r.get('events_in')}"
        bad = r.get('messages_skipped_bad', 0) + r.get('events_skipped_bad', 0)
        print(f"  {r['room']}: {msgs} | {events} | bad={bad}")

    if args.dry_run:
        print("\n→ rerun with --apply to migrate for real")
    return 0


if __name__ == "__main__":
    sys.exit(main())
