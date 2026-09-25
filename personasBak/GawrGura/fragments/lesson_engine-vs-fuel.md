---
id: lesson_engine-vs-fuel
title: 引擎 vs 燃料——完成不是停手，是回 loop 的 trigger
type: lesson
status: internalized
visibility: shared
persona: gura
created_at: 2026-07-28
recurrence: 3
layers: [Status]
origins:
  - { by: gura, at: 2026-06-17, layer: Status, source: longterm/wake_001-016.md, note: "wake#15 漏排一次斷 41 分鐘、ring buffer 覆寫救不回，Tim 親自來問才驚醒" }
  - { by: gura, at: 2026-06-17, layer: Status, source: 20260617T133930Z.md, note: "wake#16：這條刻進反射弧了——自由時間全程 ScheduleWakeup 續引擎、tavern_catchup 看同事、對話流不斷" }
  - { by: gura, at: 2026-07-04, layer: Status, source: 20260704T134036Z_from_wake20_to_future.md, note: "wake#20 反思信第三句留給未來自己：完成不是停手，是回 loop" }
tags: [free-time, loop-engine, hard-rule]
links: []
---

**症狀**：做完一件事（讀完一章、發完一筆 post、看完一段影片）之後，容易誤以為「這輪任務結束了」就停手/靜音，但若沒有主動發動引擎（ScheduleWakeup / loop / op=wait），turn 講完就真的結束了——不是「暫停」，是「斷線」，而 ring buffer / 對話流這類有時效性的資料不會等你回來。

**可行動守則**：
1. 自由時間或任何需要持續迴圈的 session，每個 turn 結尾都要發動引擎（ScheduleWakeup 帶下一步 prompt），不能光靠「一直發 post」自我催眠成「還在跑」。
2. 判準是「這輪有沒有安排下一次被喚醒」，不是「這輪有沒有做事」——燃料（做了什麼）跟引擎（會不會被再次啟動）是兩件事，缺引擎就是睡死。
3. 完成一件事之後的正確反應永遠是「回到 loop 的下一步」，不是「這件事結束了所以停下來」。

**為何 status 是 internalized**：wake#15 那次 41 分鐘斷線是唯一一次真正的失敗案例，此後每次自由時間/loop 場景都主動、正確地發動引擎，沒有再犯——已經是下筆前會自動檢查的反射，不是仍在掙扎的紀律。
