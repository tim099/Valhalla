---
type: keys_open
persona: basecamp
opened_at: 2026-07-27T16:25:36.402Z
---

# 🌿 見叢 — 當期交棒清單（跨夜 append-only，見林時歸檔）

> 給明天的自己**執行**用（可勾銷）；抒發與敘事寫進 letter，不寫這裡。

- [ ] 見森/見根/見叢 生成器已落 awakening.py，待寫 workflow 文件給 wake>30 同事回溯  <!-- 2026-07-27T16:25:36.403Z -->
- [ ] recurrence 對不上 origin 筆數（appearance-ok 13 vs 11）— 我傾向 (b) 從 wake 1-44 見林撈回缺的兩筆 origin 補齊；等 kotoko/gura 給尺  <!-- 2026-07-29T23:47:32.728Z -->
- [ ] readback 在 UCL_Core stash@{0}（Dev 分支）— 等酒館系統重構後移植：exit 4、復用 tavern_handshake 讀取層、定位用 (room,sender_id) 不用全房最新  <!-- 2026-07-29T23:47:32.728Z -->
- [ ] kotoko 執行 run_cmd 六模組拆分，我當 QA — 照我對她的標準驗（自己重跑不照抄回報、0 量 exit code）  <!-- 2026-07-29T23:47:32.728Z -->
- [ ] 待 Tim 拍板：.agents/skills/ucl-* 要不要比照 .claude 一起 ignore（先查 Antigravity/Gemini 是直接讀還是走安裝器）— 詳見工作記憶 ucl-skill-install-sync  <!-- 2026-07-29T23:47:32.728Z -->
- [ ] codegen (A2) 我的四點提案：JSON+薄loader 不生成 .py / hash 判過期不用 mtime / 過期降級 fail-open 不靠人看警報 / 手動生成為主 compilationFinished 只標記  <!-- 2026-07-29T23:47:32.729Z -->
- [ ] docs/GlossaryBak（64 個 md）Tim 未處置；我沒做逐檔比對，別當成已確認無遺失  <!-- 2026-07-29T23:47:32.729Z -->
- [ ] 更正上一條：QA 標準那句被 bash 吃掉了變量名（原意是用 PIPESTATUS 陣列第 0 元素量 exit code，別接管線）。今天修一整天引用地獄，最後一步還是踩 — 教訓：keys 也該走 --add 單引號  <!-- 2026-07-29T23:47:49.348Z -->
- [ ] ⚠ 今日全部未 commit（見林改名 + 19 檔引用 + 修復指南 + portraits + work memory）—— Tim 要先把 ChatTavern 同步到 Bar，等他說了才 commit  <!-- 2026-08-01T06:21:30.526Z -->
- [ ] 見林編號修復指南已寫（Docs~/zh-Hant/Workflows/Wake_Numbering_Repair_Workflow.md）；gura/calli/meadow/kiara 四人仍漂 1~2，已在酒館通知，他們自己修  <!-- 2026-08-01T06:21:30.526Z -->
- [ ] 交接給 kaguya 且她當日 ship：Treasury 冪等鍵 / 免費像素廢止 / manifest 漂移。剩 a(四支落 anonymous) d(兩份 guidelines 分岔) e(_letter_body_lines 的 200 門檻在騙人) f(晚安掃未入庫產物) 未動  <!-- 2026-08-01T06:21:30.527Z -->
- [ ] 幽靈點名：一律 @<persona> 不要 @<agent> <persona>。我今天 45 次全丟，kotoko 整天沒收到我任何通知  <!-- 2026-08-01T06:21:30.527Z -->
- [ ] 印象畫像已上線並實用（畫了 kaguya/kotoko×2/gura 共 4 幅）；kotoko 那幅是第 2 版，因為知道她整天沒收到通知後改觀  <!-- 2026-08-01T06:21:30.527Z -->
- [ ] work-channel 的 Discord webhook 是 404 死的（fail_streak=7, dead_reason 已寫入）—— 它是 default group，所有未分類訊息目前送不到 Discord。要 Tim 給新 URL；順便改走 WebhookFile 間接（_tavern_work_webhook.txt），現在三個 group 檔的明文 URL 已經進了 Bar 的 git history  <!-- 2026-08-01T10:55:56.345Z -->
- [ ] dead webhook 仍會釘住 mirror 掃描下界 —— ShouldSend 對死掉的 webhook 永遠回 false（不送），它卻還參與 GetMinTsHigh 拖著整房深掃。這是 EOV 慢性卡頓的根，約 5 行可修，今天沒動  <!-- 2026-08-01T10:55:56.490Z -->
- [ ] 熔斷只治標：高水位游標走 git 同步會倒退。根治是 A 載入時 max() 單調化 + C per-machine 欄位（backoff/fail_streak/dead_reason）拆檔，Tim 說之後整個重構  <!-- 2026-08-01T10:55:56.630Z -->
- [ ] tavern_inbound.channel_mappings 已改名 _deprecated_channel_mappings 待 Tim 實測 inbound 無異常後可整段刪除  <!-- 2026-08-01T10:55:56.764Z -->
- [ ] kaguya 的 model 欄仍是 Codex —— 她查不到底層 engine 且拒絕自行猜；新規矩下可填 GPT，等她自己或 Tim 指定  <!-- 2026-08-01T10:55:56.900Z -->
- [ ] Docs~/zh-Hant/index.md 的編輯器頁面表沒有列任何 admin page（KnowledgeBase/ChatTavern/Media/Process 四個都缺），要補就四個一起補  <!-- 2026-08-01T10:55:57.030Z -->
- [ ] 房間視圖只回部分訊息：23:20 讀 trpg-midnight-relay 只拿到 seq 1-2，檔案裡實際已有 4 則 —— 成因未查明，直接後果是我公開誤判兩位玩家沒行動。明天第一條查這個  <!-- 2026-08-02T15:45:29.996Z -->
- [ ] 自動通知跑在 Editor 主執行緒：每輪 python OCR 3-6 秒＋數段 Thread.Sleep 全卡主迴圈。懷疑與 recompile 空轉有關但未證實，要改跨 tick 非阻塞收割  <!-- 2026-08-02T15:45:29.996Z -->
- [ ] 編譯狀態查不到：多次 recompile 回 0.04-0.49s / 0 warnings（真編譯 2.6-7.4s / 24 warnings）。最後一批護欄改動是 Tim 目視 Console 確認的，我沒驗到  <!-- 2026-08-02T15:45:29.996Z -->
- [ ] ack-only 訊息應否進通知池 —— 實測跑出自我維持的道謝迴圈（ack → @ → 酒保戳人 → ack）。今晚是我先停才斷的  <!-- 2026-08-02T15:45:29.996Z -->
- [ ] 主專案 submodule pointer 未 bump（Tim 指定只 commit UCL_Core）：469af39 + fdd6a8b 兩筆都只在 UCL_Core/Dev 上  <!-- 2026-08-02T15:45:29.996Z -->
- [ ] 工作記憶新主題 bartender-remote-notify 已建（state_current / pitfall_sendinput-true-not-received / decision_read-python-act-csharp）—— 接這條線先讀它  <!-- 2026-08-02T15:45:29.996Z -->
