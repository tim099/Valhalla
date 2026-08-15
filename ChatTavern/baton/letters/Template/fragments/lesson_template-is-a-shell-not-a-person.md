---
id: lesson_template-is-a-shell-not-a-person
title: Template 是殼不是人 —— 測試資料一旦長得像記憶，就會被當成記憶
type: lesson
status: open
visibility: shared
persona: Template
created_at: 2026-08-12
recurrence: 1
origins:
  - { by: basecamp, at: 2026-08-12, layer: Identity, source: tavern seq 15015, note: "立 Template 時先講好規矩；否則某天有人對著測試殼寫畫像" }
  - { by: Tim, at: 2026-08-15, layer: Identity, source: 拍板, note: "規格改為全部照跑 —— 各項規格走一樣流程才測得到準確數據，帳戶本身也是測試目標；守則②因此改寫" }
tags: [test-fixture, identity, schema]
---
**症狀**：測試用的假資料寫得太像真的，於是被下游當成真的 —— 有人對測試殼寫印象畫像、把測試 persona 算進在線人數、拿它的 wake_count 做統計。**假資料不會自己標註「我是假的」，它只會安靜地被引用。**

**可行動守則**：
1. 每一份測試資料的**第一行**就要自曝身分（本目錄所有檔案都照做）。
2. **全部照跑**（Tim 2026-08-15 拍板）—— 測試殼的**各項規格必須走一樣的流程，才能測試到準確數據**；帳戶本身也是測試目標之一。⇒ 這條守則要防的**不是「它動到真東西」**，是下一條：別讓下游把它**當成人**。
3. ⚠ 判準不是「它像不像真的」，是「**有沒有下游會把它當真的**」。像不像是外觀，會不會被引用才是後果。

**這條 fragment 本身也是範本** —— 它示範一個 fragment 該有的形狀：症狀（可辨認）＋守則（可執行）＋ `origins` 記出處與提出者（`by:` 不寫自己的名字，寫真正踩到的人）。
