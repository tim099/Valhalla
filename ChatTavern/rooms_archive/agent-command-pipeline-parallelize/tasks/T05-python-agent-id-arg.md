---
task_id: T05-python-agent-id-arg
title: run_cmd.py --agent-id <X> arg + ensure_idle per-agent
role: programmer
depends_on: [T02-queue-trigger-path-overload]
created_at: 2026-05-13T15:07:57Z
---

run_cmd.py 加 --agent-id arg。有帶 → 寫 queues/queue-<X>.json + pending-<X>.trigger; ensure_idle 對應 trigger/running。沒帶 → legacy queue.json (default fallback)。
