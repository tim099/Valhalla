---
task_id: T02-runner-timeout-wrap
title: Runner: Task.WhenAny(handler.ExecuteAsync, Task.Delay) wrap + args _timeout_sec override
role: programmer
depends_on: [T01-handler-timeout-property]
created_at: 2026-05-13T15:33:24Z
---

Runner.RunAsync per-cmd block 內: 先讀 c.Args._timeout_sec int 覆寫 handler.TimeoutSeconds default. Task.WhenAny(handler 跑, Task.Delay(timeoutMs)). timeout 先到 → CancellationToken cancel + 標 LastRunError=timeout (Cancel ≠ Timeout caveat 文檔記下, handler 不 honor token 仍跑但 Runner 不被卡).
