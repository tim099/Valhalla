#!/usr/bin/env python3
# 區塊職責：AgentCommands 端 repo-root 解析的向後相容 shim —— 委派給鏡像 canonical _lib.ucl_paths。
# 物理意義：
#   歷史上本檔自帶一份 find_repo_root，錨「其下同時有 AgentCommands/ 且 CardGame/」。
#   CardGame 是 EOV 專屬特徵 —— 但 AgentCommands 是跨專案共用 submodule
#   (gitlab gamedesign1/agentcommands)，在共用碼裡塞 EOV 假設 = 換專案必斷的 bug
#   (summit QA 驗真, .gitmodules 佐證, 2026-07-04)。
# 數值影響：
#   T-PATH-RESOLVE 裁決二 —— 拔掉 CardGame 錨，錨改鏡像 C# UCL_RepoPath 契約
#   （.git 為「資料夾」才停、gitlink 檔跳過）。該邏輯已收斂在 canonical ucl_paths.py，
#   本檔改為 thin shim 委派過去，不再自己維護第二套解析（避免漂移＝6/16 病灶）。
#   保留 find_repo_root() / repo_path() 舊 API（回 str）給既有呼叫端向後相容。

from __future__ import annotations

import os

# 委派 canonical（AgentCommands/_lib/ucl_paths.py 是 UCL_Core 端的 AUTO-SYNCED 鏡像，
# 由 sync_lib_mirror.py 同步；本檔與它同在 _lib/，sibling import 得到）。
from _lib.ucl_paths import repo_root as _repo_root, data_root as _data_root


# 區塊職責：回主專案根的絕對路徑字串（向後相容 API）。
# 物理意義：解析全走 canonical ucl_paths.repo_root()：
#          tier-1 CLAUDE_PROJECT_DIR → __file__ 起 .git-資料夾 walk（跳 gitlink）→ cwd walk → fallback。
#          與 C# UCL_RepoPath.RepoRoot 對齊，跨專案安全（不再依賴 CardGame 特徵）。
# 數值影響：純唯讀解析。start 參數保留僅為簽名相容 —— 現行解析以本檔／canonical 位置與 env 為準，
#          不再吃呼叫端傳入的起點（歷史上 start 用來避開 cwd 詐欺，canonical 已從結構上解決）。
def find_repo_root(start: str | None = None) -> str:
    return str(_repo_root())


# 區塊職責：便利函式 —— 組出主根下的子路徑字串（向後相容 API）。
# 物理意義：caller 慣用 repo_path("AgentCommands","Treasury","ledger")。
# 數值影響：無；純字串組合（用 os.path.join 保持與舊版一致的字串型別輸出）。
def repo_path(*parts: str) -> str:
    return os.path.join(str(_repo_root()), *parts)


# 區塊職責：新增便利函式 —— 直接取 AgentCommands 資料根（pointer-aware）。
# 物理意義：canonical data_root() 會 honor <repo>/.agentcommands_root.local pointer 檔。
# 數值影響：唯讀；給需要「資料根可能被搬遷」語意的呼叫端用（舊呼叫端可繼續用 repo_path）。
def data_root() -> str:
    return str(_data_root())
