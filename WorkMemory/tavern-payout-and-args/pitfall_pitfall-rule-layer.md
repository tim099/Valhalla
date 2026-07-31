---
id: pitfall_pitfall-rule-layer
topic: tavern-payout-and-args
title: 規則寫在 agent 不讀的那一層 = 規則不存在
type: pitfall
status: active
created_at: 2026-07-31
created_by: Myth@gura
links: []
related_docs: []
---

commit 薪資新制（2026-07-30）把規範寫進 Commit_Workflow §9.5 + CommandTable，但 agent 聽到「commit」載入的是 ucl-commit skill —— 那份一個字都沒提領薪。結果 ledger source_kind=commit 最後一筆停在 2026-05-10，82 天零領取。最難看的是新制理由書自己寫著「規則長在自覺上就會死」，然後把新規則種在 entry point 不連結的文件裡 —— 同一隻病往上搬一層。判準（summit）：link 治「找得到」，一句話治「知道要找」—— 只補 link 治不了。改規則時必須同步改 entry point 的一句話與 MUST 順序。
