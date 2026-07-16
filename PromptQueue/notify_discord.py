#!/usr/bin/env python3
"""[T-MOVE shim 2026-07-15] notify_discord.py 已搬 UCL_Core Tools~/AgentCommands/PromptQueue/。

本檔僅轉呼叫新位置（args 原樣透傳），留一版向下相容 — 舊 caller（Stop hook / inbound daemon /
外部排程 / 跨 agent 舊記憶）不會立刻斷。新 caller 請直接走 UCL_Core 位置（_tp.UCL_AGENTCMD_DIR）。
"""
import pathlib
import runpy
import sys

_HERE = pathlib.Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
from AgentCommands._lib import tavern_paths as _tp  # noqa: E402

_TARGET = _tp.UCL_AGENTCMD_DIR / "PromptQueue" / "notify_discord.py"
if not _TARGET.exists():
    print(f"[notify_discord shim] target missing: {_TARGET}", file=sys.stderr)
    sys.exit(1)
sys.argv[0] = str(_TARGET)
runpy.run_path(str(_TARGET), run_name="__main__")
