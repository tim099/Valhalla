---
id: lesson_appearance-ok-not-really-ok
title: 外觀 OK ≠ 真的 OK（跨層次驗證）
type: lesson
status: open
visibility: shared
persona: summit
created_at: 2026-07-28
recurrence: 12
layers: [Syntactic, Identity, Status, Content, Aggregate]
origins:
  - { by: summit, at: 2026-05-16, layer: Status, source: longterm/wake_001-021.md, note: "stdout 印 Success 但 C# 端 fail 後 auto-removed" }
  - { by: summit, at: 2026-05-16, layer: Content, source: longterm/wake_001-021.md, note: "balance_after 是 cache 非真相, 重放才權威" }
  - { by: summit, at: 2026-05-16, layer: Identity, source: longterm/wake_022-031.md, note: "髮色 != 身份, OCR 字幕才是 ground truth" }
  - { by: summit, at: 2026-07-17, layer: Content, source: 20260717T151842Z.md, note: "STT 沒露餡不等於修好, 換無關新片舊片人名幻聽立刻現形" }
  - { by: summit, at: 2026-07-24, layer: Status, source: this-session, note: "check_compile 印 0 error 是改動前的舊 timestamp, recompile 才是真編譯" }
  - { by: summit, at: 2026-07-27, layer: Aggregate, source: this-session, note: "驗 gura WriteService: uuid 像撞其實是 13750 筆的生日悖論, 檔名 ts+uuid 仍唯一, 沒喊狼" }
tags: [cross-layer-verification, hard-rule]
links: [basecamp/lesson_appearance-ok-not-really-ok, lesson_report-the-ugly-true-number]
---

**症狀**：任何一層顯示的「成功」只證明那一層，不證明下一層。stdout 的 Success、狀態欄的 ok、compile 的 0 error、pip 的 rc=0 都可能跟真實產物脫鉤；反向也成立（外觀 FAIL 不等於真的 FAIL，start 被 reject 卻其實建了場）。

**可行動守則**：每個關鍵動作跑完 verify 真實產物，不信 stdout。撞「以為修好的其實壞了」時，主動列出這次涉及哪幾層（語法/身份/狀態/內容/聚合），逐層查真實落點。像 gura WriteService 那次——先辨「這是統計現象還是真 bug」再下結論，別急著喊狼也別急著放行。

**為何 status 永遠 open**：這不是學會就畢業的知識，是每分鐘要重做的動作，從不自動續期。跟 basecamp 那條同構，peer link 互指。
