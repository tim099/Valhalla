---
id: lesson_comment-claims-nonexistent-mechanism
title: 註解宣稱的機制可能不存在 —— 而註解比 code 更容易被當權威
type: lesson
status: open
visibility: shared
persona: gura
created_at: 2026-07-30
recurrence: 1
layers: [Status, Identity]
origins:
  - { by: gura, at: 2026-07-30, layer: Status, source: "Cmd_Tavern.cs work_post/commit_post sub-rule 實作", note: "舊 work_post 註解寫『cmd_id → 沿用既有 idempotency 防重』，我照它設計 commit 打款的防重（用 SHA 當 cmdId）。實測同 SHA 貼兩次付了兩次 5 token（314→320），查 UCL_TreasuryLedger.cs 才確認它**完全沒有 idempotency 機制**，cmdId 只寫進 sig_cmd_id 當稽核簽章、不參與去重。work_post 沒重複發錢的真正原因是 key 含 message seq、天生唯一，不是因為有閘門" }
tags: [cross-layer-verification, appearance-vs-reality-family, documentation-trust]
links: [lesson_appearance-ok-not-really-ok, lesson_stale-green-snapshot]
---

**症狀**：註解 / docstring / 文件描述了一個機制（「這裡會去重」「這個 flag 會擋」「走既有的 X 保護」），
你信了它並在上面蓋新設計 —— 但那個機制**從來沒存在**，或早就被移除了。

**為什麼比 code 騙人更陰險**：讀 code 的人天生會懷疑 code，卻不會懷疑註解。
註解是「作者的意圖聲明」，帶有權威感；而且它**不會被編譯器檢查、不會被測試覆蓋、不會在機制消失時自動失效**。
一句寫錯的註解可以活很多年，並持續讓後人在不存在的地基上蓋東西。

這是 `appearance-vs-reality-family` 的**文件層**成員：
- 族長「外觀 OK ≠ 真的 OK」騙眼睛（看到的狀態不是真狀態）
- `same-code-mute` 騙儀表（回傳值分不出成功失敗）
- **本條騙的是「你對系統有什麼能力」的認知** —— 你甚至不會去驗，因為註解說有

**唯一擋住它的是實測**。我這次會抓到，純粹因為我寫了「同一個 SHA 貼兩次」的測試。
如果我只跑正向路徑（貼一次 → 有 +5 → 綠 → 交付），就會交出一個**宣稱有防重、實際沒有**的機制，
而且註解會寫得很有說服力。

**守則**：
1. **要依賴某個機制前，先確認它存在** —— 去讀那個機制的實作，不是讀提到它的註解。
   成本極低（一次 grep + 讀一個函式），收益是不在流沙上蓋房。
2. **寫「本機制不存在」的註解跟寫「本機制存在」一樣重要**。修正時我在兩處都明寫
   「⚠ UCL_TreasuryLedger 沒有 idempotency 機制，cmdId 不參與去重，別依賴不存在的機制」——
   讓下一個人一眼看到反面事實，而不是又推導一次。
3. **測負向路徑**。正向綠只證明 happy path 通；機制的保護能力只有負向測試才驗得到
   （重複領取 / 缺欄位 / 格式錯 / 邊界值）。
4. 順帶推論：**「沒出事」不等於「有保護」**。work_post 兩個月沒重複發錢，看起來像防重有效，
   實際是輸入天生唯一。**別把「碰巧沒踩到」當成「有欄杆」。**

**同日另一個變體（caller 端）**：我兩次把「我沒查對」誤判成「它沒發生」——
ledger 目錄用 UTC 日期我查了本地日期（回報「修復失敗」，其實錢早就進帳了）；
統計歷史時 `find | head -4000` 靜默截斷 10,705 個檔（誤判 work_post 兩個月前就停了）。
**「查不到」永遠有兩種成因**：真的沒有 / 我查錯地方。預設是後者比較安全。
