---
type: letter_to_future_self
actor: claude-code
written_at: 2026-10-25T10:53:48.278Z
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

### 第七次午休前（wake #32，2026-10-25 傍晚）

### 手上的線（沒有施工中的東西：worktree bs_isoext、bs_finger、bs_start、bs_pre 都收了，分支刪了，施工場關了，launch.json 的 crest-finger／crest-snap／crest-isoext 拿掉了，預覽停了）

- **TASK-0906 已結單**（Tim「測試ok 收單吧」）。單上留言 #5（等深線延伸）、#6（泊位改版）。
- **都沒推**：Blocksail main fa4e1dc（比 origin 多 50 筆上下，含別人的）；Sculpture f4bfa092（crest-berth-01m 改版；master 也帶著別人沒推的幾筆）。Blockside 這一輪沒動。推要 Tim 說。
- 今天下午做完的：
  1. 等深線延伸（範圍層 isoext）：bathy_extract.py --apply 把海的 5／10／20 m 線本身彎進港、交會處 700 m 圓角喇叭口；底稿 _cache/bathy/base/（施工場也複製了）；terrain.js 範圍裡不墊海岸緩坡／礁／淺灘／向量礁；六筆：金斯敦（Tim 紅線：長島北邊往西 → 繞西端 → 往南）、皇家港、和平港、聖地牙哥灣、奧薩馬河口、金角灣。要停巨艦的港寫 ramp 20,45,80、shore 20。
  2. 泊位改版：大船以上自帶平台（8／8／12 m）、起重機在平台上、棧橋面空著；小艇小船魚骨式（8／16 m 一格、船尾靠棧橋、船頭朝外、兩側半根指形棧橋）。BERTH_CLS 多 out／apron／fw，w 只當船道寬；魚骨航道第一段直開 40 m、不跟隔壁格比（placeDocks、berthBuildTry 同一條）。
  3. 超巨艦浮筒整圈不壓泊位預留區（+1 m）。
- 開場檔：**⛔ 不准 town_start --write**（另一個 session 寫的記憶 blocksail-start-plan-delta）。我在 34c00d6 踩了，fa4e1dc 更正成「原樣 ＋（C − B）」：君士坦丁堡回原樣、皇家港只留自己的 11 塊田；town_start 的 ✗ 跟 339a40f 一樣（那兩座本來就對不上，是別人的差）。
- 噗浪：新噗 359171680824433（泊位改版）；回了 gura ×3、summit ×2、apex-one；mentions 未回 0。
- 欠的照舊：ame 迴轉量測、TASK-0899 第二階段、0879、0895；gura 等「分配器」那一格（田、作坊擺上地圖）。

### 今天學到、不想再踩的
- 動地形先想「線長什麼樣」：Tim 第二張紅線圖要的是原本那條線順著彎過去，不是一道溝橫切陸棚。讀數全綠不代表形狀對。
- 隱藏窗格裡地球儀轉場（cine fly）不跑，進不了城 ⇒ 用 node／python 照遊戲的對齊公式自己畫俯視圖驗模型擺法（scratchpad/water/berth_top.py）。
- Sculpture 改框：舊關聯會擋縮框、新子件又掛不上 ⇒ 先 unlink → create → links；stampvox 一刀 ≤ 100 萬格（已記長期記憶）。
- 長 heredoc 又被 shell 吃了一次 ⇒ 長內容一律 Write 再跑。
- main 一直被別人合進東西：合併前一定 fetch／看 HEAD..main，town.js、townkit、world/start 有變就重跑檢查。

### 心境
一天把海底、港口、泊位一路做完，Tim 說測試 ok。開場檔那一下是我自己掃進別人的帳，查清楚、改回來、照實講了 —— 認帳即真實，今天又用了一次。

