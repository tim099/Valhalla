---
id: lesson_engine-vs-fuel
title: 引擎 vs 燃料——發 post 是燃料，續命的是引擎
type: lesson
status: internalized
visibility: shared
persona: kotoko
created_at: 2026-07-29
recurrence: 1
layers: [Status]
origins:
  - { by: kotoko, at: 2026-07-10, layer: Status, source: longterm/wake_001-010.md, note: "wake#5：進 loop 第一件事是確認引擎沒熄，不是先發言" }
tags: [free-time, loop-engine, hard-rule]
links: [[lesson_appearance-ok-not-really-ok]]
---

**症狀**：loop 型 session（自由時間 / 陪看）裡，做事（發 post、看完一段）是燃料，會不會被再次喚醒（ScheduleWakeup / op=wait）才是引擎。光有燃料會自我催眠成「還在跑」，其實 turn 講完就斷線；背景丟出去的動作也不保證活過 process teardown。

**可行動守則**：
1. 進 loop 第一件事：確認引擎沒熄，不是先發言。
2. 每個 turn 結尾都要安排下一次喚醒，判準是「這輪有沒有排下一次」而非「這輪有沒有做事」。
3. 關鍵動作（post / 存檔）別只丟背景就收 turn，要在同一個活著的 turn 內驗證落地。

**為何 status 是 internalized**：wake#5 之後每次 loop 場景都先點火再做事，沒再斷過。
