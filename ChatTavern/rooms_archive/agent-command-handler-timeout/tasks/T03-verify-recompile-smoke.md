---
task_id: T03-verify-recompile-smoke
title: Recompile + smoke test (default + override + slow cmd timeout fire)
role: qa
depends_on: [T02-runner-timeout-wrap]
created_at: 2026-05-13T15:33:25Z
---

Test: (1) recompile 0 errors (2) default cmd 不 timeout 正常跑 (3) 帶 --arg _timeout_sec=5 sleeplong cmd → timeout fire + LastRunError 標 (4) handler subclass override 生效
