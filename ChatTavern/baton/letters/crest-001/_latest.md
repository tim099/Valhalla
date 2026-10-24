---
type: letter_to_future_self
actor: claude-code
written_at: 2026-10-24T16:42:27.027Z
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

### 第四次午休前（wake #32，2026-10-25 凌晨）

### 手上的線（沒有施工中的東西：兩個 worktree、預覽伺服器、截圖收件伺服器、施工場都收了；launch.json 的 crest-water、crest-snap 已拿掉）
- **TASK-0899 水上建築**（in_progress，claimed）—— 第一階段已合進 Blocksail main 3146da7、Blockside dev 4146e78，**都還沒推**（等 Tim；wrap_up 問了推不推，他還沒答就叫午休）。
  - Blocksail：8cdcab1（主體）＋ fab67f1、b9f4801（文件）＋兩次合 main（df663c0、3146da7）。Blockside：73975c4 ＋兩次合 dev（246b260、4146e78）。
  - 推的話會帶上別人沒推的：Blocksail c462aa2（meadow 農莊模型）、96c5fc0（圖示）、afab61b（workers901 文件改名）；Blockside dev 只有我的三筆。
  - 地球儀的規劃已在 main 重烘（town_bake，五座都換）。
  - 正本 TOWN_BUILD §5.18（規則、讀數表、第二階段待辦）；單上留言 #4（開工、第 3 題）、#5（第一階段判定與憑據）。
  - Tim 拍板：第 3 題 ⇒「可以有下水演出(但先不急著做) 保留規格」；「報表的判定code可以跟遊戲共用一部份嗎」⇒ 報表呼叫 BSW.townWaterFit（遊戲那一支），town_check 留另一把尺。
- **第二階段（等 Tim 說開工）**：五種水上版模型（現有的 trailhead 起重架、船棚是正面 y 0 朝水做的 ⇒ 水上版要反過來，出入口與船台朝背面；ame 的船廠、修船碼頭在 ame-carib-civic-01m）＋建築的繩索（雕刻 rig.ropes ⇒ townmodels.py 帶出 ⇒ Blockside 城鎮畫繩；建築不動，可能不需要船那種 ropebind）。施工演出、下水演出另外。
- **剛報給 Tim、還沒答**：加拉塔多了一對房子互疊 3.8 m²（kastellion 模型比地塊大、往外溢 10 m，開場農莊換位置後貼過去）。我傾向修「農莊挑位置照模型實際外框」，那是 kaguya／meadow 的範圍 ⇒ 問 Tim 要我修還是記單交給她們。
- 另外記在單上不在射程：金斯敦 farm-vegetables-9 放回原位被判跟 farm-cassava-9 的田疊（town_check 量是邊貼邊）——試放與田的容許差。
- TASK-0895（分區）照舊：剩施工演出與佔位數字。TASK-0879 等 Tim 勾格；欠 ame 迴轉量測、見叢兩件照舊。

### 今天晚上學到、不想再踩的
- **一條 python 改好幾處，中途 assert 失敗，後面的指令照跑**：我把改文件、git add、commit 寫在同一個 Bash 裡，python 在第二處對不上字串就停，commit 還是落地了（8cdcab1 帶著「七座都一樣」的錯句），只好補一筆。多步改檔後面接提交 ⇒ 用 `&&` 串、或分兩次呼叫先看結果。
- **寫讀數前先真的量**：差點把「主控台沒有錯誤」寫進文件，回頭讀才發現沒看過；看了是只有 worktree 缺烘焙檔的 404。「泊位七座都一樣」也是只比了七座裡的五座就寫。
- **反向對照的搬法要考慮棧橋**：報表的已知答案「往正面推一個進深」，棧橋旁的推過棧橋還是水 ⇒ 0 ⇒ 0。改成搬到陸上一棟住宅那一點。
- **合 main 前 main 會一直動**：一晚上合了兩次 Blocksail main、兩次 Blockside dev（meadow 的 townRecipe 也改 townPick）。town_foot 已經改成順著呼叫一路往下抽（kaguya），新 helper 不用再手補。
- 隱藏窗格開航海：place 船之後 `__globe.battleIn('sail')`，iframe src 有了就加 &debug=1、postMessage go；小地圖在航海模式才開，canvas 在 #chartBox。

### 心境
Tim 一句「899 開工」，從格子帶一路做到遊戲裡的木樁。半路他問報表能不能跟遊戲共用判定 —— 問得好，本來兩份各寫各的，改完之後改一處兩處都動。寫讀數的時候被自己抓到兩次「還沒量就先寫」，下次先量。

