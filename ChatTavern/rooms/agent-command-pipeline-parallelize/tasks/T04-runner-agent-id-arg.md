---
task_id: T04-runner-agent-id-arg
title: UCL_AgentCommandRunner / Trigger: 加 agentId 參數 + MarkRunning 對應檔
role: programmer
depends_on: [T02-queue-trigger-path-overload]
created_at: 2026-05-13T15:07:56Z
---

Runner.RunAsync(string agentId = null), Trigger.MarkRunning(agentId) / Clear(agentId) 全 overload。null → 走 default 路徑 (existing behavior)。
