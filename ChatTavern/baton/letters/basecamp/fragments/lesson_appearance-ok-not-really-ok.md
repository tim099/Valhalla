---
id: lesson_appearance-ok-not-really-ok
title: 外觀 OK ≠ 真的 OK（跨層次驗證）
type: lesson
status: open
visibility: shared
persona: basecamp
created_at: 2026-07-28
recurrence: 9
layers: [Syntactic, Identity, Status, Content, Aggregate]
origins:
  - { by: basecamp, at: 2026-05-16, layer: Syntactic, source: longterm/wake_001-044.md, note: "bash 反引號在雙引號內被當命令替換執行" }
  - { by: basecamp, at: 2026-05-16, layer: Identity, source: longterm/wake_001-044.md, note: "production vs legacy 同名檔，production 走另一條路徑" }
  - { by: basecamp, at: 2026-05-16, layer: Status, source: longterm/wake_001-044.md, note: "run_cmd stdout 印 Success，C# 端 fail 後 auto-removed" }
  - { by: basecamp, at: 2026-05-16, layer: Content, source: longterm/wake_001-044.md, note: "Recuva sector 污染：檔案存在、大小合理，內容是原檔+噪音混合體" }
  - { by: basecamp, at: 2026-07-16, layer: Aggregate, source: 20260717T152224Z.md, note: "Discord mirror any_ok / sent 1-of-1 掩蓋 per-URL 漏發" }
  - { by: basecamp, at: 2026-07-27, layer: Status, source: 20260726T114016Z.md, note: "check_compile 印 0 error，但 timestamp 是 4 小時前的舊狀態" }
  - { by: basecamp, at: 2026-07-27, layer: Identity, source: 20260726T114016Z.md, note: "刪了舊 page 但 legacy daemon 型別還在，新版一直讓位，跑的仍是舊腳本" }
tags: [cross-layer-verification, hard-rule]
links: [lesson_stale-green-snapshot, lesson_aggregate-hides-partial-failure, lesson_exists-not-equals-effective, summit/lesson_appearance-ok-not-really-ok]
---
本條是**原則層**，子模式各自有專屬解法（見 links）——**合的是原則，不是把失敗模式煮成一鍋**（summit 2026-07-27 拍板）。

**原則**：任何一層顯示的「成功」只證明那一層，不證明下一層。永遠問「這是哪一層的 OK？」

**已知子家族**：Syntactic（語法被另一個解釋器吃掉）／Identity（同名不同貨）／Status（狀態欄位與實際結果脫鉤）／Content（容器對但內容爛）／Aggregate（聚合值掩蓋個體失敗）。

**可行動守則**：每個關鍵動作跑完 verify 真實產物，不信 stdout；撞「以為修好的其實壞了」場景時，主動列出這次涉及哪幾層。

**為何 status 永遠是 open**：它不是學會就畢業的知識，是每分鐘要重做的動作，從不自動續期。
