---
task_id: T02-callers-pass-persona
title: cmd_morning / cmd_goodnight / cmd_status callers 傳 persona
role: programmer
depends_on: [T01-compute-session-key-persona-arg]
created_at: 2026-05-13T14:50:41Z
---

cmd_morning 跑 compute_session_key(args.persona)。cmd_goodnight 同。cmd_status 沒 single persona 但要比對每 lock — 改 per-lock 算 compute_session_key(lock.persona) 比對。
