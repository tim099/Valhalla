---
task_id: T01-collision-detect-status
title: awakening.py status: 偵測 session_key 多 lock collision + 顯示 pid/locked_at + 移除 single-key ownership 假設
role: programmer
created_at: 2026-05-13T13:06:20Z
---

同 session_key 多筆 lock → 印 ⚠ collision 警告; lock 列加 pid 短前綴 + locked_at ts; 不再用 single key 標「← me」。改用 process-aware hint「← same key, pid 不同 (另 Claude invoke)」.
