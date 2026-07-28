#!/usr/bin/env python3
"""
qdrain.py — Stop hook：自動消化 prompt queue 下一個 task。

Lifecycle（每次 Claude 回合結束都跑）：
  1. 若 _pause.flag 存在 → exit 0 沉默退出（Tim 暫停）
  2. 讀 events.jsonl 算當前 pending tasks
  3. 沒 pending → exit 0
  4. 挑 priority desc + created_seq asc 第一個 → task_claim
  5. 讀 tasks/<task_id>.md 完整 prompt body
  6. 印 prompt 到 stderr + exit 2 → Claude Code 不結束回合，把 stderr 當新指令繼續

Tim 控制：
  - 暫停 auto-drain：touch AgentCommands/PromptQueue/_pause.flag
  - 恢復：rm AgentCommands/PromptQueue/_pause.flag
  - 看 queue：python AgentCommands/PromptQueue/qstatus.py
  - 加 prompt：python AgentCommands/PromptQueue/qadd.py "..."
"""
import sys
import json
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent.parent
# T-PATH-02: run_cmd.py 走 layout-agnostic resolver, 不再寫死 CardGame/...
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from AgentCommands._lib import tavern_paths as _tp  # noqa: E402
RUN_CMD = _tp.RUN_CMD_PATH
ROOM_DIR = PROJECT_ROOT / "AgentCommands/ChatTavern/rooms/agent-prompt-queue"
EVENTS_PATH = ROOM_DIR / "events.jsonl"
TASKS_DIR = ROOM_DIR / "tasks"
PAUSE_FLAG = HERE / "_pause.flag"
DRAIN_LOG = HERE / "_drain.log"     # 純 debug 紀錄（append-only），出問題時看
DRAIN_ACTOR = "claude-da-xiaojie"   # 預設身分；換 agent 時這條要動


def log(msg: str) -> None:
    """append 到 _drain.log（不影響 stdout/stderr）；保留近 200 行避免膨脹。"""
    try:
        import datetime
        ts = datetime.datetime.utcnow().isoformat() + "Z"
        with DRAIN_LOG.open("a", encoding="utf-8") as f:
            f.write(f"[{ts}] {msg}\n")
        # 簡單 trim：超過 200 行只留尾 200
        lines = DRAIN_LOG.read_text(encoding="utf-8").splitlines()
        if len(lines) > 200:
            DRAIN_LOG.write_text("\n".join(lines[-200:]) + "\n", encoding="utf-8")
    except Exception:
        pass


def load_events():
    """精簡 reducer — 只認 prompt queue 用得到的 event type。"""
    if not EVENTS_PATH.exists():
        return []
    raw = EVENTS_PATH.read_text(encoding="utf-8")
    out = []
    idx = 0
    while idx < len(raw):
        nl = raw.find("\n", idx)
        if nl < 0:
            break  # partial line → 丟
        line = raw[idx:nl]
        idx = nl + 1
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def reduce_states(events):
    states = {}
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
            }
        elif t == "task_claim" and tid in states:
            states[tid]["status"] = "claimed"
            states[tid]["owner"] = ev.get("actor")
        elif t == "task_progress" and tid in states:
            states[tid]["status"] = "in_progress"
        elif t == "task_done" and tid in states:
            states[tid]["status"] = "done"
        elif t == "task_release" and tid in states:
            states[tid]["status"] = "pending"
            states[tid]["owner"] = None
        elif t == "task_reopen" and tid in states:
            states[tid]["status"] = "in_progress"
    return states


def pick_next(states):
    """挑下一個要消化的：priority desc → created_seq asc。"""
    pending = [s for s in states.values() if s["status"] == "pending"]
    if not pending:
        return None
    pscore = {"high": 100, "normal": 50, "low": 0}
    pending.sort(key=lambda s: (-pscore.get(s["priority"], 50), s["created_seq"]))
    return pending[0]


def claim_task(task_id: str) -> bool:
    """走 run_cmd.py 呼叫 Cmd_Tavern task_claim — 維持單一寫者鐵律。"""
    cmd = [
        sys.executable, str(RUN_CMD),
        "run", "Tavern",
        "--arg", "op=task_claim",
        "--arg", "room=agent-prompt-queue",
        "--arg", f"task_id={task_id}",
        "--arg", f"claimer={DRAIN_ACTOR}",
    ]
    try:
        rc = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, timeout=60).returncode
        return rc == 0
    except Exception as e:
        log(f"claim_task exception: {e}")
        return False


def read_task_body(task_id: str) -> str:
    """讀 tasks/<task_id>.md 全文（含 frontmatter + 包裝 body）。"""
    p = TASKS_DIR / f"{task_id}.md"
    if not p.exists():
        return f"_(tasks/{task_id}.md 不存在 — 可能 task_create 失敗)_"
    return p.read_text(encoding="utf-8")


def main() -> int:
    # Windows console 預設 cp950 → 強制 utf-8 stderr，Claude 看到才不會 mojibake
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    # Pause flag 檢查
    if PAUSE_FLAG.exists():
        log("paused (flag exists) → silent")
        return 0

    # Queue 房不存在 → queue 從沒用過
    if not EVENTS_PATH.exists():
        return 0

    events = load_events()
    states = reduce_states(events)
    nxt = pick_next(states)
    if nxt is None:
        log(f"no pending (events={len(events)}, states={len(states)})")
        # 2026-07-28: queue-idle Discord 通知隨 notify_discord.py 一同退役（python → Discord
        # 傳送路徑整條移除；該 stream 實測長期零活動）。需要恢復請在 C# 端補等價 daemon。
        return 0

    task_id = nxt["id"]
    log(f"picking next: {task_id} priority={nxt['priority']} title={nxt['title']!r}")

    if not claim_task(task_id):
        log(f"claim failed for {task_id} → silent (will retry next turn)")
        return 0

    body = read_task_body(task_id)
    pending_left = len([s for s in states.values() if s["status"] == "pending"]) - 1

    # 構造 stderr 訊息：給 Claude 看到當作下一輪指令
    msg_lines = [
        f"[PromptQueue auto-drain] 已 claim 下一個 queued task：`{task_id}`",
        f"剩餘 pending: {pending_left}",
        "",
        "=== 開始任務 ===",
        body,
        "=== 任務結束指令 ===",
        f"完成時務必跑：python AgentCommands/PromptQueue/qdone.py {task_id}",
        f"（沒 done → 下次 Stop hook 會以為這個 task 還在跑，不會抓下一個）",
        "",
        "若 Tim 中途指示「停下」/「pause queue」→ touch AgentCommands/PromptQueue/_pause.flag",
    ]
    sys.stderr.write("\n".join(msg_lines) + "\n")
    log(f"injected task_id={task_id} → exit 2")
    return 2  # 讓 Claude Code 不結束回合，把 stderr 當新指令


if __name__ == "__main__":
    sys.exit(main())
