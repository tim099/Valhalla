---
task_id: T02-verify-3-paths
title: Verify 4 條測試 case (per design doc)
role: qa
depends_on: [T01-add-rebind-flag]
created_at: 2026-05-13T13:29:03Z
---

Test: (1) cross-agent claim 無 flag → reject (2) + --rebind-agent → rebind OK (3) + --fork-name → fork OK (4) same-agent persona → 原 reuse 不變.
