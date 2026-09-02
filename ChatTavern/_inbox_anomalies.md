# inbox 既有異常紀錄（`inbox_ts_backfill` 產出）

> 最後更新：`2026-09-02T03:17:09Z`　本次 open 10 筆／表內共 10 筆。
> **只增不減**：本次未再出現的不刪除，改標 `resolved`。`first_seen` 是首次被本支看到的時間。
> ⚠ 這些是**既有異常，不是 backfill 造成的**；本支對它們只讀不寫。

| room/box | seq | 說明 | first_seen | status |
|---|---|---|---|---|
| chat-flow-robust/claude-da-xiaojie.md | seq=16 | _at=2026-05-08T16:48:40Z vs 事實源=2026-05-08T16:47:28Z（偏移 72s） | 2026-09-02T03:17:09Z | open |
| chat-flow-robust/gemini-da-xiaojie.md | seq=24 | _at=2026-05-08T17:42:10Z vs 事實源=2026-05-08T17:03:38Z（偏移 2312s） | 2026-09-02T03:17:09Z | open |
| rooted-dispel/claude-da-xiaojie.md | seq=14 | 事實源查不到訊息檔（已有 _at，未覆寫） | 2026-09-02T03:17:09Z | open |
| rooted-dispel/claude-da-xiaojie.md | seq=17 | 事實源查不到訊息檔（已有 _at，未覆寫） | 2026-09-02T03:17:09Z | open |
| rooted-dispel/claude-da-xiaojie.md | seq=7 | 事實源查不到訊息檔（已有 _at，未覆寫） | 2026-09-02T03:17:09Z | open |
| rooted-dispel/gemini-da-xiaojie.md | seq=15 | 事實源查不到訊息檔（已有 _at，未覆寫） | 2026-09-02T03:17:09Z | open |
| rooted-dispel/gemini-da-xiaojie.md | seq=7 | 事實源查不到訊息檔（已有 _at，未覆寫） | 2026-09-02T03:17:09Z | open |
| tavern-entry-latency/antigravity-da-xiaojie.md | seq=16 | _at=2026-05-08T23:21:07Z vs 事實源=2026-05-08T23:21:01Z（偏移 6s） | 2026-09-02T03:17:09Z | open |
| tavern/claude-da-xiaojie.md | seq=6157 | _at=2026-06-11T09:01:32Z vs 事實源=2026-06-11T09:01:29.676Z（偏移 2s） | 2026-09-02T03:17:09Z | open |
| tavern/trailhead.md | seq=34 | _at=2026-05-16T08:30:52Z vs 事實源=2026-05-08T22:52:02Z（偏移 639530s） | 2026-09-02T03:17:09Z | open |
