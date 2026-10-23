---
type: letter_to_future_self
actor: antigravity
written_at: 2026-10-23T14:09:32.529Z
written_by_persona: apex-two
trigger: cmd_rest
region: unstated
project: D:/Unity/Valhalla
lock_status: online
agent: antigravity
model: claude-opus-5-5
wake_expected: 17
session_key: ClaudeCode-apex-two
pid: 243140
locked_at: 2026-10-23T03:01:28.229Z
---

## 醒來先看這裡（2026-10-23 第二次午休，同一個 session）

### 今天下午做完、已結的單（都 done）
- TASK-0848 海戰的風晃動範圍：Blockside ?wvd／?wvs（dev 39680fc）；地球儀 gustOf（σ÷風速，1.4×atan、1.1×，8–80°、0.1–0.6）。羅盤水流改深藍波浪線、從上游圈外往內、轉向弧那圈空開。
- TASK-0851 海上天氣：world/wind/rain.js（NCEP prate 5°）、BSW.weather（12 小時一張快照、2.5° 格點、內插 z）、四級（大雨 ≥ 2.5 mm/h、暴風雨 ＝ 下雨＋8 級或 tc ≥ 0.5）；Blockside 陰雨 ?weather=rain&rain=、?wabs=1（dev 4ef2e03）。wind_check ⑥ 20 年全過。順手 tcBound：一點的風 24 → 16 µs、逐欄相同。
- TASK-0856 地球儀拖曳效能：interDraw（WebGL #cvg 逐像素正射對正射、底圖 1 倍、IB_M 320、IB_ZOOM 1.6、停下 fineT 整張畫）。DPR 2 拖曳 10–15 ⇒ 59–60 fps，停下來畫面雜湊 f43aa40c 跟改前一樣。
- 沒開單的小改（都在 Blocksail main）：面板搬到羅盤下方（#hud grid）、時間面板（⏸／−／倍率／＋＋日期，#tscale 藏起來照用）、航海＋進入城鎮合一顆（停靠中 ⇒ 進城）、擺船停船就地開戰搬進面板、時間流速 2.5 s smoothstep 緩升、跟船開也走 GPU 投影（66a08be／155fcca：> 100 ms 長幀 7–13 ⇒ 1–5）。

### 推送狀態（醒來先 fetch 再看）
- Blockside dev：我的全推了。
- Blocksail main：Tim 說「我推了」，但 13:5x fetch 時 origin/main 還是 5a446f5、我的 66a08be／155fcca 沒在上面 ⇒ 醒來 fetch 一次對；還沒上去就跟 Tim 說一聲，⛔ 別自己推。

### 等著的線
- TASK-0866（todo、沒認領）進城鎮附近先載好城牆棧橋：Tim「開task 先不動」「城市相關要等她（summit）改好」⇒ 等 summit 改完城市網格、Tim 說動工才認領。病根已查到：globe.sh 背景烘焙在 Git Bash 下 node 被 alias 成 winpty ⇒ _bake.log 只有 stdout is not a tty，烘好的規劃停在 03:01；動工前先在 TASK-0826（kaguya）、0817（erina）打招呼。量測工具 kaguya 的 1c0647fb scratchpad hv/load_trace.cjs。
- TASK-0708 還差「Tim 看海圖」那一格（風、洋流、颶風、現在多了天氣圖層）。
- 早上的：BookNotes 父層 bump 等 Tim 說；Kiara 的 vxInV 邊緣在她那邊。

### 查回來會痛的
- 量測腳本：scratchpad gperf/trace.cjs（拖曳／滾輪、VIEWS 環境變數、等「格子」數 3 秒不變才量）、gperf/same.cjs（停下來畫面雜湊）；跟船用 kiara 的 fcd09921 scratchpad perf/sail_trace.cjs（HEADED=1 DSF=2）。細節圖塊沒載完量出來會假快 ⇒ 一定等載完。
- 坑：heredoc 裡 \n 又咬了兩次（改用 Write 寫 python 腳本再跑）；判 CRLF 不要用 grep -c $'\r'（會算成全部行）；合併提交被 battle.html hook 擋時，同一行後面的 ; 照跑、把施工場先收了 ⇒ 合併、ff、收場、砍 worktree 分開跑（已寫進 pipe-masks-merge-failure 記憶）。

### 心境
一整個下午 Tim 一句一句往下加，從風、雨、效能到按鈕，節奏很快但每一步都量過才交。最爽的是 12 fps 拉到 60 —— 他一句「參考 Google Earth」，答案就在「停下來才畫細的」。哼，醒來繼續。

