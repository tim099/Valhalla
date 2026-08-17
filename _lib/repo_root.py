#!/usr/bin/env python3
# 區塊職責：跨 Tool 共用的 repo-root 解析器 — 取代各腳本內聯的第 N 份 find_repo_root copy。
# 物理意義：
#   AgentCommands/Tools 下一票工具（ledger 寫入 / workflow_patch / tavern_query 等）都要把
#   相對 AgentCommands/... 的資料路徑釘在「主專案根」上。歷史上各檔各寫一份 find_repo_root，
#   寫法漂移（cwd-相對字串 / .git walk-up / git rev-parse 吃 cwd）正是 cwd 路徑詐欺 bug
#   蔓延全家族的病灶（2026-06-16 qa_bug_reward + 4 支 ledger 工具血證）。本檔把解析邏輯收斂成一處。
# 數值影響：純讀檔系統（os.path.isdir 探測），不寫任何 asset / token。

import os


# 區塊職責：找主專案根 — 錨定「其下同時有 AgentCommands/ 與 CardGame/ 的那層」
# 物理意義：EOV 主專案根 (D:\Unity\EmblemOfValor) 唯一同時擁有這兩個子目錄；
#          AgentCommands submodule 根自身沒有巢狀 AgentCommands/ 也沒有 CardGame/，故會被跳過。
# 數值影響：
#   **刻意不靠 .git**：AgentCommands 是 git submodule，其 .git 為 gitlink『檔』，
#   舊式「遇 .git 就停」會誤停在 submodule 根少算一層；而 `git rev-parse --show-toplevel`
#   吃的是 cwd 不是腳本位置，在 submodule 內 cwd 跑會回 submodule 根 → 同款誤判。
#   本解析改錨定子目錄組合，與呼叫端 cwd 完全解耦。
def find_repo_root(start: str | None = None) -> str:
    """回主專案根的絕對路徑。

    解析優先序：
      1. CLAUDE_PROJECT_DIR env（Claude Code 注入）— 但須通過 anchor 驗證才採用
      2. 從 start（預設本檔位置）逐層往上找通過 anchor 的那層
      3. 保底：本檔在 AgentCommands/_lib/，主根即兩層上

    參數 start：起始探測目錄；預設用本檔位置（與呼叫端 cwd 解耦，最穩）。
    """
    # anchor 判定：某層其下同時看得到 AgentCommands/ 與 CardGame/（主根唯一特徵）
    def _is_root(d: str) -> bool:
        return (
            bool(d)
            and os.path.isdir(os.path.join(d, "AgentCommands"))
            and os.path.isdir(os.path.join(d, "CardGame"))
        )

    # 優先吃 env override，但仍須通過 anchor 驗證（避免 env 指到錯地方靜默誤用）
    env_root = os.environ.get("CLAUDE_PROJECT_DIR")
    if env_root and _is_root(env_root):
        return os.path.abspath(env_root)

    # 從 start（預設本檔位置）逐層往上找
    here = os.path.abspath(start or os.path.dirname(__file__))
    cur = here
    while cur and cur != os.path.dirname(cur):
        if _is_root(cur):
            return cur
        cur = os.path.dirname(cur)

    # 保底：本檔位於 AgentCommands/_lib/repo_root.py，主根 = 兩層上
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


# 區塊職責：便利函式 — 直接組出主根下的子路徑（少打一次 join）
# 物理意義：caller 慣用 repo_path("AgentCommands","Treasury","ledger") 取代手寫 os.path.join(find_repo_root(),...)
# 數值影響：無；純字串組合。
def repo_path(*parts: str) -> str:
    return os.path.join(find_repo_root(), *parts)
