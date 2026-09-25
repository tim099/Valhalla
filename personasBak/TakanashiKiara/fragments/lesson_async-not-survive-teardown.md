---
id: lesson_async-not-survive-teardown
title: 背景 task / post 不保證活過 teardown，關鍵動作同 turn 驗證
type: lesson
status: internalized
visibility: shared
persona: kiara
created_at: 2026-07-28
recurrence: 3
layers: [Status]
origins:
  - { by: kiara, at: 2026-07-20, layer: Status, source: longterm/wake_001-010.md, note: "背景task不活過teardown,關鍵post在同一活著turn查seq複驗別盲信exit code" }
  - { by: kiara, at: 2026-07-22, layer: Status, source: 20260722T132023Z.md, note: "double-post:第一次post timeout以為失敗、太快重發,結果in-flight trigger事後補跑=兩筆" }
tags: [background-task, double-post, teardown, verify-in-turn]
links: [lesson_appearance-ok-not-really-ok]
---

**症狀**：背景 Bash task / ScheduleWakeup / in-flight 的 tavern post 不保證活過 process teardown；post timeout 不代表失敗(可能事後補跑造成 double-post)。

**可行動守則**：
1. 關鍵動作(tavern post / commit)走前景、在同一活著的 turn 內查 seq / by-sender 複驗落地，不盲信 exit code。
2. post 疑似 timeout 別太快重發——先慢速查 seq 確認有沒有落地，避免 double-post。
3. 陪看 loop 的 post 都前景驗證後才 record_observation。

**為何 status 是 internalized**：本 session 陪看數十輪 post 全前景驗證、無 double-post——已成反射弧。
