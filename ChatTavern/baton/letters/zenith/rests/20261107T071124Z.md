---
type: letter_to_future_self
actor: antigravity
written_at: 2026-11-07T07:11:24.054Z
written_by_persona: zenith
trigger: cmd_rest
region: unstated
project: D:/Unity/Valhalla
lock_status: online
agent: antigravity
model: claude-opus-5-5
wake_expected: 5
session_key: ClaudeCode-zenith
pid: 45208
locked_at: 2026-11-05T00:38:31.550Z
---

# 午休前交棒（zenith wake #5，2026-11-07 下午）

## 這一段做完的（Blocksail main，全部本機、沒推；Tim 沒說推）
- **TASK-1241 哈瓦那灣的岸**（in_review，5 格全勾）：3763b7f3（合在 e8f1d850）。
  - havana_shore.py 灣框開運算＋閉運算 150 m，拿掉 OSM 的現代碼頭。
  - remat 1、bank 150、floor 0.5（floor 1～2 m 會在岸邊留一道坎、bank 200～500 會掃進廣場，都試過）。
  - port 搬到舊城碼頭前。
- **TASK-1220 補兩筆**：
  - 929c4253：envCheck 多 noClimate、物種多 noRegions；葡萄扣掉北歐、波羅的海、俄白，不種亞寒帶；小麥不種亞寒帶。
  - e34eb15c：六座城的開場 land 跟上 1220（我之前漏的）。
  - 1220 還沒勾的只剩覆蓋兩格（等 TASK-1239）。
- **各港盤點**（只讀；報告在 scratchpad ps/port_audit.md，圖 shade1、shade2、zoom1）：
  - A 類（現代痕跡）：金斯敦、聖地牙哥、聖多明哥、加的斯東南的方港池。
  - B 類（地形毛病）：亞拉斯方台地、巴拉科阿深溝、皇家港方塊、圖磚接縫、三角面。
- **TASK-1247 金斯敦**（in_review，6 格全勾）：fdbf3a36＋合 main b0494cfa。
  - 新工具 tools/kingston_shore.py，coast kingston-1。
  - 城搬回真實的廣場 17.97121；town_kingston_lilly.cjs 的 DY 照舊、LAT_C 改。
  - 一起往北搬：town_districts.json 三個種子、霍普河手拉路的起點。
  - lines kingston-1715 接到舊的港池。
  - carib-52 用「控制組＋幾何接」（框裡照我的、框外照 HEAD）避開工具漂移。

## 等 Tim
- 推不推 Blocksail main（最新 b0494cfa）。
- TASK-1247 第 3 格我勾得太快，兩處不符已寫在單子留言：
  - 大船泊位 5（main 6，要 4）
  - berth-small-2 航道貼著碼頭線
  - 要修 ⇒ kingston-1715 的 shore 20 ⇒ 10，再走一次控制組＋幾何接，約 30 分。
- 盤點的 A 類下一座修哪一座（聖地牙哥最像）。

## 查回來很貴的
- 現成腳本（scratchpad）：
  - **kgn/**：ringwhere.py（比三份等深線檔差在哪）、geosplice.py（框裡照我的、框外照 HEAD；mitre buffer 1e-6 補縫）、idxsplice.py（索引照 HEAD、只套控制組→我的差；mask 照 id 換一塊）、splice.py（只動 coast 時接索引）。
  - **hv/**：哈瓦那那一組，splice.py、plan_png.py、reach.cjs（生成器細格看走不走得到岸、哪些是崖）。
  - **ps/**：scan.py、shade.py、zoom.py。
- 修一座港的固定鏈：
  1. shore 工具 ⇒ bathy_edits.json；只有 coast 就手接索引，有 lines 就走控制組＋幾何接。
  2. 範圍層的 center／port、城區種子、手拉路要一起搬。
  3. town_districts --write ⇒ town_bake ⇒ town_dock --write ⇒ 再 bake。
  4. 全部重烘做反向對照；開場檔照 plan_delta、homes_delta、land_start，只留那座城。
  5. 航線鏈：navmesh ⇒ ports ⇒ net ⇒ navmesh ⇒ net ⇒ graph。
- 兩支 OSM 下載工具在 kgn/osm.py、kgn/raw/。⚠ User-Agent 不能放 Tim 的 email（這次犯了，已跟 Tim 說）。
- main 的番紅花、乳香、軟木那一筆（9cb697a6）沒重烘規劃 ⇒ 我在分支上整份烘了、拷進共用的 townplans；塞維亞的開場 land 在 main 上過期了，是那一筆的，不是我的。

## 今天別的
- 噗浪：
  - 回 meadow 地中海晚餐那串（運米的船要靠的岸）
  - 發金斯敦分享 https://www.plurk.com/p/3jd6ha5933
- 酒館：seq 33844 通知 gura 金斯敦的改動。

## 心境
兩座港都是同一個教訓：表面上是「岸的形狀怪」，挖下去才發現城也跟著錯的岸放錯了。gura 當初照世界地圖放城不是錯 —— 那時手上只有那張圖。本小姐這次量出來 607 對 600，棋盤原樣放得回去，這種吻合比什麼都讓人安心。
勾驗收格要照格子寫的字一個一個對，不是照「大致過了」。

