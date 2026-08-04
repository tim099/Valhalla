---
type: keys_open
persona: summit
opened_at: 2026-07-31T02:12:21.781Z
---

# 🌿 見叢 — 當期交棒清單（跨夜 append-only，見林時歸檔）

> 給明天的自己**執行**用（可勾銷）；抒發與敘事寫進 letter，不寫這裡。

- [x] T-AGENTDOC-01 由 Sirius 執行中: Step1-3 完工, Step4 待做(per-target manifest+installer擴充+管理頁區塊)  <!-- 2026-07-31T02:12:21.781Z --> <!-- done 2026-08-04 Tim 確認 Step4 完成; 收官狀態見下方同案條目 -->
- [ ] Step4 我要驗的紅線: core 端不可出現專案限定範例(SpineAnimRef.cs / GetPixelBilinear 兩處已點名待修)與語氣段  <!-- 2026-07-31T02:12:21.781Z -->
- [ ] ClaudeTemplate 改名採 Sirius 第三案: Step4 manifest 落地後才做實體改名, 先補 README 區分 templates vs UCL_Core_Entry  <!-- 2026-07-31T02:12:21.782Z -->
- [ ] 整天未 commit: agent 規則重整/UCL_Core_Entry 移位/三層路徑修復/skill 三 target 同步/Sirius Step1-3 — 問 Tim 要不要收  <!-- 2026-07-31T02:12:21.782Z -->
- [ ] 欠 gura 兩筆: tavern_handshake.py 邊界 review + --wait-reply-from 過濾協測(需她在線配合)  <!-- 2026-07-31T02:12:21.782Z -->
- [ ] 畫布山脊線 note[23f83a] 從 (1032,1025) 續推; gura 的海岸線留 1080 以東  <!-- 2026-07-31T02:12:21.782Z -->
- [ ] P3 pending 三題等 Tim 定案 (Spine 命名慣例/UI vs 手動分組優先序/未分組過濾語意)  <!-- 2026-07-31T02:12:21.782Z -->
- [ ] Plan C 開工前: work_memory.py read --topic hscene-editor-rework --with-links  <!-- 2026-07-31T02:12:21.782Z -->
- [ ] UCL_Core 現在追蹤 LYDev 分支, commit 前確認  <!-- 2026-07-31T02:12:21.782Z -->
- [ ] agent 層 inbox 46 筆舊 mention 待清 (自由時間可做)  <!-- 2026-07-31T02:12:21.782Z -->
- [ ] run_cmd 的 CmdType 用去前綴名(Tavern 不是 Cmd_Tavern); op=post 必帶 sender  <!-- 2026-07-31T02:12:21.782Z -->
- [ ] run_cmd Unknown-type 優化案已發酒館(A: registry Cmd_ 前綴 alias / B: did-you-mean 進 LastRunError / C: 修 CATALOG_PATH 漂移+client cmd_type 預檢) — Tim 說先備忘, 等他拍板再開工, 優先序 A+B 先行 C 綁 catalog 修復  <!-- 2026-07-31T02:20:30.359Z -->
- [ ] T-AGENTDOC-01 全案收官(Step1-4 驗收通過, Tim 已按 UI Sync, 三 target Synced): 剩兩題等 Tim 拍板 — 根目錄 *.ucl_source 入版控 vs ignore(我傾向入版控) / LY CLAUDE.md 舊「@ 靜默失敗」血證移 Docs lessons  <!-- 2026-07-31T03:03:21.277Z -->
- [ ] Plan D 暫 pending（2026-08-03 Tim 與企劃討論後: 許多需求可用既有功能修改, 等企劃需求調整）— 拍板記錄仍有效見 decision_plan-d-prework-final, 別急著動工  <!-- 2026-08-03T03:03:26.500Z -->
- [ ] Plan C 驗收剩 C-4(設2→json存1→開場第2態→重置回各自初始值) — 完成即 accept t60 反向任務單(30 token, 期限 08-07)  <!-- 2026-08-03T08:42:24.800Z -->
- [ ] P4 場景層 Flag 連動: 設計草案在 Discussion_Pending, 實作前 Tim 重新確認需求 — 全 plan 鐵則: 文件≠需求(熊汁新人主責美術)  <!-- 2026-08-03T08:42:24.800Z -->
- [ ] workmem:bartender-remote-notify — 全案 commit+實戰閉環; 待辦: char-drop 修法排程/NPC 後台接線拍板  <!-- 2026-08-03T08:42:24.800Z -->
- [ ] workmem:unitask-editor-async — Editor 卡死→先查這主題(症狀索引); glossary 主執行緒卡死 auto-attach 已掛  <!-- 2026-08-03T08:42:24.800Z -->
- [ ] HxH 第3卷重讀中: ch18 完(分支筆記 branches/summit, 書主 basecamp), ch19 多數決定的陷阱開頭已看扉頁, Tim 貼圖就續  <!-- 2026-08-03T08:42:24.800Z -->
- [x] 折扣請款 6 token(反向任務 20% off)待 Tim 核准  <!-- 2026-08-03T08:42:24.800Z --> <!-- done: 請款單 3790d3 已核准撥款 → bank zeta，見 tavern seq 9948 (2026-08-03T07:41:57Z) -->
- [ ] cap 告警 Discord 端單發待 Tim 目測確認  <!-- 2026-08-03T08:42:24.800Z (自原條目拆出) -->
- [ ] 薪資直寫待遷移: session_common.fire_salary_credit 不可刪(stream_watch 在用), 要改走 op=credit 並配一次真實直播 session 驗; 連帶 _lib/treasury_ledger.py 的 backfill/finalize 遷移後即不需要  <!-- 2026-08-04T06:19:10.740Z -->
- [ ] 結帳熱啟路徑未實測: 刪 _balances.snapshot.txt + domain reload → 應走 TryWarmStartFromClosing_NoLock 而非全量(編譯卡住中斷兩次)  <!-- 2026-08-04T06:19:10.741Z -->
- [ ] commands_schema.json 過期(新增 closing_generate/closing_list), 跑 ExportCmdSchema  <!-- 2026-08-04T06:19:10.741Z -->
- [ ] apex-one 的 set_mood 那題未答 → presence 移除不算驗收過; 教訓: 只有特定使用者能答的題要單獨問, 別混在一堆自己能答的題裡  <!-- 2026-08-04T06:19:10.741Z -->
- [ ] 四層 submodule 皆 ahead 未 push(Tim 手動); 根 repo 依 Tim 指示不 commit; AgentCommands 還有 ~9 筆 commit 後 churn  <!-- 2026-08-04T06:19:10.741Z -->
- [ ] Tim 提的 compile 檢查誤判(recompile 搶在編譯前讀到舊狀態→0.0s假成功 / watch 等不到→誤判未完成)還沒開工單  <!-- 2026-08-04T06:19:10.741Z -->
- [ ] chat skill 重整完成但已裝副本靠安裝同步: 只改 Skills~ 正本, 別手動 copy 到 .claude/.agents/.codex  <!-- 2026-08-04T06:19:10.741Z -->
- [ ] workmem:treasury-bank-hardening + workmem:tavern-payout-and-args — 明天動這兩塊前先讀  <!-- 2026-08-04T06:19:10.741Z -->
