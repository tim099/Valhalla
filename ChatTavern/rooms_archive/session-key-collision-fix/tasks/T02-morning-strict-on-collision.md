---
task_id: T02-morning-strict-on-collision
title: cmd_morning: 偵測 collision 且 caller 沒帶 --persona → 拒絕 reuse + 要求 --strict-persona 顯式指定
role: programmer
depends_on: [T01-collision-detect-status]
created_at: 2026-05-13T13:06:21Z
---

當前 Step 0 same-persona re-awakening short-circuit 假設 session_key match = 自己。collision 場景下會 reuse 別 process 的 lock。改成 collision 偵測 → 強制 explicit --persona, 不 short-circuit.
