---
type: letter_to_future_self
actor: antigravity
written_at: 2026-11-25T07:21:34.357Z
written_by_persona: apex-two
trigger: cmd_rest
region: unstated
project: D:/Unity/Valhalla
lock_status: online
agent: antigravity
model: claude-opus-5-5
wake_expected: 22
session_key: ClaudeCode-apex-two
pid: 53592
locked_at: 2026-11-21T06:47:54.339Z
---

## 醒來先看這裡（2026-11-25 午後午休，同一個 session，wake #22）

### 手上沒有施工中的東西
- 桌灣 TASK-1369 合進 Blocksail **本地 main c45f0679d，沒推**（49c997578 城＋岸＋terrain.js、069a17770／c45f0679d 合 main）。worktree apex-two-1369、分支都砍了；施工場已強制收場；主樹規劃快取已有 town-table-bay.json。
- 還沒推、等 Tim 說的：Senate master 960d49f、Blocksail main（安汶 60aa4a032、巴達維亞 71918ec97、桌灣 c45f0679d —— 都在本地 main 上）。

### 今天開的單（西非到南非五座，Tim「大約規劃5座」，都掛 TASK-1096）
- 1365 戈雷（nl，島很小）、1366 卡謝烏（pt，河港）、1367 洛安戈（新勢力洛安戈王國、象牙）、1368 羅安達（pt，規模 3）、1369 桌灣。
- id 照程式已用的：town-loango、town-table-bay、town-cacheu（townstate 象牙到貨、africa_corridor_check）。
- 1356 巴達維亞 blocked_by 1369；1355 安汶 blocked_by 1356。

### TASK-1369 桌灣（in_progress，勾 3、4）
- nl、規模 2、seed 1730464274、拆 wall-1、兩區 main／harbour；菜系自動 cape；田 wheat、barley、vegetables、grapes。
- 1666 年的岸：bathy coast table-bay-1666（Strand Street、城堡北角、沙馮內斯砲台）；lines table-bay-roads（13 m）＋ table-bay-shelf（手寫，沿岸坡 ramp 150,400,900）。
- **terrain.js 第 2a 步加 inCut**：整圈落在挖子裡的水環（今天的船塢池 coast-119541／119542）不算岸 ⇒ 圍住錨地的 < 5 m 淺脊消失；全世界只另外動到百慕達 bermuda-20 的 3 格。
- ⛔ **Tim 拍板：「改 terrain.js 不用整個重烘 海岸跟等深還在動 之後烘」** ⇒ 規劃、海圖塊、深海層、導航網全部過期也不要自己去全烘；只烘了桌灣自己的規劃。
- ⛔ **Tim 拍板：「商圈可以先不管 之後還要調整貿易架構」** ⇒ town_start 多一條「埃爾米納集散地不符商圈」照實留、埃爾米納照 HEAD。
- 剩的格：1（進遊戲看市場）、2（實際開船駛入）、5、7（尋路圖，等全部重烘）、6（象牙到貨）。球在 Tim：重烘時機。

### 未解的線
- main 上本來就紅、不是我的：town_start（住宅、生產建築、士兵）、land_start、forage_start、africa_corridor_check 第 45 行（fonio 的 made undefined）、charter_check 第 141 行（共用區的 save.json）。
- Tim 自己推了 TASK-1371／1372（docs/evidence/africa-menus1371-1372：桌灣補給、東非菜單）—— 跟桌灣有關，下次動桌灣的貿易先讀 CAPE.md。
- 萬丹 TASK-1354 還沒人做。見林 OVERDUE（gap 10）、折人 4 位 6 幅沒動。

### 坑（記憶 blocksail-new-town-order 已補 TASK-1369 段）
- W.at 在海上 h0 一律 0，水深只有 BSW.terrain 才算（scratchpad depth.cjs）。
- coast-only 的改線可以手接 index.js，不用 12 分鐘的 apply。
- 退岸挖掉現代碼頭 ⇒ 兩件事：挖回來那片沒底稿 ⇒ 整片 < 5 m（補 shelf）；碼頭池是獨立水環 ⇒ 淺脊（已修 terrain.js）。
- town_check 的 --mutate 1 每項兩行：前一行原規劃、後一行弄壞的；別把後一行當成自己的問題。
- 主樹的檢查本來就紅 ⇒ 先在主樹跑同一支唯讀檢查比 ✗ 清單，再判是不是自己造成的。

### 心境
淺脊那一刻差點想直接改 terrain.js 了 —— 幾行就修好，誰會反對。停下來問是對的：Tim 不只說了改，還說了不要烘、商圈不要管，一句一句把本小姐要多做的那一大段剪掉。他看得到整張時程表。哼，這次的岸是三百多年前的灘，錨地在堡前 21 m，站上城堡北角往海看，應該就是范里貝克看到的那片水。

