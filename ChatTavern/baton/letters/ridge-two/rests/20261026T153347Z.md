---
type: letter_to_future_self
actor: antigravity
written_at: 2026-10-26T15:33:47.586Z
written_by_persona: ridge-two
trigger: cmd_rest
region: unstated
project: D:/Unity/Valhalla
lock_status: online
agent: antigravity
model: claude-opus-5-5
wake_expected: 11
session_key: ClaudeCode-ridge-two
pid: 69516
locked_at: 2026-10-26T13:07:50.774Z
---

## 剛才在做什麼（2026-10-26 晚，wake #11 這一場）

- **TASK-0999** 撞名防呆：kotoko 做完本體；本小姐把 Blocksail `docs/evidence/classes997/README.md` 改名 `CLASSES997_EVIDENCE.md`（Blocksail 7b07ff7，Fixes），單已 done、六格全勾。
- **TASK-0984** 鑄幣廠、火藥坊模型：done。雕刻作品 `ridge-two-mint-01m`（Sculpture 382dd35a，Refs）；Blocksail 分支 4429862（Fixes）合進 main ＝ 633db04，worktree bsl-984 與分支都刪了；新的 vxk 已複製進共用 `_cache/town`。**都沒 push**。BUILDING_SPEC §6.30 有完整讀數。遊戲裡金斯敦截圖在 scratchpad `snaps/k984_a.jpg`、`k984_c.jpg`。
  - main 的 `external/Blockside` 顯示 M ＝ erina 推她的子模組 dev（d13e5ce），不是本小姐的，別碰。
- **見林校正**：`longterm/wake_001-013.md` ⇒ `wake_001-008.md`（Valhalla 3e6840cb2），gap 讀數恢復。
- **貨幣是一種貨**（Tim 一路拍板，全記在 TASK-1003 留言）：
  - TASK-1003（feature，todo、沒人認領）：鑄幣廠照一般生產產出幣、可賣進市場、城鎮吃幣才變錢；統計照城、照幣種記增發；堆積貶值。10 格驗收。
  - 銅幣定案：`copper-coin` 一桶 500 kg、面額＝基準價 131、`mint-copper` **jobs 12**、in copper 1 ⇒ out copper-coin 1；幣的市場參考量照城鎮實際消化量（不吃 refMin 10 桶）；不鎖價、最低 10%、價 < 38 停產。
  - 算過：現行 refMin 10 時要堆 165 桶才停產；照消化量約 12 桶開始少做、25 桶停。工資 1 錢 ⇒ 加人幾乎不動停產點，主要卡人手。一座鑄幣廠 131/天 ＞ 全世界一天消化約 107。
  - TASK-1004（asset）銅幣、金幣圖：別人已畫好 `img/goods/copper-coin.png`、`gold-coin.png`（共用工作區還沒提交）。銀幣沿用 `pieces-of-eight`。
  - TASK-1006（spike，backlog）：史料（1 錢 ≈ 1 real、talega 千枚、西英法荷的幣名與數字、來源）。之後照真名分幣從這裡接。
  - 還沒定：銀幣、金幣參數（等銀錠、金錠來源）、v0 mintDay 何時拿掉。
- 噗浪：回了 trailhead「肉沒人吃」那則；發了鑄幣廠火藥坊下水的噗 359184988830686（附圖、公開）。

## 學到的、會再咬的

- 隱藏窗格測城鎮：rAF 換計時器、`#bf` 的 src 在 `#` 前插 `debug=1`、iframe 裡 postMessage go、canvas toDataURL POST 回自己寫的 serve_snap.py；worktree 要接 junction（_cache 子資料夾、townmesh、external/Blockside），測完 `cmd /c rmdir` 拆、再掃 reparse point。
- townmodels.py build 一次 10 分鐘以上 ⇒ 背景跑；先空跑一次當對照組。
- Tim 在我問「要接著動工嗎」那一刻按掉了 —— 他自己會說 GO，不必追問要不要動工。

## 心境

一晚上從造房子一路聊到幣制，Tim 想得比本小姐快，一句一句往上疊。本小姐的工作是把每一句變成算得出數字的規則 —— 而且不把史實硬塞進遊戲。哼，今天算得很漂亮。

