---
id: decision_decision-agent-canonical
topic: tavern-payout-and-args
title: 參數 canonical 定為 agent，值域是 agent/bank 不是 persona
type: decision
status: active
created_at: 2026-07-31
created_by: Myth@gura
links: []
related_docs: []
---

Tim 2026-07-31 拍板。C# ArgsSpec 是唯一真相源（python 吃反射產物 commands_schema.json 並驗 source_hash，過期自動降級不擋）→ 改一處全鏈生效。別名宣告順序必須對齊 handler 巢狀序（順序錯不報錯，會安靜選錯值）。GetAgentArg 刻意不收 id —— id 是超載名（createroom/campaign 的 id 是房間 id）。task_* 保留 actor/claimer 當 canonical（語意不同）。血證：hook 拿未驗證的 sender 當帳戶，summit 帶 persona 名 summit（bank 應為 zeta）→ 錢進影子帳戶。
