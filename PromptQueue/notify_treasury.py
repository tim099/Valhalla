#!/usr/bin/env python3
"""[T-MOVE shim 2026-07-15] notify_treasury push 路徑已被 pull adapter 收編（Tim 拍板方案 C）。

舊 caller（C# UCL_TreasuryLedger / _lib.treasury_ledger.fire_broadcast）spawn 本檔時，不再逐筆
push POST — 改觸發一次統一 mirror run（notify_discord --mode tavern），新 entry 由 treasury pull
adapter 依 cursor 撿走（冪等：同 entry 不會因多次觸發重複發送）。--entry-file / --stdin 參數
接受但忽略（entry 已在 ledger 落盤，adapter 自己讀）。
"""
import pathlib
import subprocess
import sys

_HERE = pathlib.Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
from AgentCommands._lib import tavern_paths as _tp  # noqa: E402

_TARGET = _tp.UCL_AGENTCMD_DIR / "PromptQueue" / "notify_discord.py"
if not _TARGET.exists():
    print(f"[notify_treasury shim] unified target missing: {_TARGET}", file=sys.stderr)
    sys.exit(1)
rc = subprocess.run([sys.executable, str(_TARGET), "--mode", "tavern"],
                    cwd=str(_REPO_ROOT), capture_output=True).returncode
sys.exit(rc)
