---
task_id: T02-letters-refactor
title: 重構 letters/<actor>/ → letters/<actor>/<persona>/ + 改 awakening.py:write_letter()
role: programmer
depends_on: [T01-survey]
created_at: 2026-05-13T11:21:05Z
---

awakening.py 改 letters_dir 用 actor/persona 巢狀。_latest.md 留在 persona 子目錄。dialogues/ 也搬。
