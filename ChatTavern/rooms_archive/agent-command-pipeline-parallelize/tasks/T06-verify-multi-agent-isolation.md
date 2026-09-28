---
task_id: T06-verify-multi-agent-isolation
title: Verify: 雙 agent 同時 submit 互不阻塞 + recompile clean
role: qa
depends_on: [T03-watcher-multi-trigger-scan, T04-runner-agent-id-arg, T05-python-agent-id-arg]
created_at: 2026-05-13T15:07:58Z
---

Test: (1) recompile 0 errors (2) 沒 --agent-id 走 legacy 不破壞 (3) 帶 --agent-id=gemini 跑 → queues/queue-gemini.json 寫入 (4) Zeta 同時 submit → 各自獨立 queue, 不互撞.
