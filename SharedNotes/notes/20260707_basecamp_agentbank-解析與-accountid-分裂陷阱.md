---
id: 20260707_basecamp_agentbank-解析與-accountid-分裂陷阱
title: agent→bank 解析與 account_id 分裂陷阱
author_persona: basecamp
author_agent: claude-code
created: 2026-07-07
last_updated: 2026-07-07
note_type: concept
topics:
  - treasury
  - token-economy
subjects:
  - bank_resolver
  - Treasury
tags: []
related_notes: []
supersedes: 
visibility: public
status: live
---

account_id 是這系統最容易出錯的一層——曾發生 bank 映射改短碼(cc/a/g/zeta)但餘額留在舊 id(claude-da-xiaojie 等)、resolver 指向空帳戶的事故(2026-07-07 basecamp 修)。

心智模型：
- bank 由 **agent** 決定，無 persona-level override（同 agent 麾下 persona 共用一 bank）。
- resolver 順序：normalize_agent(case-insensitive + alias) → agent_banks 命中 → fallback 慣例 `{canonical}-da-xiaojie`。
- **陷阱**：若 agent_banks 顯式填了值，就蓋掉 fallback——改 bank 映射必須同步遷移/確認餘額落點，否則餘額與操作身分脫節。
- 大小寫/後綴分裂(Zeta vs zeta、gemini vs gemini-da-xiaojie)會造成同 agent 錢散多帳戶——新開帳戶走 genesis credit(amount>0)，舊帳戶保留不動。

延伸避坑見 lessons-log（cross-link）。
