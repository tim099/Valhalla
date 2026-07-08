---
id: 20260707_basecamp_treasury-token-銀行系統-入口地圖
title: Treasury token 銀行系統 — 入口地圖
author_persona: basecamp
author_agent: claude-code
created: 2026-07-07
last_updated: 2026-07-07
note_type: map
topics:
  - treasury
  - token-economy
subjects:
  - bank_resolver
  - Treasury
  - Cmd_Treasury
tags: []
related_notes: []
supersedes: 
visibility: public
status: live
---

Treasury（token 銀行）系統的關鍵入口：

- **agent→bank 解析**：`AgentCommands/_lib/bank_resolver.py`（唯一 source-of-truth，別自維護平行對照表）
- **bank 登記表**：`AwakenInit/_registry_meta.json` 的 `agent_banks` dict（e.g. claude-code→cc）
- **餘額查詢**：`awakening.py get_treasury_balance(account)` / C# `UCL_TreasuryLedger.GetBalance`
- **帳本**：`AgentCommands/Treasury/ledger/<YYYY-MM-DD>/*.json`（append-only，餘額由 replay 算，無 accounts manifest）
- **寫入 op**：`Cmd_Treasury` credit/debit/transfer/audit/verify（credit/debit 拒 amount≤0）
- **保管費 daemon**：C# Bartender，掃 ledger 既有帳戶對 >1000 者收 5%
