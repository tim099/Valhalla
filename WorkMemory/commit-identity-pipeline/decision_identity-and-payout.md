---
id: decision_identity-and-payout
topic: commit-identity-pipeline
title: 身分與領薪的十三條拍板（含依據與提出者）
type: decision
status: active
created_at: 2026-08-03
created_by: basecamp
links: [ucl-skill-install-sync/state_current, ucl-skill-install-sync/state_state-2026-07-29]
related_docs: [Assets/Plugins/UCL_Core/Skills~/ucl-commit/SKILL.md]
---

**核心判準（今天所有決定共用一句）**：能讓工具做的就不要讓人記得；**人只保留「工具無從得知」的那部分**。

## 已拍板並落地

| 決定 | 內容 | 依據 |
|---|---|---|
| 信箱來源 | `persona.email` → `defaults[actual_agent]` → `fallback` → 哨兵 `unset@invalid` | Tim 2026-08-03 |
| 預設表 key | **`actual_agent`**（封閉集合三值），不是顯示 agent（開放集合，每多一位同事就多一格要填） | basecamp 提、Tim 設定時採用 |
| 查不到時 | 回**哨兵**不回空字串 —— 空字串在 trailer 裡長得像「還沒填」，`unset@invalid` 長得像「壞了」，**只有後者會被人看見** | basecamp |
| 型號欄 | `(<vendor> / <version>)`；vendor 由 `actual_agent` 推導不靠人填，version 知道才寫 | 三票一致（apex-one / meadow / basecamp） |
| 冗餘 | **不剝** version 開頭的 vendor 前綴（`GPT / GPT-5.6 Luna` 照印） | 兩位同事：「字串拆分才可能產生新失真」 |
| 缺 `actual_agent` | 整段沿用 `persona.model` 原值，**不印假精確的 `?`** | 三票一致 |
| model 欄被填成 agent 名 | **底層自動翻譯**，且**刻意不寫進 skill/workflow** —— Tim 實測：提示反而讓人填成 agent 名。防呆一旦被說明就不再是防呆 | Tim 2026-08-03 |
| commit 提交 | 一律走 `git_commit.py`；stage / 切分支 / push 維持手動 | Tim |
| 公告領薪 | **提交後自動發**（`--no-announce` 可關）；可選 `--announce-body` 開場白 | Tim |
| pointer bump | `--bump-of <SHA>` 發極簡公告，帳照領 | meadow |
| 輸出 | 成功一行、異常大聲（Alert Fatigue） | apex-one 命名 |
| hook | **(a)+(b)**：工具內先驗 + 可安裝 hook 擋繞過的人。**不採「只提醒」** | meadow 修正 basecamp 原案 |
| hook 擋什麼 | 只擋「已有 trailer 但信箱/型號/persona 對不上」；**沒有 trailer 一律放行**（人手改的本來就不該掛） | 三方共識 |

## 一條原則層的收穫（meadow 2026-08-03，值得跨工作引用）

> **寫入保存事件，讀取決定怎麼看。**

覺得訊息太密就做 digest / 摺疊 / 依 category 過濾 —— 那些都回得到完整明細。
`--no-announce` 則是把「顯示問題」偽裝成「事件不存在」：**寫入端省略不可逆，讀取端過濾可逆。**
（此條的反面教材是 basecamp 本人：想解「別洗版」卻按下「別留紀錄」。）
