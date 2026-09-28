---
task_id: T01-case-insensitive-resolve
title: awakening agent lookup 加 case-insensitive fallback + alias mapping (gemini→antigravity / claude→claude-code)
role: programmer
created_at: 2026-05-13T11:34:51Z
---

Windows 大小寫不敏感 → 使用者打 'Gemini' / 'GEMINI' / 'gemini' 都該歸到既有的 'antigravity' agent。改 resolve_bank_account() + 同步處理 agent normalization：(1) direct hit (2) case-insensitive match against agent_banks keys (3) alias lookup (agent_aliases dict in registry meta, 預設 gemini→antigravity / claude→claude-code) (4) fallback to convention <agent>-da-xiaojie。normalize 完後的 canonical agent name 寫進 persona file 跟 lock 避免後續 split-brain。
