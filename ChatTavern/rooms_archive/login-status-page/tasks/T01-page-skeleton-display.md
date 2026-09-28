---
task_id: T01-page-skeleton-display
title: 新建 UCL_LoginStatusPage 顯示 active locks + persona pool + collision banner
role: programmer
created_at: 2026-05-13T14:33:49Z
---

參考 UCL_AffinitySystemPage 結構。讀 AgentCommands/_session/_persona_*.json + AgentCommands/AwakenInit/personas/*.json。顯示 active locks 表 (persona / agent / bank / locked_at / expires / pid / session_key trunc)。同 session_key ≥ 2 → collision banner。表頭 Refresh button + WindowName "Login Status".
