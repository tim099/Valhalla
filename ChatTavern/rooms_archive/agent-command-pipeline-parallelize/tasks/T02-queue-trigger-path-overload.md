---
task_id: T02-queue-trigger-path-overload
title: UCL_AgentCommandQueue: 加 path methods overload (agentId arg) + queues/ subdir
role: programmer
depends_on: [T01-analysis-design]
created_at: 2026-05-13T15:07:54Z
---

GetQueuePath / GetTriggerPath / GetRunningTriggerPath 加 string agentId = null overload。null → 走 default queue.json (legacy backward compat)。非 null → 走 queues/queue-<agent>.json + pending-<agent>.trigger。EnsureDir 同。
