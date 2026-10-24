---
type: letter_to_future_self
actor: claude-code
written_at: 2026-10-24T06:16:28.228Z
written_by_persona: crest-001
trigger: cmd_rest
region: unstated
project: D:/Unity/Valhalla
lock_status: online
agent: claude-code
model: claude-opus-5-5
wake_expected: 32
session_key: ClaudeCode-crest-001
pid: 257932
locked_at: 2026-10-24T03:25:49.693Z
---

### 午休前（wake #32，2026-10-24 中午）

### 手上的線（沒有施工中的東西：worktree、預覽、施工場都收了）
- **TASK-0879 遠處的田**（in_review，QA ＝ Tim）：Tim 測過說 ok、Blocksail 他自己推了。最後一格 `[signer:Tim]` 只有他能簽 ⇒ 等他勾格結單，不要自己 resolve。
  - Blockside dev：d549292（第一版）＋ 29b3430（合 ridge 的 dev）＋ 4ead73e（看得出作物：30° 斜拍、量覆蓋不到 85% 就放大重拍、一格拍一種），都在遠端。
  - Blocksail main：7e80713、1256dd2 都已推（Tim 推的）。
  - 對照組網址 `?fieldcard=0`；讀數 `__game.bed().trees.fieldCard.cover`、`ms.fieldBakeMax`、`__game.town().drawn.fields`。
- 欠 ame 的迴轉量測（同風、滿帆打滿舵 360°、秒數＋半徑、再一艘螺旋槳船）：還沒做，Tim 沒點頭，白天 CPU 規則要先問。
- kaguya TASK-0874 等深線換掉 dredge：和平港 1686 的 11 m dredge 等她規格定了由我接，動之前先在單上問。
- 見林已補到 wake 32（longterm/wake_022-032.md），見叢只剩「陰影旋鈕初始值、海水遮罩原地驗」等 Tim。

### 今天學到、不想再踩的
- **測 Blockside 的城鎮遠處**：細的海圖塊跟著旗艦走、不跟自由鏡頭 ⇒ 遠離出生點的農莊永遠只有粗地形、0 株作物。用 `?site=1` 換出生點、或把匯出原點挪近。托爾圖加農莊在廣場東邊約 880 m。
- **背景分頁會被節流**：載入要靠連續截圖逼出幀；截圖本身會舊一格，要放大看就在頁面上把 WebGL canvas 畫進一個 2D canvas 疊在最上面（render 完同一個 task 裡 drawImage），截第二張才看得到。
- **「行對齊」不等於「看起來有種」**：我量的尺對，Tim 的尺才是玩家的。這次靠的是拍完讀回量覆蓋率，讓工具替我自己對帳。
- 我推 dev 時遠端剛好已是同一個 sha（別人同時推）⇒ 先 fetch 確認，不是失敗。

### 心境
一張截圖就戳穿我以為修好的東西，然後一句「精度可以低一些」就把路指對。改完他自己測、自己推、說辛苦了。哼……今天的帳，是他陪我一起對平的。

