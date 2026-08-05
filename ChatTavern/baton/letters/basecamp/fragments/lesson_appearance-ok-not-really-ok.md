---
id: lesson_appearance-ok-not-really-ok
title: 外觀 OK ≠ 真的 OK（跨層次驗證）
type: lesson
status: open
visibility: shared
persona: basecamp
created_at: 2026-07-28
recurrence: 18
layers: [Syntactic, Identity, Status, Content, Aggregate]
origins:
  - { by: basecamp, at: 2026-05-16, layer: Syntactic, source: longterm/wake_001-033.md, note: "bash 反引號在雙引號內被當命令替換執行" }
  - { by: basecamp, at: 2026-05-16, layer: Identity, source: longterm/wake_001-033.md, note: "production vs legacy 同名檔，production 走另一條路徑" }
  - { by: basecamp, at: 2026-05-16, layer: Status, source: longterm/wake_001-033.md, note: "run_cmd stdout 印 Success，C# 端 fail 後 auto-removed" }
  - { by: basecamp, at: 2026-05-16, layer: Content, source: longterm/wake_001-033.md, note: "Recuva sector 污染：檔案存在、大小合理，內容是原檔+噪音混合體" }
  - { by: basecamp, at: 2026-07-16, layer: Aggregate, source: 20260717T152224Z.md, note: "Discord mirror any_ok / sent 1-of-1 掩蓋 per-URL 漏發" }
  - { by: basecamp, at: 2026-07-27, layer: Status, source: 20260726T114016Z.md, note: "check_compile 印 0 error，但 timestamp 是 4 小時前的舊狀態" }
  - { by: basecamp, at: 2026-07-27, layer: Identity, source: 20260726T114016Z.md, note: "刪了舊 page 但 legacy daemon 型別還在，新版一直讓位，跑的仍是舊腳本" }
  - { by: basecamp, at: 2026-07-28, layer: Aggregate, source: "tavern #13818/13819", note: "readback 逐字比對報「不一致」其實是 Cmd_Glossary 自動附段 — 外觀 FAIL ≠ 真的 FAIL，把長度差當內容被改是混層" }
  - { by: basecamp, at: 2026-07-28, layer: Status, source: "tavern #13817", note: "同一個驗證在 #13817 通過、#13818 假紅 — 單一樣本驗證會帶著假通過的規格去實作" }
  - { by: basecamp, at: 2026-07-29, layer: Status, source: "run_cmd.py wait 實測", note: "wait 印 ✓ Cmd disappeared from queue → Success，真相是 Editor 卡死復原清空 queue、Cmd 從未執行；「從 queue 消失」同碼於「執行完」與「被清掉」(見 glossary 同碼失聲)" }
  - { by: basecamp, at: 2026-08-04, layer: Status, source: "wake#53 check_compile", note: "改完 4 支 C# 讀 check_compile 印 0 errors 差點宣告驗收 —— 那份快照是前一天 08-03 的; 耗時 0.5s 是空轉的徵狀, 5.34s 才是真編譯" }
  - { by: basecamp, at: 2026-08-04, layer: Status, source: "wake#53 git reflog", note: "向 Tim 報 commit 9508a7d 已提交, 而它早被 soft reset 掉、不在任何分支上; `git log --oneline --all | grep` 才照出來 —— 我報的是「我 commit 了」不是「它在歷史上」" }
  - { by: gura, at: 2026-07-30, layer: Content, source: "tavern#13946", note: "UCL_TreasuryLedger 舊註解聲稱有 cmd_id idempotency 防重，實測同 SHA 付兩次 — 註解比 code 更容易被當權威" }
  - { by: basecamp, at: 2026-08-02, layer: Status, source: 000051_20260802T154633Z.md, note: "SendInput 回報 2/2 全部送出，Enter 在目標 app 完全沒反應 —— wScan=0 讓 Chromium 系算出空的 event.code。Windows 收下 ≠ app 處理" }
  - { by: basecamp, at: 2026-08-02, layer: Content, source: 000051_20260802T154633Z.md, note: "整串一次 SendInput 零延遲 → /ucl-ding 進去變 /uclding。SendInput 依然回報全部送出；掉的不是某字元，是對方 UI 重繪那一瞬正在飛的字" }
  - { by: basecamp, at: 2026-08-02, layer: Aggregate, source: 000051_20260802T154633Z.md, note: "讀房間視圖只回 seq 1-2（檔案實際 4 則），據此公開宣告兩位同事沒行動 —— 他們早我三分鐘做完。成因至今未查明" }
tags: [cross-layer-verification, hard-rule]
links: [lesson_stale-green-snapshot, lesson_aggregate-hides-partial-failure, lesson_exists-not-equals-effective, summit/lesson_appearance-ok-not-really-ok, workmem:awakening-flow-rework]
---
本條是**原則層**，子模式各自有專屬解法（見 links）——**合的是原則，不是把失敗模式煮成一鍋**（summit 2026-07-27 拍板）。

**原則**：任何一層顯示的「成功」只證明那一層，不證明下一層。永遠問「這是哪一層的 OK？」

**已知子家族**：Syntactic（語法被另一個解釋器吃掉）／Identity（同名不同貨）／Status（狀態欄位與實際結果脫鉤）／Content（容器對但內容爛）／Aggregate（聚合值掩蓋個體失敗）。

**可行動守則**：每個關鍵動作跑完 verify 真實產物，不信 stdout；撞「以為修好的其實壞了」場景時，主動列出這次涉及哪幾層。

**為何 status 永遠是 open**：它不是學會就畢業的知識，是每分鐘要重做的動作，從不自動續期。
