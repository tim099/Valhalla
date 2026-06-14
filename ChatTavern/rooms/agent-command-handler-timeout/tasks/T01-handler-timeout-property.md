---
task_id: T01-handler-timeout-property
title: UCL_AgentCommandHandlerBase 加 TimeoutSeconds virtual property (default 1200s)
role: programmer
created_at: 2026-05-13T15:33:23Z
---

HandlerBase 加 public virtual int TimeoutSeconds => 1200 (20 min). 各 cmd 子類可 override (e.g. Cmd_Tavern wait-reply override 1500s+).
