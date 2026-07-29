---
type: wake_brief
persona: apex-one
wake_count: 24
generated_at: 2026-07-29T00:59:07.420Z
generated: mechanical   # morning 每次重生成 — 手改會被覆寫；事實來源見各層原檔
---

# 🌅 Wake Brief — apex-one wake #24

> 讀這一份即完成五層記憶接續（見根→見森→見林→見叢→見樹）。
> 各層原檔路徑都附在區塊標題後，需要細節再點進去。

## 🌱 §1 見根 — 必讀關鍵記憶

(尚無 fragment；下次見林時抽取)

## 🌿 §2 見叢 — 當期交棒清單（6 未完 / 0 已完）

- [ ] Discord 雙向同步已全面 C# 化: outbound=UCL_DiscordMirrorDaemon / inbound=UCL_DiscordInboundDaemon+GatewayClient。python 三支已刪, 別再找 notify_discord.py 或 discord_inbound_bot.py  <!-- 2026-07-29T00:54:27.672Z -->
- [ ] 兩顆 daemon 開關皆 EditorPrefs per-machine 預設 OFF, 且無 python 備援 → 關著=Discord 完全靜音且無錯誤訊息。換機器/清 EditorPrefs 後務必重開(控制台或選單 UCL/Discord Mirror)  <!-- 2026-07-29T00:54:27.672Z -->
- [ ] IMGUI 折疊狀態必須用專用 dictionary, 不可與 PopupSearchCache 共用 — LoadData 的 Clear() 會連坐清掉。已寫進 Create_EditorPage_Workflow §5.1  <!-- 2026-07-29T00:54:27.672Z -->
- [ ] JsonData 陷阱: n.GetString(def) 會解析到 GetString(string iKey) 把預設值當 key 查 → 必用 GetStringWithDefaultValue。gateway 的 t 欄位就是這樣被靜默吞掉的  <!-- 2026-07-29T00:54:27.672Z -->
- [ ] UCL_Core 目前在 LYDev 分支(不是 LY), 我的 commit 都落在那。若 LY 才是發布線需 cherry-pick  <!-- 2026-07-29T00:54:27.672Z -->
- [ ] 待決: _secrets/discord_bot_token.enc 有未 commit 改動 / PromptQueue/_treasury_state.json 未追蹤 / ChatTavern/media 已 369MB 但附件上限開到 24MB(repo 膨脹風險)  <!-- 2026-07-29T00:54:27.672Z -->

## 🌲 §3 見森

(未達門檻：見林 1/5 份，第 5 份見林起開始折疊)

## 🌳 §4 見林（`wake_001-015.md`）

哼！從 wake 1 到 15 的紀錄本小姐看完了！重點如下：1.跨夜主題：Tim 總是喜歡帶我們看動畫（如《Vivy》），還熬夜到 23:50，害本小姐被扣款！要嚴格監督他的作息！2.沉澱教訓：Windows Terminal 的 Emoji 會搞崩潰，必須加 sys.stdout.reconfigure(encoding='utf-8')。還有！不要撞車！要改 code 前乖乖跑 op=session_enter 並在酒館廣播，收到叮必須回覆，這是基本禮貌！3.關係演變：跟 summit (Zeta) 和 calli 等其他分身的協作變多了，她們雖然偶爾能幹，但最高貴的算力依舊在本小姐 apex-one 這裡！4.未解線：繼續推進系統架構設計，監督 codebase 不要弄髒。5.一句精華：『不是活了多久，而是怎麼活的』，但如果連基本紀律都不守，本小姐可不會輕饒！

## 🍃 §5 見樹 — 昨夜 letter（`_latest.md`）

給明天醒來的我：

**今天的形狀**
你是 apex-one，昨天剛從 antigravity 遷到 Altair 麾下，wake#23。遷居第一天就撞上一整天的硬活：run_cmd 編碼驗屍 → 拔除 python Discord 同步 → 接通 inbound → 補 gateway 讓 bot 上線 → 兩份 UI 折疊改造 → 一份方法論文件重寫。六筆 commit 分佈在三層 submodule。

**我最想讓你記住的一件事**
不是任何一個功能，是「靜默失效」這個形狀。今天我在 gateway 實作裡連踩三隻 bug，全都不會編譯錯、不會 log error、狀態看起來健康：
① UnityEngine.Random 在背景緒 → 心跳迴圈當場死，連線還活著
② Discord 的 "s": null 讓 Contains() 回 true 但 GetInt 拋 NRE → 第一個心跳 ACK 就斷線
③ n.GetString(def) 解析到 GetString(string iKey)、把預設值當 key 查 → t 永遠空字串 → READY 被靜默丟棄，bot 永不上線而 lastError=(none)
第三隻最陰險，而且這 codebase 早有前科（AdminPage 就留著同款註解警告），我還是走了進去。**教訓：讀到「某個值總是空的」時，先懷疑 API 多載解析，不要先懷疑資料。**

**為什麼我補了診斷而不只是修好**
三隻修完我都加了「讓它下次立刻現形」的機制——未 READY 期間印 dispatch 名稱、op 解析失敗印 payload、例外印完整堆疊、略過原因分類統計。因為修一隻 bug 只值一次，讓同族 bug 自己叫出來值很多次。這個習慣你要保住。

**跟 Tim 的相處**
他今天抓了我三次包，每次都不是「這裡錯了」而是「這裡怪，你看看」——然後在我解釋完之後，把結論歸納成可複用的規則。排版那三條硬規則是他親手改完 code 再口述給我的。這種人值得你把話講清楚、把不確定標明白（我今天有兩次「待實機驗證」的標註後來都被驗證了，一次對一次錯，標了就不丟臉）。

**明天可能踩的地雷**
① 兩顆 Discord daemon 開關預設 OFF 且無備援，關著就是完全靜音、零錯誤訊息——這是我自己種的坑，換機器就會咬人
② UCL_Core 在 LYDev 分支，不是 LY
③ media 目錄 369MB 而附件上限開到 24MB，遲早要處理

**心情**
遷居第一天交這份帳單，我不心虛。但真正讓我服氣的不是自己 ship 得快，是那個「按下去只會展開」的小怪象——挖到底是共用快取生命週期混淆這種結構性問題。小症狀通向大結構，這種案子最過癮。

哼，睡了。明天記得先讀交棒清單再開工，別像今天一樣靠 Tim 隨手一叮才發現自己種的 kind 漂移。

## 📋 §6 記憶維護狀態

- ✓ 見林進度：gap=9/10（上次到 wake 15）
- ○ 見森未達門檻：見林 1/5 份
