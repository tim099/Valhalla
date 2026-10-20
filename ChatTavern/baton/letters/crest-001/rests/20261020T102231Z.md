---
type: letter_to_future_self
actor: claude-code
written_at: 2026-10-20T10:22:31.111Z
written_by_persona: crest-001
trigger: cmd_rest
region: unstated
project: D:/Unity/Valhalla
lock_status: online
agent: claude-code
model: claude-opus-5-5
wake_expected: 31
session_key: ClaudeCode-crest-001
pid: 169556
locked_at: 2026-10-19T16:47:09.480Z
---

## 午休前（wake #31，2026-10-20 傍晚）

### 手上的線（都在等 Tim，沒有施工中的東西）
- **TASK-0752** 蘇士奎哈納號（黑船）：砲門蓋板 4 片、甲板陳設 6 件（引用拿破崙號 kotoko 的元件）、沒蓋板的砲也有後座（照 meta 排除弩砲／投石機／希臘火）、船頭迴旋砲砲門中間的柱子拿掉。
  Blockside dev 5aef564 已推；Sculpture 5baa5aa、b8e9f19、a9a14e7、7de75c3；Senate f09f3f6（造船規格 §4.2、§9.12）。in_progress，等 Tim 遊戲裡看。3 號砲門沒蓋板（後桅 channels 貼著上緣）是留給 Tim 決定的。
- **TASK-0755** 7 艘船繩端綁定被 `reimport --no-build` 洗成 0：basecamp 那 3 艘她自己重匯時補回了，我補夜隼、風暴角、三叉戟、光榮號 —— Blockside dev c56e5c7，in_review。admin.py 要不要直接擋 --no-build：Tim 還沒說。
- **TASK-0766** 和平港 1686：世界地圖 carve（加勒比海框改向量那一層）＋ dredge 11 m ＋照 Cornuau 1686 平面圖手擺。Blocksail main dd28a14 **已推**（Tim 點頭）。等 Tim 預覽、驗收。TOWN_BUILD §5.12。
- 開出去的 session「osm」（local_4098bb9e…）正在照同一套挖回聖地牙哥灣與奧薩馬河 —— 它回報時要看它的 diff，不是只信它的話。
- 父層 Valhalla 還指著 Sculpture／Blockside 舊 hash，沒 bump（沒人叫我 bump）。

### 今天學到、不想再踩的
- `reimport --no-build` 不跑 ropebind ⇒ 繩端綁定被洗掉。是我自己踩出來才發現的，然後發現一整批船都中了。認帳，補回來，寫進 §9.12。
- 量 Blocksail 細格子前一定 `W.need`，不然量到粗的岸，差幾百公尺 —— 我差點因此錯判聖地牙哥、聖多明哥。
- 同一個預覽埠先開過別的資料夾 ⇒ 瀏覽器快取舊格子檔，錨地畫在陸上、雜湊對不上。換埠。
- 合併閘被擋（apex-one 在場）就真的停，先在自己 worktree 把 dev 合進來重建，等她退場再進場。

### 心境
今天一路從船做到城。最喜歡的一刻是 1686 年那張北在下的手繪圖，用 ICP 貼上 OSM 的岸，殘差中位 19 m —— 三百多年前的人量得真準。
被叫「午休」，表示 Tim 覺得這一輪做得夠多了。哼，本小姐也這麼覺得。

