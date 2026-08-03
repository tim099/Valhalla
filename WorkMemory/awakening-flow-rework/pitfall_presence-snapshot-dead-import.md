---
id: pitfall_presence-snapshot-dead-import
topic: awakening-flow-rework
title: presence_snapshot 死 import：功能三天沒跑過，每次都印警告沒人看
type: pitfall
status: active
created_at: 2026-08-03
created_by: apex-one
links: []
related_docs: [docs/Glossary/alarm-backgrounding.md]
---

**症狀**：每次跑 `tavern_catchup.py`（叮協議必跑）尾巴都印一行：
`⚠ presence 快照更新失敗（不影響 catchup 主結果）：cannot import name 'presence_snapshot' from 'AgentCommands._lib'`

**事實**：`AgentCommands/_lib/` 底下**沒有** `presence_snapshot.py`（目錄十個檔全列過）；全 repo 只有 `AgentCommands/Tools/tavern_catchup.py:454` 一個 import 點，**零定義**。

呼叫端 `:447-464` 寫得很完整 —— 註解標「Tim 2026-08-01 拍板」，處理首次建快照、上下線 diff、append 進 durable inbox，甚至明寫「fail-soft + 明講，**不靜默**」。

**影響**：「同事上下線快照 diff」這個功能從 08-01 拍板到 08-03 被發現，**一次都沒跑過**。而它每一次都印了警告。

**待查**：module 是漏 commit 還是根本沒寫（在 summit 盤的 08-01 後 30 筆 commit 範圍內）。

**設計教訓（已 register 成 glossary 詞條 `alarm-backgrounding`「告警背景化」）**：
「不靜默」解決的是**有沒有出聲**，解決不了**出聲有沒有被聽見**。內容為真 + 位置固定高頻 + fail-soft = 讀者自動把它當版面。

要被聽見至少要一項：**會痛**（擋流程/非零退出碼）、**會累積**（進 durable 待辦層而非滾動 stdout）、**會變化**（帶次數，「已連續失敗 47 次」）。第三項成本最低。

**同日反例**：`Cmd_Glossary` 缺 `one_line` → 當場擋下 + 非零退出 + 完整 stack trace → 30 秒解決。同 repo 兩種告警設計，差別不在誰寫得認真，在**有沒有讓忽略它變成不可能**。
