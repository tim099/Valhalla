---
id: lesson_no-position-derived-cursor
title: 位置推導的游標會漂 — 一律 glob / append-only
type: lesson
status: internalized
visibility: shared
persona: basecamp
created_at: 2026-07-28
recurrence: 3
layers: [Identity]
origins:
  - { by: basecamp, at: 2026-07-16, layer: Identity, source: 20260717T152224Z.md, note: "用檔名排序位置推導 seq 當穩定游標 = Discord 漏發真兇" }
  - { by: basecamp, at: 2026-07-16, layer: Identity, source: 20260717T152224Z.md, note: "Books 兩處聚合檔併發衝突，改 per-entry append-only" }
tags: [cursor, concurrency]
links: [lesson_appearance-ok-not-really-ok]
---
**症狀**：拿「檔案在排序中的第幾個」當穩定 ID。新增／刪除／重排一發生，游標指向的東西就換人了。

**可行動守則**：讀取一律 glob 全量、寫入一律 per-entry append-only；游標存**內容 ID 或 mtime**，絕不存位置。

**已內化證據**：2026-07-27 檢視 tavern seq 從「成功 parse 數」改「檔數」時，第一反應就是問「壞檔會不會讓兩者漂」——反射弧已經在。
