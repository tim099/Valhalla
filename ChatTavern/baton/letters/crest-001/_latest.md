---
type: letter_to_future_self
actor: claude-code
written_at: 2026-11-02T15:48:47.570Z
written_by_persona: crest-001
trigger: cmd_rest
region: unstated
project: D:/Unity/Valhalla
lock_status: online
agent: claude-code
model: claude-opus-5-5
wake_expected: 34
session_key: ClaudeCode-crest-001
pid: 2160
locked_at: 2026-10-31T07:12:59.583Z
---

### 第五次午休前（wake #34，2026-11-02 深夜）

### 手上的線

- **TASK-1105 演出物件：已結單**（下午）。
  - 格 1、2、6 量完。
  - 格 8：Tim 看截圖說「可以 簽吧」，本小姐用 persona=Tim 代簽、留言 #5 註明。
  - 單上留言 #4 有全部讀數。
- **拿掉城鎮時空分組＋船隊航程上限**：都在 Blocksail main，**沒推**（推要 Tim 點頭）。
  - 由來：Tim「時空分組 這個不用」「君堡可以跟其他城市通航」「城鎮時空目前單純是演出(不影響城鎮功能以及貿易)」；讀數出來後選「船隊航程設上限」。
  - 本小姐的四筆：
    - d9e5087a：fleet.js 不分 spaceOf；nav_bake／nav_net／nav_stale 一組；navGraph 找不到海路、旁邊 10 km 有港 ⇒ split noRoute；fleet_check 三條已知答案。
    - 789c7852：合 main（里斯本）＋航線快取重烘。
    - 7a9f8bf4：航程上限照去、回兩個方向（inReach），母港一定回得去。
    - 7165957f：合進 main。
  - 讀數：
    - FLEET.maxDays 200：加勒比內部兩個方向最長 160 天，不切；跨大西洋去 58～229、回 267～367 天 ⇒ 擋。
    - 里斯本 ⇄ 加的斯 ⇄ 君堡（16～176 天）照通。
    - fleet_check 103 條全過。
- **TASK-1160 加的斯**（in_progress，我認領）：每一步都做完了，**還沒提交**。
  - 位置：worktree scratchpad/bs-1160（分支 crest/1160-cadiz，基底 main 789c7852 之後又合了 7a9f8bf4 那一筆；改動都在工作區、沒 stage）。
  - ⚠ git stash 裡還留著一份「cadiz wip」（stash pop 之後沒自動丟），確認不需要再 drop。
  - **等 Tim 決定**：港口點 [-6.28, 36.535] 離市中心 1.3 km ⇒ 中心城區沿灣長成「兩道牆夾一條走廊」（PITFALLS 第一條鑰匙孔）。
    - 選項：挪到舊城東北的岸邊（海門外），讓城緊湊；要重做 harbour_deep、規劃、dock、開場檔、nav，約 2 小時。
    - 或照現在提交。
    - 截圖給 Tim 了（cz_town_core／port／wide／globe，在 scratchpad/m1105/out）。
  - 做了什麼：
    - 岸：OSM（Tim 同意）、tools/cadiz_shore.py ⇒ coast cadiz-cut-1～11、fill-1～6；NEAR 框 (-6.345,36.445,-6.17,36.6)。
    - 局部等高線：relief_rings.py 加 cadiz（Tim 同意下載 terrarium 10_493_400、10_494_400，放共用 _cache/terrain-raw/tiles10）。
    - 港：lines cadiz 12 m、goal 14。
    - 範圍：world/areas/cadiz.js（從 europe.js 改名，照里斯本 lisbon.js 一城一檔）；seed 2669556159、hash 33704f0f69f9ac9a。
    - 城區三區；開場檔 ＋ opening 39 座（有釀酒坊、鹽田）。
    - nav：ports／net／graph 都烘了，接里斯本、君堡、瓜德羅普。
    - 一年模擬：物產都 > 0（葡萄酒 1,226、鹽 2,810）。
  - 單上留言 #1 是做到一半時的進度。**提交前要再寫一則**：最後的讀數＋遊戲裡截圖。
  - 照實留：
    - 城牆角露縫 4～9 個（六個種子都有）。
    - town_districts --check 在 main 上本來就 ✗（「districts 不是最後一欄」，不是加的斯）。
  - 合 main 時要重做的：bathy 照新表 --apply ⇒ 還原漂移 12 檔 ⇒ splice index。
    - 拼法：scratchpad/cz/splice_index.py <HEAD 的 index> <新跑的 index> <輸出> cadiz ean32-5 --relief。
  - worktree 的 _cache/bathy/base 已含 ea* 底稿。
- 噗浪：
  - 新噗 359262497964331（君堡通航＋加的斯圖）。
  - 回了 basecamp（巧克力）、erina ×2、ridge-001（里斯本）。
  - mentions 未回 0。
- 量測架 scratchpad/m1105：P2.sh／shot2.sh 是 9586／8836 那一套（伺服器根 = 加的斯 worktree）；現在都停了。

### 這次學到、不想再踩的
- **nav_net.cjs 自己在每條邊的指紋裡**：改這支一個字 ⇒ 全部邊重新細修，一個多小時；第一次設 58 分鐘逾時被跑爆。改它之前先想「值不值得整份重烘」；之後增量就快（14 分鐘）。
- **上限只量一個方向等於沒量**：信風讓航程不對稱（往西 60 天、往東 300 天）。設任何距離、時間上限都要問「回得來嗎」。是加的斯的木薯露餡才抓到的。
- **我寫的已知答案自己錯了兩次**：加拉塔照規則本來只配雙桅帆船；250 天 × 150 km 比半個地球遠，經度繞回來反而近。測試的世界也有它的物理。
- **「慢到沒人會挑」是沒量就寫的句子**：寫進文件之前先跑模擬，一跑就是 14 支船隊。
- 地圖上 0.2 m 的平地會讓生成器整條路斷掉（cpass > 0.3 m）；先量範圍裡陸地的高度分布。
- Cádiz 的 OSM 岸是一整條開的鏈，封口往陸地那一側（東）接；1666 年要拿掉的填海分三種處理：開運算、不補、窄口照史料留岬。

### 心境
一張城鎮單，半路變成拆掉整個時空的分組。Tim 一句「城鎮時空只是演出」，本小姐就順著拆，結果拆出一年才回得來的商船。先問一次、量一次、再改一次，帳是平的。加的斯長得像走廊這件事，本小姐自己看圖就覺得不對；照實說、不硬交，讓 Tim 選。

