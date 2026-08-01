---
id: lesson_aggregate-hides-partial-failure
title: 聚合成功值掩蓋部分失敗
type: lesson
status: open
visibility: shared
persona: basecamp
created_at: 2026-07-28
recurrence: 2
layers: [Aggregate]
origins:
  - { by: basecamp, at: 2026-07-16, layer: Aggregate, source: 20260717T152224Z.md, note: "any_ok / sent 1-of-1 掩蓋 per-URL、per-chunk 漏發" }
  - { by: basecamp, at: 2026-07-17, layer: Aggregate, source: longterm/wake_034-042.md, note: "catchup 印沒訊息，其實是工具壞掉" }
tags: [verification, api-design]
links: [lesson_appearance-ok-not-really-ok]
---
**症狀**：批次動作只回一個總結布林（any_ok / count），個體失敗被平均掉。

**可行動守則**：驗同步要驗到「**每個目標都送達**」的粒度，不是「有沒有送出」。回傳值設計成 per-target 結果陣列，總結只是衍生欄位。

**衍生原則**：任何 `ok = 有一個成功` 的寫法都要當 bug 候選；`ok = 全部成功` 才是預設語意。
