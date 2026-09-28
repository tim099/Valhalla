---
task_id: T03-watcher-multi-trigger-scan
title: UCL_AgentCommandWatcher: 掃 default + queues/ subdir 所有 trigger 並 dispatch
role: programmer
depends_on: [T02-queue-trigger-path-overload]
created_at: 2026-05-13T15:07:55Z
---

當前 watcher 1s poll 看 default trigger。改成掃 default + 列舉 queues/pending-*.trigger。各觸發 trigger MarkRunning + 對應 Runner.RunAsync(agentId)。多 trigger 同時可並行 dispatch (UniTask)。
