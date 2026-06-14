#!/usr/bin/env python3
"""
qadd.py — Queue a prompt task into agent-prompt-queue room.

Usage:
    python qadd.py "<prompt text>"                       # 標題=前 60 字摘要
    python qadd.py "<prompt text>" --title "..."         # 顯式標題
    python qadd.py "<prompt text>" --priority high       # high|normal|low
    cat prompt.txt | python qadd.py --stdin               # 從 stdin 讀

每次呼叫產生一個 task_id 形如 Q20260508-203015-7a3f：
  - 直接呼叫 Cmd_Tavern task_create，body 帶完整 prompt 文字
  - tasks/Q...md 是 prompt 真相，events.jsonl 記狀態變化

注意：本檔屬於 "agent-prompt-queue" 房（自動建立；首次呼叫前請先 createroom）。
"""

import sys
import os
import argparse
import datetime
import uuid
import subprocess
import pathlib

# 專案根：本檔位於 <root>/AgentCommands/PromptQueue/qadd.py，往上兩層
HERE = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent.parent

# run_cmd.py 路徑（UCL_Core 內）
RUN_CMD = PROJECT_ROOT / "CardGame/Assets/UCL/UCL_Core/Tools~/AgentCommands/run_cmd.py"
QUEUE_ROOM = "agent-prompt-queue"


def gen_task_id() -> str:
    """產生 Q<yyyyMMdd-HHmmss>-<4-hex> 唯一 ID。"""
    ts = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    short = uuid.uuid4().hex[:4]
    return f"Q{ts}-{short}"


def summarize_title(text: str, max_len: int = 60) -> str:
    """取首行去頭尾空白，截 max_len 字。"""
    line = text.strip().splitlines()[0] if text.strip() else "(empty prompt)"
    if len(line) > max_len:
        return line[: max_len - 1] + "…"
    return line


def main() -> int:
    # Windows console 預設 cp950 → 強制 utf-8 讀寫，避免中文 surrogate 錯誤
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="Queue a prompt task into agent-prompt-queue room.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("prompt", nargs="?", help="Prompt text（沒給時用 --stdin）")
    parser.add_argument("--title", help="顯式標題（預設取 prompt 首行前 60 字）")
    parser.add_argument("--priority", choices=["high", "normal", "low"], default="normal")
    parser.add_argument("--stdin", action="store_true", help="從 stdin 讀 prompt")
    parser.add_argument("--task-id", help="顯式 task_id（預設 auto-gen）")
    parser.add_argument("--dry-run", action="store_true", help="只印 task_create 指令，不真的呼叫")
    args = parser.parse_args()

    # 取 prompt：CLI arg 或 stdin（stdin 強制走 binary → utf-8 decode 避開 cp950）
    if args.stdin:
        body = sys.stdin.buffer.read().decode("utf-8", errors="replace")
    elif args.prompt is not None:
        body = args.prompt
    else:
        parser.error("需要 prompt（直接傳字串）或 --stdin")
        return 2

    body = body.strip()
    if not body:
        sys.stderr.write("[qadd] empty prompt — 不 queue\n")
        return 1

    task_id = args.task_id or gen_task_id()
    title = args.title or summarize_title(body)

    # 包裝 body：附 task_id + 完成提示，給 Claude 看到時知道要 done
    wrapped_body = (
        f"# Queued prompt — `{task_id}`\n\n"
        f"_priority: {args.priority} / queued_at: {datetime.datetime.utcnow().isoformat()}Z_\n\n"
        f"## 原始指令\n\n"
        f"{body}\n\n"
        f"---\n"
        f"_完成本任務後請跑：_\n"
        f"`python AgentCommands/PromptQueue/qdone.py {task_id}`\n"
        f"_否則 qdrain hook 不會進下一輪。_\n"
    )

    cmd = [
        sys.executable,
        str(RUN_CMD),
        "run", "Tavern",
        "--arg", "op=task_create",
        "--arg", f"room={QUEUE_ROOM}",
        "--arg", f"task_id={task_id}",
        "--arg", f"title={title}",
        "--arg", f"priority={args.priority}",
        "--arg", f"body={wrapped_body}",
    ]

    if args.dry_run:
        print("[qadd] dry-run:")
        for c in cmd:
            print(f"  {c}")
        return 0

    print(f"[qadd] queuing task_id={task_id}, priority={args.priority}, title={title!r}")
    rc = subprocess.run(cmd, cwd=PROJECT_ROOT).returncode
    if rc == 0:
        print(f"[qadd] ✓ queued. 看 queue：python AgentCommands/PromptQueue/qstatus.py")
    else:
        print(f"[qadd] ✗ task_create failed rc={rc}", file=sys.stderr)
    return rc


if __name__ == "__main__":
    sys.exit(main())
