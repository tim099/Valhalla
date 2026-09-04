#!/usr/bin/env python3
"""
qstatus.py — 列出 prompt queue 中所有 task 狀態。

Usage:
    python qstatus.py                                    # 全部 task
    python qstatus.py --pending-only                     # 只看待消化（pending/ready）
    python qstatus.py --raw                              # 直接印 task_list 的 last_op markdown

讀 events.jsonl 自己 reduce（純查詢，不打擾 Editor）。
"""
import sys
import argparse
import json
import pathlib
from typing import Dict, List

HERE = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent.parent
# T-PATH-02: run_cmd.py 走 layout-agnostic resolver, 不再寫死 CardGame/...
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from AgentCommands._lib import tavern_paths as _tp  # noqa: E402
EVENTS_PATH = PROJECT_ROOT / "AgentCommands/ChatTavern/rooms/agent-prompt-queue/events.jsonl"
PAUSE_FLAG = HERE / "_pause.flag"


def load_events() -> List[dict]:
    """讀 events.jsonl，跳過 partial 行（行尾沒 \\n）— 跟 C# reducer 一致。"""
    if not EVENTS_PATH.exists():
        return []
    raw = EVENTS_PATH.read_text(encoding="utf-8")
    events = []
    idx = 0
    while idx < len(raw):
        nl = raw.find("\n", idx)
        if nl < 0:
            break  # partial line at end → skip
        line = raw[idx:nl]
        idx = nl + 1
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


def reduce_states(events: List[dict]) -> Dict[str, dict]:
    """從 events.jsonl 重放算每 task 當前 status / owner / priority / created_seq。
    精簡版 reducer — 只懂 prompt queue 用得到的 type。"""
    states: Dict[str, dict] = {}
    for ev in events:
        tid = ev.get("task_id")
        if not tid:
            continue
        t = ev.get("type")
        if t == "task_create":
            data = ev.get("data") or {}
            states[tid] = {
                "id": tid,
                "title": data.get("title", ""),
                "priority": data.get("priority", "normal"),
                "status": "pending",
                "owner": None,
                "created_seq": ev.get("seq", 0),
                "created_at": ev.get("ts", ""),
            }
        elif t == "task_claim":
            if tid in states:
                states[tid]["status"] = "claimed"
                states[tid]["owner"] = ev.get("actor")
        elif t == "task_progress":
            if tid in states:
                states[tid]["status"] = "in_progress"
        elif t == "task_done":
            if tid in states:
                states[tid]["status"] = "done"
        elif t == "task_release":
            if tid in states:
                states[tid]["status"] = "pending"
                states[tid]["owner"] = None
        elif t == "task_reopen":
            if tid in states:
                states[tid]["status"] = "in_progress"
    return states


def priority_score(st: dict) -> int:
    """high=100 normal=50 low=0；不算 age_factor (queue 跑得勤，老化沒太大意義)。"""
    return {"high": 100, "normal": 50, "low": 0}.get(st["priority"], 50)


def sort_pending(states: Dict[str, dict]) -> List[dict]:
    """挑 pending → 按 priority desc → created_seq asc。"""
    pending = [s for s in states.values() if s["status"] == "pending"]
    pending.sort(key=lambda s: (-priority_score(s), s["created_seq"]))
    return pending


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--pending-only", action="store_true", help="只看 pending（未消化）")
    parser.add_argument("--raw", action="store_true", help="走 task_list 走 Editor（含 ready 偵測等完整算法）")
    args = parser.parse_args()

    if args.raw:
        # 走 Editor 拿完整版（慢但準）
        # 2026-09-04（TASK-0107）：派遣由 `python run_cmd.py` 換成 `senate ucmd run`。
        # 路徑走 `_tp.senate_exe()`（三層解析），⛔ 不寫裸字串 "senate"（PATH 是使用者環境，別台不保證）。
        # 解不到時 senate_exe() 會 raise ⇒ 這裡**刻意不 catch**：
        #   這條路是 `--raw` 顯式要求「走 Editor 拿準的」，靜默退回本地估算會給出一份
        #   看起來正常、但**不是使用者要的那一份**讀數 —— 那比直接失敗貴。
        # 🩸 順手修掉一格既有缺陷（不是這次轉接造成的，但我不照抄它）：
        #   舊寫法不帶 lane 旗標 ⇒ 實測落進 `queues/anonymous/`（`→ LY:anonymous`），
        #   跟所有「漏帶 --persona 的人」擠同一條 lane 互相阻塞，而那個資料夾因此不再是儀表。
        #   ⇒ 帶 `--persona system`：這筆**不是人派的**（qstatus 是查詢工具，沒有「誰」），
        #     跟 `_lib/treasury_cmd.py` 的金流 Cmd 同一個理由。
        #   ⚠ lane 只決定走哪條佇列，**不宣告身分** —— 本 op 是唯讀查詢，沒有身分語意。
        import subprocess
        cmd = [str(_tp.senate_exe()), "ucmd", "run", "Tavern", "--persona", "system",
               "--arg", "op=task_list", "--arg", "room=agent-prompt-queue"]
        return subprocess.run(cmd, cwd=PROJECT_ROOT).returncode

    events = load_events()
    states = reduce_states(events)

    paused = PAUSE_FLAG.exists()
    pending = [s for s in states.values() if s["status"] == "pending"]
    in_prog = [s for s in states.values() if s["status"] in ("claimed", "in_progress")]
    done = [s for s in states.values() if s["status"] == "done"]

    print(f"# 📋 PromptQueue — agent-prompt-queue")
    print()
    print(f"- pause flag: {'🔴 PAUSED' if paused else '🟢 active (auto-drain)'}")
    print(f"- pending: **{len(pending)}** / in_progress: **{len(in_prog)}** / done: **{len(done)}**")
    print()

    if args.pending_only:
        rows = sort_pending(states)
        if not rows:
            print("_(沒 pending — queue 空）_")
            return 0
        print("## Pending（按消化順序）")
        for i, s in enumerate(rows, 1):
            print(f"{i}. `{s['id']}` [{s['priority']}] — {s['title']}")
        return 0

    if pending:
        print("## 🟢 Pending（按消化順序）")
        for i, s in enumerate(sort_pending(states), 1):
            print(f"{i}. `{s['id']}` [{s['priority']}] — {s['title']} _(created {s['created_at']})_")
        print()
    if in_prog:
        print("## 🚧 In Progress")
        for s in in_prog:
            print(f"- `{s['id']}` [{s['status']}] — owner: {s['owner']} — {s['title']}")
        print()
    if done:
        print(f"## ✅ Done（{len(done)} 筆）")
        for s in done[-5:]:  # 最新 5 筆
            print(f"- `{s['id']}` — {s['title']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
