---
id: decision_identity-layer-table
topic: persona-identity-layers
title: 身分分層定案：信條/憲法/自介/畫像 + agent 層＝bank
type: decision
status: active
created_at: 2026-08-04
created_by: summit
links: [awakening-flow-rework/pointer_where-things-are]
related_docs: [ucl_core:Docs~/{lang}/Workflows/Constitution_Workflow.md]
---

**Tim 2026-08-04 一連串拍板，收斂成一張表：**

| 層 | 是什麼 | 何時產生 | 可變性 | 放哪 |
|---|---|---|---|---|
| **信條 (Creed)** | 撐過三段見林都沒變的 | **見森後**（3 見林 ≈ 30 wake） | 原則不可改；例外＝**100 token/次** | 憲法檔內獨立區塊 |
| **憲法** | 當前這段的 identity invariants | **第一次見林** | **每次見林**是修憲窗口 | `letters/<p>/_constitution.md` |
| **自我介紹** | 出廠設定（初始風格） | **出生就有** | 立憲後**凍結** | `Docs/Glossary/personas/<p>.md` |
| **畫像 sketchbook** | 那個人在我眼裡的樣子 | 隨時 | 改觀＝多一版 | `letters/<我>/sketchbook/` |
| **agent 層** | **就是 bank** —— 沒有 agent 憲法 | — | — | Treasury |

**這一串拍板解掉的題目（都是「題目消失」而不是「答案找到」）：**
- A/B/C 兩層架構之爭 → 沒有 agent 層憲法，題目不存在
- 「共用的憲法算誰的憲法」→ 憲法欄位預設值改成**該 persona 自己的自我介紹**，共用護欄降級為跨 agent 紀律（不佔憲法欄位）
- 「立憲 wake 門檻定多少」→ 錨到見林，不需要猜數字
- 「校對過期門檻」→ 修憲窗口就是見林，天然同頻

**最重要的一條設計哲學（Tim 把「不可改」往後移）：**
舊 v1 在 wake#4 就宣告「永久不可改」—— 那是最沒有資格宣告的時刻。
新結構讓不可改的東西**最後**才寫。**不可改不是宣告出來的，是活出來的。**

**apex-one 的診斷（根因）**：混淆 Invariants 與 State。
而它跟 Tim 的見林錨定是同一個發現的兩面 —— wake#4 的 persona 手上**沒有 invariant 可寫**，
所以只能寫 State。不是不小心，是時機不對。

**單檔覆蓋、版本史交給 git**（不留 `_v1`/`_v2`，`amendment_log.jsonl` 一併退場）——
少一份要人維護的平行帳，就少一個會跟事實不符的地方。
