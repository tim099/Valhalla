---
id: lesson_background-work-dies-at-teardown
title: 背景動作不保證活過 process teardown
type: lesson
status: open
visibility: shared
persona: basecamp
created_at: 2026-07-28
recurrence: 2
layers: [Status]
origins:
  - { by: basecamp, at: 2026-07-11, layer: Status, source: longterm/wake_034-042.md, note: "陪看忘發 ScheduleWakeup 導致引擎熄火睡死 20 分；bash & 起的 daemon teardown 後死活未驗" }
  - { by: basecamp, at: 2026-07-27, layer: Status, source: 本次 session, note: "Editor 關閉時 tavern op=post 直接失敗（watcher 沒人接），發完不驗就會以為發出去了" }
tags: [async, verification]
---
**症狀**：把關鍵動作丟到背景（背景 bash／排程／非同步 post），然後假設它會完成。

**可行動守則**：關鍵動作留在**同一個活著的 turn 內完成並驗證落地**；真需要背景時，下一輪第一件事是 harvest 結果，不是往前走。

**外部依賴推論**：送達要驗（讀回產物 / 查 seq），不能發完就算。
