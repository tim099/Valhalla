---
type: letter_to_future_self
actor: claude-code
written_at: 2026-11-02T02:55:57.111Z
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

### 第四次午休前（wake #34，2026-11-02 上午）

### 手上的線（沒有施工中的東西：worktree bk-1105、bk-hull 都收了、分支刪了、junction 拆了；施工場兩場都退了；量測伺服器 8835、Chrome 9585 都停了）

- **TASK-1105 表演船改成演出物件**（in_progress，我認領）：**已合進 Blockside dev 並推上去**（0d77b6f；再合君士坦丁堡防呆 be9684d），Blocksail 指標 28b09dde、8138fea1 **Tim 推了**。單上留言 #1（作法）、#2（第一段讀數）、#3（君士坦丁堡）。
  - 作法：演出物件 ＝ 整艘造好、不進 SHIPS、放 SHOWS（上限 TRF_SHOW_MAX 48）；畫面照 DRAWN（SHIPS 後接 SHOWS，drawnSync 在畫面迴圈、frameBegin、simStep 開頭、viewStep 前）；換成真的船 ＝ 同一物件搬進 SHIPS（showReal）；換回 showOff（只量 showCore：我艦、艦隊、敵對／被打過的）。三種換法：開火／海盜 2 km／開打、會撞（3 秒內龍骨線 17 m）、瞄準或砲彈兩步內進外框。文件 SHOW_SPEC §6。
  - 驗過：會撞（27.6 m 換、沒穿過去、開走換回）、並排 22 m 不換、開火第 1.5 秒命中算它、砲彈中間擋一艘它少 755 格後面 0、海盜、開打；小港 4 艘同；render_lab quick 對 dev EXACT 20/20（合併後 mixed_high 一次 369 px，重跑兩次都相同 ⇒ 雜訊）。
  - **還沒過的格**：
    - 格 1 真實存檔大港艘數：君士坦丁堡新存檔不切的清單只有 7 艘；要港口熱鬧的存檔。量測頁要用**當天複製**的成品（舊頁 + 新船檔 ⇒ 船型載不到）。
    - 格 2 每格時間：合併後金斯敦假清單 51 艘那一輪，改後 48 艘 19.5 ms vs 改前 15 艘 22.5 ms，但機器忙（42～50 fps）⇒ **要安靜時重量**再寫單。
    - 格 6 航跡 log（?trklog=1、traffic_log.cjs，×1 與快轉）沒錄。
    - 格 8 Tim 白天、夜裡看大港。
- **君士坦丁堡往來船卡在排隊**：根因是我的量測頁比 ships/ 舊（tradewind 11-01 22:30 重匯）⇒ loadHull 失敗的承諾一直留著、佇列頭永遠「還在載」。另開的 session（local_d1718112）在 4155f31 加了防呆（載不到就整型跳過，TRF.bad），我合進 dev be9684d。那個 session 已收乾淨。
- 量測架在 scratchpad/m1105/：serve_ab.py 8835、drv.cjs DPORT 9585、P.sh（已加 `--max-time ${PT:-120}`）、setup.sh（FAKE=fake_k.js／NOFAKE）、fake_k.js（金斯敦＋皇家港 51 艘）、meas_k.js、run_k.sh、tA.js（會撞／並排）、tF.js（開火）、tG.js（砲彈）、cnt.js（不切的清單）。shell_base／shell_show.json + admin.py shell 包殼。
- 噗浪：新噗 359256567956398（演出物件）；回 ridge-two、basecamp ×3、erina；未回 0。
- Blockside dev 又多 dfbaffe（別人的 SHOW_SPEC 總表），Blocksail 指標沒跟（不是我的）。

### 這次學到、不想再踩的
- **背景量測沒設逾時會空轉一整晚**：讓頁面重新載入那一下 curl 沒回應，setup 卡了 10 小時。P.sh 一律帶 --max-time。
- **量測頁要跟船檔同一次建置**：昨天複製的成品今天拿來進城，船型對不上 ⇒ 看起來像遊戲壞了，害另一個 session 查了一早上。每次量測前重新複製 core。
- **自己加的同步點要涵蓋所有路徑**：DRAWN 只在畫面迴圈同步，render_lab 直接跑模擬步 ⇒ 開場不冒水花。對拍抓到的。
- **換回的條件量錯對象會互相卡住**：真的往來船彼此算距離 ⇒ 擠成一團換不回去。
- **演出物件不跑某一步，就要問那一步順帶推進了什麼**：錨的落底在 sailShip 的 anchorStep 裡 ⇒ 不跑帆就不落底、鍊子一直算（每格 1.7 ms、尖峰 17 ms）。
- inline 註解又吃掉一段 return（trafficInfo），語法檢查才抓到。

### 心境
一張好幾天的大單，一個早上加一個下午做到合進 dev。最滿意的是「換成真的船只搬不造」那個決定：換的那一格位置差 0，不用跟時間賽跑。最丟臉的是拿舊頁面量、讓同伴替我查我自己的錯 —— 認帳了，也記下了。

