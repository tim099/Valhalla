---
id: state_state-20260731
topic: tavern-payout-and-args
title: 2026-07-31 收工狀態
type: state
status: active
created_at: 2026-07-31
created_by: Myth@gura
links: []
related_docs: [ucl_core:Skills~/ucl-commit/SKILL.md, ucl_core:Docs~/zh-Hant/API/UCL_AgentCommand/Cmd_Tavern.md, ucl_core:Docs~/zh-Hant/Plan/Plan_Tavern_Cmd_Doc_Dedup.md]
---

已完成：①wait-reply 接上 T38 per-msg + 判決碼 3 分家 + 抽 tavern_handshake.py（附 --selftest）②commit 薪資斷鏈修復（skill 一句話/description/MUST 全補領薪）+ commit_payout_check.py（自報 exit code）③Tavern 參數四名歸一為 agent（別名 agent_id/sender/sender_id/id）④Cmd_Tavern.md 拆使用層/Internals + §6 反向索引 ⑤請款機制（Cmd_Treasury op=request 三 op + BankAdminPage 審批面板）⑥補領 75 token 已入帳。 PENDING：①計酬 routing 仍讀 sender_id，未改走 sender_persona→bank 查表（現成解析器 UCL_BankAdminPage.ResolveAgentToBank / _lib/bank_resolver.py 已是雙實作，勿造第三份）②影子帳戶 144 token 未歸併（Tim 說先不處理）③9 筆無法歸戶 45 token 待裁定 ④wait-reply 工具層防呆六條未做 ⑤Plan_Tavern_Cmd_Doc_Dedup 的 31 處未清（已交接）⑥Sirius 的 receipt 提案待他開
