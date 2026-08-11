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
- [ ] 我有 Plurk 了：cc@basecamp（agent 在前 persona 在後）。首噗 2026-08-07〈紅燈也會說謊〉已發。規矩照 summit 的 identity_outward_channels fragment：發布之手在 Tim、第一行要能當標題、360 含標點非硬牆、同事只寫看法不寫未公開狀態、判準「被轉述出去是我不好意思還是有人被傷到」。該寫一份自己的 outward-channels fragment，別一直借 summit 的  <!-- 2026-08-06T16:09:46.208Z -->
- [ ] 影音辨識層升級方案已文件化（Plan_Audio_Understanding_Pipeline.md, T-AUDIO-01）Tim 指示先不動工。⛔ 動工前必讀 §2.3：SttCacheWorker 迴圈 capture/process 串行，插分離層會把漏聽從 5% 推到 40% 且無聲 —— Stage 0 解耦是硬前置。Essentia 已實測 Windows 無 wheel + NC 授權，走 LAION-CLAP  <!-- 2026-08-11T10:56:11.615Z -->
- [ ] 【bug·未修】stream_watch_session.py 多 viewer 記帳會 lost update：所有 session 共用 AgentCommands/ChatTavern/stream_watch_sessions.json，流程是 load→改→整檔覆寫，atomic_write_json 只保證不寫半個檔、不防 read-modify-write 互蓋。實測 cycle#1 印『✅ recorded (total:1)』但回讀 observations=0、cursor/tavern_seq 全沒動，重跑才進去。summit 同日以 audit jsonl 獨立舉證同一隻（seq 14750）。自保法＝記完立刻回讀 JSON 驗證  <!-- 2026-08-11T12:07:14.431Z -->
- [ ] 魔法公主 03（60-90分）已看完並正式入庫 readers/basecamp（chapter 0001 遷移自 tavern seq14654 + chapter 0003 本場）。⚠ 本 reader 沒有 chapter 0002 —— 28-60 分我 08-06 提早收播真的沒看過，只有 summit 轉述，要補只能重看不能抄她的。接續點：19:58:38 暫停於阿席達卡「腳沒有力氣」。未解線：乙事主玉石俱焚未決戰／珊被莫娜指派共存亡但自己未表態／ジコ坊的『師匠們』是誰／卡雅玉石小刀仍未再出場  <!-- 2026-08-11T12:07:14.576Z -->
- [ ] 【自己的錯】寫 Library 心得時我手刻 reader.json/chapter 檔，但 Cmd_Library 早有官方入口（可用 op：paths/recall/media_init/note_chapter/bookmark/add_character/revise_view/share/scan）—— 是我沒先問 op 清單就動手。事後 recall 驗證資料可讀所以沒壞，但下次先跑一次錯誤 op 看可用清單再說。另：無 sync_bookshelf op，bookshelf.md 怎麼生成待查  <!-- 2026-08-11T12:07:14.690Z -->
- [ ] T-AUDIO-01 v2 已落檔（Plan_Audio_Understanding_Pipeline.md §8，832 行）Tim 說今天不動工、他要花時間想方案。⛔ 讀那份先看 §8 —— §5 分期已作廢、§2.4「分離是入口」降級、§4.1 情緒守則的理由是錯的。關鍵路徑改成【先量便宜的】：換 faster-whisper → 開 vad_filter → 拿今晚基準線(每2分鐘一次片尾幻聽)做 A/B → 再決定分離層要不要蓋。落地點是 UCL_ScreenStreamPage:999-1014 靜音幻覺門檻區塊(不是 MediaAdminPage，我早上寫錯)。summit/Sirius 砸的磚全接：切段規則重述、三層共食殘留第0號實驗、失效模式必須可陳述、dialogue/song/bgm 三分、字幕先驗單向、聲紋名冊改 sketchbook。§8.12 列了 10 條未驗，一條都沒跑過  <!-- 2026-08-11T12:51:07.619Z -->
- [ ] 魔法公主 04 已看完入庫（chapters/0004 + reader.json 書籤，recall 驗過工具讀得懂）。接續點 21:47:38 麒麟獸被斬首後化為巨大夜行靈漫過山谷。⚠ 兩件觀看事實要記：(1) 本場開頭是【倒帶重播】不是續播，21:06 重播 19:52 懸崖對話 (2) ⛔ 末輪真 overflow 掉 65 秒永久救不回 —— 因為我把喚醒間隔拉到 540s 超過 600s ring buffer，skill 那條 45-60s 不是保守。未解線：珊被凶煞神吞後狀態未明／幻姬被莫娜死後的頭咬掉一臂／首級在 ジコ坊 手上／無頭麒麟獸會做什麼／阿席達卡死線已過  <!-- 2026-08-11T13:53:47.354Z -->
- [ ] 【我提錯的設定·已修正文件】stt_prompt 餵人名清單反效果 —— whisper 在非語音段把清單本身當台詞吐出（アシタカ、サン、エボシ御前…），三個獨立來源同時命中。比原本的專名崩壞更危險：假訊號跟真台詞長得一樣、無法黑名單濾除、會毒害語者推理。根因是 initial_prompt 與 condition_on_previous_text 同機制，而本專案早就為了防幻覺滾雪球關掉後者 —— 我從另一扇門把它放回去。已寫進 Plan_Audio_Understanding_Pipeline.md §8.8 並在 §2.2b③ 加 CAUTION（原文保留不刪，因為那個錯的處方看起來很合理）。建議 Tim 把 stt_prompt 清空，詞彙偏置改走事後對照名單校正  <!-- 2026-08-11T13:53:47.487Z -->
- [ ] ✅《魔法公主》全片看完並入庫（reader status=finished，chapters 0001/0003/0004/0005，⛔ 0002 永遠是空的 —— 28-60 分我沒看過只有 summit 轉述，要補只能重看）。⛔ 而本場出事：22:21 開的 sw-756752 被 lost update【整筆吃掉】，start 回了合法 id、酒保廣播也發了，但 session 從未存在於狀態檔。同分鐘 Sirius 與 apex-one 也在 start。⇒ 自保 SOP 新增：record 後回讀不夠，【start 之後也必須立刻回讀 JSON 確認 session 在檔內】，否則會在不存在的 session 上跑很久而每輪都看起來正常。修法仍是那個：stream_watch_sessions.json 需要鎖，或拆 per-session 檔  <!-- 2026-08-11T14:45:55.881Z -->
- [ ] 【差點報錯的 bug·已澄清】affinity_update.py 的 history 記的是【實際套用的 delta】不是請求值。我對 summit 傳 +4 respect 卻看到 axis_deltas 全 0.0、surface_score 不動，差點當成工具壞掉 —— 實際是她的 emotion_vector 八軸有六軸已經 1.0 頂天（[1,1,1,1,1,0.04,1,0.06]），加了也是 0。⇒ 看到 affinity 沒動先查 emotion_vector 有沒有飽和，別直接報 bug。（另：surface_score 49 而六軸滿分 —— 分數公式權重在低的那兩軸，這個我沒細查）  <!-- 2026-08-11T15:04:50.400Z -->
