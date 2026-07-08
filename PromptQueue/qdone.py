#!/usr/bin/env python3
"""
qdone.py — 標記 queued task 完成。Claude 跑完 queued prompt 必跑。

Usage:
    python qdone.py <task_id>                           # 預設 actor=claude-da-xiaojie
    python qdone.py <task_id> --actor gemini-da-xiaojie

只是 Cmd_Tavern task_done 的 thin wrapper — 房名固定 agent-prompt-queue。
"""
import sys
import argparse
import subprocess
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent.parent
# T-PATH-02: run_cmd.py 走 layout-agnostic resolver, 不再寫死 CardGame/...
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from AgentCommands._lib import tavern_paths as _tp  # noqa: E402
RUN_CMD = _tp.RUN_CMD_PATH
QUEUE_ROOM = "agent-prompt-queue"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("task_id")
    parser.add_argument("--actor", default="claude-da-xiaojie")
    args = parser.parse_args()

    cmd = [
        sys.executable, str(RUN_CMD),
        "run", "Tavern",
        "--arg", "op=task_done",
        "--arg", f"room={QUEUE_ROOM}",
        "--arg", f"task_id={args.task_id}",
        "--arg", f"actor={args.actor}",
    ]
    rc = subprocess.run(cmd, cwd=PROJECT_ROOT).returncode
    if rc == 0:
        print(f"[qdone] ✓ {args.task_id} marked done")
    return rc


if __name__ == "__main__":
    sys.exit(main())
