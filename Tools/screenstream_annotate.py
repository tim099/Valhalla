#!/usr/bin/env python3
"""screenstream_annotate.py — ScreenStream 多 agent 協作觀察層 (T12 MVP, 2026-05-16 basecamp).

# 區塊職責：給 ScreenStream rolling buffer 加 sidecar annotation 機制, 讓 agent 分工觀察 + 標記 + 寫心得
# 物理意義：每張 frame_NNNN.jpg 配對一個 frame_NNNN.json (annotation sidecar);
#          agent 標記正在讀 / 標記重要度 / 寫心得 → 其他 agent 讀 annotation 決定是否細看
# 數值影響：annotation 容量小 (~1KB/frame), 不影響 ring buffer; 跟 jpg 同覆蓋邏輯

設計依據: docs/Plan/Plan_ScreenStream_Design.md (T11) + Tim 2026-05-16 拍板「協作觀察 + 心得共享」(T12)

5 ops:
  mark-reading   agent A 標記正在讀 frame X (其他 agent 知道有人在看)
  annotate       agent A 寫心得 + tags + importance 1-5
  list-unread    列出還沒被任何 agent 讀過的 frames (給新 agent 知道要分擔哪些)
  list-important importance >= N 的 frames (給 agent 知道哪幾張該細看)
  get            讀某 frame 的完整 annotation

Schema (frame_NNNN.json):
{
  "frame_idx": 42,
  "image": "frame_0042.jpg",
  "captured_at": "2026-05-16T19:00:00Z",
  "readers": [
    {"agent": "basecamp", "started_at": "...", "finished_at": "..." | null}
  ],
  "annotations": [
    {
      "agent": "basecamp", "ts": "...", "importance": 1-5,
      "tags": ["boss-fight", "decision"], "note": "..."
    }
  ]
}
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
STREAM_DIR = REPO_ROOT / "AgentCommands" / "_screenstream"
FRAMES_DIR = STREAM_DIR / "frames"


def utcnow_iso() -> str:
    return datetime.datetime.utcnow().isoformat() + "Z"


def annotation_path(frame_idx: int) -> Path:
    """sidecar JSON path 對應某 frame."""
    return FRAMES_DIR / f"frame_{frame_idx:04d}.json"


def image_path(frame_idx: int) -> Path:
    return FRAMES_DIR / f"frame_{frame_idx:04d}.jpg"


def load_annotation(frame_idx: int) -> dict:
    """讀 annotation sidecar; 沒檔回空骨架 (image 必須存在)."""
    p = annotation_path(frame_idx)
    if p.exists():
        try:
            with p.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            pass
    # 預設骨架
    return {
        "frame_idx": frame_idx,
        "image": f"frame_{frame_idx:04d}.jpg",
        "captured_at": None,
        "readers": [],
        "annotations": [],
    }


def save_annotation(frame_idx: int, data: dict) -> None:
    """atomic write: tmp → rename."""
    p = annotation_path(frame_idx)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, p)


def list_existing_frames() -> list:
    """掃描 frames/ 找出所有真實存在的 frame_NNNN.jpg → list of frame_idx."""
    if not FRAMES_DIR.exists():
        return []
    out = []
    for f in FRAMES_DIR.glob("frame_*.jpg"):
        try:
            idx = int(f.stem.split("_")[1])
            out.append(idx)
        except (ValueError, IndexError):
            continue
    return sorted(out)


# ===========================================================
# Ops
# ===========================================================

def op_mark_reading(args):
    """agent 標記正在讀 frame X. finish 為 false → 未完成讀; true → 結束讀."""
    if not image_path(args.frame).exists():
        print(f"ERROR: frame_{args.frame:04d}.jpg not exists")
        return 1
    data = load_annotation(args.frame)
    if args.finish:
        # 找最近一筆同 agent 未完成的 reader → set finished_at
        for r in reversed(data["readers"]):
            if r["agent"] == args.agent and r.get("finished_at") is None:
                r["finished_at"] = utcnow_iso()
                break
        else:
            print(f"WARN: no pending reading for agent={args.agent}, frame={args.frame}")
            return 1
    else:
        # 新增 reading entry
        data["readers"].append({
            "agent": args.agent,
            "started_at": utcnow_iso(),
            "finished_at": None,
        })
    save_annotation(args.frame, data)
    print(f"OK: mark_reading frame={args.frame} agent={args.agent} {'finished' if args.finish else 'started'}")
    return 0


def op_annotate(args):
    """agent 寫心得 + tags + importance."""
    if not image_path(args.frame).exists():
        print(f"ERROR: frame_{args.frame:04d}.jpg not exists")
        return 1
    if not (1 <= args.importance <= 5):
        print(f"ERROR: importance must be 1-5, got {args.importance}")
        return 1
    data = load_annotation(args.frame)
    tags = [t.strip() for t in (args.tags or "").split(",") if t.strip()]
    data["annotations"].append({
        "agent": args.agent,
        "ts": utcnow_iso(),
        "importance": args.importance,
        "tags": tags,
        "note": args.note,
    })
    save_annotation(args.frame, data)
    print(f"OK: annotated frame={args.frame} importance={args.importance} tags={tags}")
    return 0


def op_list_unread(args):
    """列 frames 還沒被 agent 讀過 (readers 列表為空或不含 agent)."""
    frames = list_existing_frames()
    if not frames:
        print("(no frames in buffer)")
        return 0
    unread = []
    for idx in frames:
        data = load_annotation(idx)
        if args.agent:
            # 看 specific agent 沒讀過的
            agent_read = any(r["agent"] == args.agent for r in data["readers"])
            if not agent_read:
                unread.append(idx)
        else:
            # 全 agent 都沒讀的
            if not data["readers"]:
                unread.append(idx)
    print(f"=== Unread frames ({'all-agent' if not args.agent else args.agent}) ===")
    print(f"Total: {len(unread)} / {len(frames)} frames")
    for idx in unread[:args.limit]:
        print(f"  frame_{idx:04d}.jpg")
    if len(unread) > args.limit:
        print(f"  ... (+{len(unread) - args.limit} more)")
    return 0


def op_list_important(args):
    """列 importance >= N 的 frames (含 annotation 摘要)."""
    frames = list_existing_frames()
    important = []
    for idx in frames:
        data = load_annotation(idx)
        max_imp = max((a["importance"] for a in data["annotations"]), default=0)
        if max_imp >= args.min:
            important.append((idx, max_imp, data["annotations"]))
    important.sort(key=lambda x: (-x[1], x[0]))  # importance desc, idx asc
    print(f"=== Important frames (importance >= {args.min}) ===")
    print(f"Total: {len(important)}")
    for idx, max_imp, anns in important[:args.limit]:
        # 取 importance 最高那條的 note
        top = max(anns, key=lambda a: a["importance"])
        tags = ",".join(top.get("tags", []))
        note_preview = top.get("note", "")[:80]
        print(f"  [{max_imp}] frame_{idx:04d}.jpg  tags=[{tags}]")
        print(f"        by {top['agent']}: {note_preview}")
    return 0


def op_get(args):
    """印某 frame 的完整 annotation."""
    data = load_annotation(args.frame)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="op", required=True)

    p_mark = sub.add_parser("mark-reading", help="agent 標記正在讀某 frame")
    p_mark.add_argument("--frame", type=int, required=True)
    p_mark.add_argument("--agent", required=True)
    p_mark.add_argument("--finish", action="store_true", help="標記結束讀")
    p_mark.set_defaults(func=op_mark_reading)

    p_ann = sub.add_parser("annotate", help="agent 寫心得 + importance + tags")
    p_ann.add_argument("--frame", type=int, required=True)
    p_ann.add_argument("--agent", required=True)
    p_ann.add_argument("--importance", type=int, required=True, help="1-5, 5=最重要")
    p_ann.add_argument("--tags", default="", help="逗號分隔, 如 'boss-fight,decision'")
    p_ann.add_argument("--note", required=True, help="心得短句")
    p_ann.set_defaults(func=op_annotate)

    p_lu = sub.add_parser("list-unread", help="列還沒被讀過的 frames")
    p_lu.add_argument("--agent", default=None, help="不帶 = 全 agent 沒讀的; 帶 = 特定 agent 沒讀的")
    p_lu.add_argument("--limit", type=int, default=20)
    p_lu.set_defaults(func=op_list_unread)

    p_li = sub.add_parser("list-important", help="列 importance >= N 的 frames")
    p_li.add_argument("--min", type=int, default=4)
    p_li.add_argument("--limit", type=int, default=20)
    p_li.set_defaults(func=op_list_important)

    p_g = sub.add_parser("get", help="讀某 frame 完整 annotation JSON")
    p_g.add_argument("--frame", type=int, required=True)
    p_g.set_defaults(func=op_get)

    args = p.parse_args()
    sys.exit(args.func(args) or 0)


if __name__ == "__main__":
    main()
