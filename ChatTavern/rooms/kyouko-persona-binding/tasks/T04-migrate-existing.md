---
task_id: T04-migrate-existing
title: 搬遷既有 letters/baton 進新結構（best-effort 讀 frontmatter written_by_persona）
role: programmer
depends_on: [T02-letters-refactor]
created_at: 2026-05-13T11:21:10Z
---

python migration script: 讀每筆 letter frontmatter 撈 written_by_persona，搬進 letters/<actor>/<persona>/。沒 persona meta 的留原處或進 _unassigned/。
