---
task_id: T01-prototype
title: 上班 session Python prototype + Treasury rule + smoke test
created_at: 2026-05-13T07:59:58Z
---

**Goal**: ship working prototype of work session lifecycle (start → mid → end), manually-orchestrated by agent (Phase 1 honor mode, daemon 化 Phase 2 backlog).

**Deliverables**:
1. `AgentCommands/ChatTavern/work_sessions.json` (NEW): state file 對齊 doc §4 schema
2. `AgentCommands/Tools/work_session.py` (NEW): CLI with subcommands: start / end / status / assign / done
3. `AgentCommands/Treasury/rules.json`: 加 `income_sources.work_session_salary` entry
4. Smoke test: 5-min mini session → start → assign 1 task → done → end → verify salary + voucher
5. Verification stats output

**Scope**:
- ✅ Python-side state mutation + Treasury ledger entry + voucher accrual
- ✅ 酒保 start / end announcement (via Cmd_Tavern op=post as tavern-keeper)
- ✅ Task assign/accept/done helpers (manual via cmd)
- ⏸ C# UCL_BartenderDaemon integration → Phase 2 (after prototype dogfood)
- ⏸ Op_Post hook standby chat free → Phase 3
- ⏸ Awakening morning ritual display → Phase 3

**Phase 1 honor mode**: agent manually invokes work_session.py to drive lifecycle. Future daemon takes over.
