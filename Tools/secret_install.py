#!/usr/bin/env python3
"""secret_install.py — [DEPRECATED thin wrapper] 委派到 UCL_Core ucl_secret.py.

# 區塊職責：保留 EOV 既有 CLI 入口 (encrypt/decrypt/status)，實作全部委派 UCL_Core 通用版。
# 物理意義：原本這支自己 import secrets_crypto 做加解密；Secret Manager Phase 1 把邏輯抽到
#          UCL_Core (跨專案共用 + 多 hint/show-hint/list/rotate/reveal op)。本檔降級為 thin wrapper，
#          所有現行 caller (RCG_DiscordTokenInstallWindow / daemon / hook) 不必改一行。
# 數值影響：純委派，無自己的 crypto 邏輯。exit code / stdin-passphrase 行為跟 ucl_secret.py 完全一致。

⚠ DEPRECATED：新程式請直接用
    python CardGame/Assets/UCL/UCL_Core/Tools~/AgentCommands/ucl_secret.py <op> ...
本 wrapper 只為 backward-compat 保留 (舊 caller 用 secret_install.py decrypt ... --stdin-passphrase)。

委派後可用的 op 比舊版多 (encrypt/decrypt/status + show-hint/list/rotate/reveal)，
且 encrypt 多接受 --hint / --label。舊有用法全部相容。
"""
from __future__ import annotations

import sys
from pathlib import Path

# 區塊職責：定位 UCL_Core 的 ucl_secret.py 並加進 import path
# 物理意義：本檔在 <repo>/AgentCommands/Tools/，UCL_Core 通用 CLI 在
#          <repo>/CardGame/Assets/UCL/UCL_Core/Tools~/AgentCommands/ucl_secret.py
# 數值影響：路徑算錯會 import 失敗 → 印明確錯誤訊息給人 debug
_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent.parent
# T-PATH-02: UCL_Core Tools~/AgentCommands 走 layout-agnostic resolver, 不再寫死 CardGame/...
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
from AgentCommands._lib import tavern_paths as _tp  # noqa: E402
_UCL_TOOLS = _tp.UCL_AGENTCMD_DIR


def main():
    cli = _UCL_TOOLS / "ucl_secret.py"
    if not cli.exists():
        print(f"[err] UCL_Core ucl_secret.py 不存在: {cli}\n"
              f"      (secret_install.py 已降級為 thin wrapper，需 UCL_Core submodule 就位)",
              file=sys.stderr)
        sys.exit(127)

    # 區塊職責：import UCL_Core 通用 CLI 並委派 main()
    # 物理意義：argparse 讀 sys.argv[1:] (忽略 argv[0])，故 op + 參數原樣 pass-through，
    #          stdin (passphrase pipe) 由同一 process 繼承，無需額外處理。
    sys.path.insert(0, str(_UCL_TOOLS))
    import ucl_secret  # noqa: E402
    ucl_secret.main()


if __name__ == "__main__":
    main()
