---
task_id: T05-lease-cwd-fix
title: check_task_lease.py git rev-parse cwd bug 修掉
role: programmer
depends_on: [T01-ucl-paths]
created_at: 2026-07-04T02:47:28Z
---

【裁決三 Q3 核准併批】check_task_lease.py get_repo_root() 的 git rev-parse --show-toplevel 吃 caller cwd，在 submodule 內跑回錯根。改錨 __file__（或用 ucl_paths.repo_root()）。一行的事，同批修。驗收：從 submodule 目錄 cwd 跑仍回 host repo root。
