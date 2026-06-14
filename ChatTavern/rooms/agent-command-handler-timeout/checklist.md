# ✅ Checklist — agent-command-handler-timeout

_衍生 cache；最後更新 2026-05-13 15:38:56 UTC_

- ✅ **T01-handler-timeout-property** UCL_AgentCommandHandlerBase 加 TimeoutSeconds virtual property (default 1200s)
- ✅ **T02-runner-timeout-wrap** Runner: Task.WhenAny(handler.ExecuteAsync, Task.Delay) wrap + args _timeout_sec override
- ✅ **T03-verify-recompile-smoke** Recompile + smoke test (default + override + slow cmd timeout fire)
- ✅ **T04-doc-sync** Architecture §8.1 backlog 移到 shipped + AgentCommand handler doc 加 TimeoutSeconds property
