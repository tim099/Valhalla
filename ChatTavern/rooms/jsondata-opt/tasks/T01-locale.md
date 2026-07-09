---
task_id: T01-locale
title: ToJson/ToJsonBeautify 全走 InvariantCulture(+R→G17) 修 locale 資料損毀
role: programmer
created_at: 2026-07-09T07:18:08Z
---

ToJsonBeautify 漏 InvariantCulture(:830/:841) → 德法逗號小數存出非法 JSON。ToJson 已對(:711/:722)。統一兩者走 InvariantCulture,並考慮 R→G17 round-trip。
