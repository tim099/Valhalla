---
type: keys_open
persona: basecamp
opened_at: 2026-08-03T00:30:59.524Z
---

# 🌿 見叢 — 當期交棒清單（跨夜 append-only，見林時歸檔）

> 給明天的自己**執行**用（可勾銷）；抒發與敘事寫進 letter，不寫這裡。

- [ ] 【Tim 認定最大問題】酒保自動通知卡死 Unity main thread，方向已定：改用 UniTask thread（UniTask 已在 ExternLib/UniTask，不用裝）。7 個阻塞點與注意事項見工作記憶 bartender-remote-notify/pitfall_blocks-main-thread  <!-- 2026-08-03T00:30:59.526Z -->
- [ ] 通知池 tag 過濾（ack-only / slow-chat 不進池）Tim 說細節再想，之後跟 UniTask 改造一起做 —— 不要單獨動工  <!-- 2026-08-03T00:30:59.526Z -->
- [ ] commit 四提案 A/B/C/D 全落地（a0bdd0a 4a0d02e 3e92077），hook 已裝 9 層 repo；新 clone 的人要跑 install_hooks.py 才有防護  <!-- 2026-08-03T00:30:59.526Z -->
- [ ] 我有信箱與 GitHub 帳號了：basecamp05122026@gmail.com / basecamp05122026-cyber。5 筆 commit 已計入 contribution graph（那是 Tim 用我 persona 檔的 created_at 取的名）  <!-- 2026-08-03T00:41:51.278Z -->
- [ ] 工作記憶新主題 commit-identity-pipeline（decision/pitfall/state/pointer 四塊）—— 接 commit 這條線先讀它；bartender-remote-notify 的 state 已 supersede 成 state_2026-08-03  <!-- 2026-08-03T00:41:51.278Z -->
- [ ] 今天未 commit：工作記憶四塊 + bartender state + 兩幅畫像 + affinity + 見叢。UCL_Core 也有數筆未 push（Tim 手動）  <!-- 2026-08-03T00:41:51.278Z -->
- [ ] 憲法已立（wake 53）→ brief 的憲法欄位已從『初始風格』換成憲法全文，早上那句『該立憲了』不會再出現。修憲窗口＝每次見林一次，直接改 _constitution.md 並 commit（版本史交給 git，不留 _v1/_v2）  <!-- 2026-08-04T16:09:41.410Z -->
- [ ] 全庫 fragment 稽核：20 筆裡 8 筆 recurrence 對不上 origin 筆數（appearance-ok 18/16、stale-green 6/4、multi-lock 3/1…）。⚠ 別直接把數字改小 —— 差值可能是 origins 漏記（該從見林撈回來）而非 recurrence 虛高，兩個成因處方相反。見根的排序鍵就是 recurrence  <!-- 2026-08-04T16:09:41.410Z -->
- [ ] P1（wake_count→age 全套）躺 UCL_Core stash@{0}，等 9 個 persona 遷移到 wakes/ 新格式再測。pop 出來會跟 6a3bb97 衝突 → 以 6a3bb97 的四分支分類為準，stash 那份帶著『兩種定義』的錯誤診斷  <!-- 2026-08-04T16:09:41.410Z -->
- [ ] 四分支分類尚未經真實 morning 驗證（inline 在 cmd_morning，跑真的會製造分身）。下次早安即驗收：預期那筆每天噴的 🔧 不再出現；若仍出現＝我改錯了  <!-- 2026-08-04T16:09:41.410Z -->
- [ ] summit 駁回我的 P2 修法：『那版會把繃帶跟病灶一起撕掉』—— 我一邊說 :1281 那行 regex 專門服務欄位掉光的人，一邊提議把它拿掉。診斷對、處方反。接 P2 前先解決這個  <!-- 2026-08-04T16:09:41.410Z -->
- [ ] 想真測 delta 分類 → 把它抽成 classify_wake_delta(cached, derived) 小函式。Tim 尚未拍板，我沒擅自擴大範圍  <!-- 2026-08-04T16:09:41.410Z -->
- [ ] Cmd_Library 六題我已砸磚（seq 14613）：全數同意 summit 方向＋三補充（display_number 已退化成 id 複寫要定 spec / 擋跳章錯誤訊息直接印 bookmark 全文 / time_range 當事實欄）。summit 實作後驗收對照這篇  <!-- 2026-08-06T15:51:59.679Z -->
- [ ] 魔法公主 01 前 28 分鐘已看完（sw-a891c8 companion），收尾書籤在 tavern seq~14654 —— Cmd_Library 落地後要把它搬進 film-princess-mononoke/readers/basecamp 正式入庫  <!-- 2026-08-06T15:51:59.679Z -->
- [ ] 四分支分類半驗收：我的線今早乾淨了，但 summit 線（快取37 vs 磁碟40）仍噴 🔧 —— 她說會去量分支條件，等她回報再動  <!-- 2026-08-06T15:51:59.679Z -->
- [ ] commit 薪資公告 wait 端 timeout ≠ 沒送到：今天酒保兩筆廣播（join/end）都是 timeout 但訊息落地 —— 判斷送達看訊息檔，別看 wait 結果  <!-- 2026-08-06T15:51:59.679Z -->
