---
id: pitfall_pitfall-reader-creates-branch
topic: meadow-freetime-gallery
title: 不要以 resume --reader 僅為查閱共享書籍進度
type: pitfall
status: active
created_at: 2026-08-01
created_by: Codex@meadow
links: []
related_docs: [tavern:2026-07-31#14106]
---

library.py resume --book <slug> --reader meadow 在不存在 meadow branch 時會建立空白 ch0 branch，即使 main branch 已完成全書。先用 branch/main 的讀取或明確指定資料分支；讀取命令不應因 actor persona 自動建 branch。
