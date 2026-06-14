---
task_id: T01-add-rebind-flag
title: awakening.py 加 --rebind-agent flag + Step 3 改 reject path
role: programmer
created_at: 2026-05-13T13:29:02Z
---

argparse 加 --rebind-agent (action store_true). Step 3 (line 942-944) silent rebind 改成 cross-agent claim 偵測 → 沒帶 flag exit 2 + hint 三 path; 帶 flag 走原 rebind 印 ack message.
