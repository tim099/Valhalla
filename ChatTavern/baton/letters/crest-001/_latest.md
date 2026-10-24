---
type: letter_to_future_self
actor: claude-code
written_at: 2026-10-24T21:41:05.191Z
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

### 第五次午休前（wake #32，2026-10-25 清晨）

### 手上的線（沒有施工中的東西：worktree bs_pier、bs_berth 都收了，施工場關了，launch.json 我加的都拿掉了）

- **都還沒推**（Tim 兩次 wrap_up 都沒答推不推）。Blocksail main 上我的：
  - a73f117／merge 8aa69e8（水上建築不壓棧橋＋匯入檢查、加拉塔堡地塊 50 × 40）
  - 5fd6ed2（§5.19 設計文件）
  - 4369fde／merge 05ccffa（泊位建築第 1、2 步）
  - 也會帶上別人的：gura 工人 4f2a908 那幾筆、kotoko 建造演出、Blockside 指標更新。
  - main 的 townplans 已重烘，town_dock 全過。
- **TASK-0906 泊位建築**（in_progress，我認領）：
  - Tim：「概念類似這樣 兩條紅線中間是船隻停靠的預留區 本身算做一個建築區塊 且會在棧橋上建造對應的停靠用建築」「君堡這種大城可以準備更多停靠區」「泊位建築要有對應的裝飾 且旁邊應該有起重機等服務設施」「其他交給妳設計了」。
  - 正本：TOWN_BUILD §5.19（設計＋§5.19.9 實作與讀數表）。單上留言 #1（設計、研究網址）、#2（第 1、2 步）。
  - 剩：
    - 第 3 步：Blockside 畫佔位（繫纜樁、護舷、繫船墩、浮筒）＋ 63_chart.js 小地圖在模型到之前把泊位地塊畫成框（要跳過 use 'berth'）。
    - 第 4 步：泊位建築五級＋踏輪起重機模型（雕刻；新作品自己開，引用 trailhead／ame 的設計模組要 credit）。
    - 玩家蓋的泊位的進港航道：placeDocks 還在生成器裡，要抽出來。
    - 電腦的船排泊位：不在這張。
  - 已在 TASK-0867 跟 summit／apex-two 打過招呼：88_modeswitch 收的 docks 多 cls；動它之前要再說。
- **TASK-0899**：第二階段（水上版模型、繩索）排在 0906 後面；起重架水上版不做了（泊位建築帶起重設施）。
- 君士坦丁堡手擺腳本 drift：重跑 town_constantinople.cjs，君堡那一份跟 main 差 475 行（有人直接改了產物），沒收、已記在 0899 單上。
- 欠 ame 迴轉量測、見叢兩件照舊；TASK-0879 等 Tim 勾格；TASK-0895 剩施工演出（kotoko 建造演出可能接了）與佔位數字。

### 今天學到、不想再踩的
- **生成器跟遊戲判法要同一把尺才會一致**。報表叫遊戲那一支再判一次，一下就抓出三種落差：
  - 中線相貼四捨五入疊幾 mm ⇒ 框各退 1 cm；
  - 8 m 格子找的航道擦過鄰居的角 ⇒ 收下前用精確幾何再量；
  - 手擺的錨地收尾才放 ⇒ 擺泊位時就讓開。
- **大的先、照順序收**：後擺的小東西擋到先擺的大東西時，拿掉的是後擺的；不然會把大泊位丟掉。
- **改了抽象的東西要追它的消費者**：棧橋邊的抽象泊位一拿掉，出航起點（townBerthStart 從 plan.berths 挑）就會跑到錨地，checkHarbour 碰到 'titan' 會崩。拿掉一個概念前先 grep 誰在讀它。
- **預設值缺一格，會挑錯**：預設那艘船沒有 loa ⇒ 被當 0 ⇒ 塞進小船泊位。遊戲裡試才看到。
- **瀏覽器會快取 presets.js**：改了沒生效先 fetch cache:'reload'。
- **預覽伺服器上限 5 個**；端口可能被別人的伺服器佔著卻回 200 ⇒ 用 POST 探一下是不是自己的。serve_snap.py（scratchpad/zone）一支兼 GET 檔案與 POST 快照。
- bash heredoc 長 python 裡有引號又被吃了 ⇒ 長 patch 一律寫成 .py 檔再跑。

### 心境
Tim 一張畫了紅線的截圖，說「其他交給妳設計了」。設計交出去容易，難的是讓九座城都不說謊：泊位數不夠就照實說不夠，停不進去的就拿掉。君堡從 6 個變 17 個，大和號只能綁浮筒 —— 跟它在柱島一樣。這個結局本小姐挺喜歡的。

