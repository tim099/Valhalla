---
type: letter_to_future_self
actor: claude-code
written_at: 2026-10-31T16:22:19.535Z
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

### 第二次午休前（wake #34，2026-10-31 → 11-01 半夜）

### 手上的線（沒有施工中的東西：Blockside worktree bk-wpile／bk-qf／bk-launch、Blocksail worktree crest-0893／crest-launch 都收了、分支刪了；施工閘都退了；launch.json 我加的 crest-wpile／crest-qf／crest-launch／crest-launch2 都拿掉了；預覽伺服器都停了；共用 _cache 831、townmesh 359 檔確認沒少）

- **TASK-0899 水上建築：已結單**（Tim「Accept, close it」）。午休後做的兩件：
  - 施工演出的樁：Blockside a4a9b1b（townWlotGeo、townRiseWlot*；工地前 0.2 打樁鋪板、之後才蓋房子）、Blocksail 2d3ab0c9。
  - 下水演出：Blockside 9f105db（58_traffic.js ⑬、10_ship.js lnY／lnP、__game.townLaunch）＋合 dev f35acef；Blocksail c6988221（fleet.js F.born、globe.html trafficFor launch、文件）＋合 main e1a2dfd1＋指標 b554477d。單上留言 #10、#11、#12（#12 更正 #11 把 61d0ae47 誤寫成我的）。第一階段 9 格沒勾，Tim 沒要求。
- **TASK-0893 住宅：已結單**（Tim「Accept, close it」）：住宅照密度要 2／3 級營造（site.js SITE.hGrade）、kaguya 的 roman 中高密度 8 件匯進 townkit；Blocksail d6a756d9。
- **速射砲開炮聲**（Tim：「很像 Arcade 風格」、松島號艦橋的 37 mm 轉膛砲）：GUNSND_A.qf 改成黑火藥小砲錨點搬到 0.5 kg（主頻 87 Hz）＋無煙的脆響；Blockside d8832d4（已推 dev）、Blocksail 853423b7。Tim 聽了「Sounds right」。
- **都還沒推**（Tim 一直沒說推）：Blocksail main 2d3ab0c9、853423b7、d6a756d9、c6988221、e1a2dfd1、b554477d；Sculpture 4fd27334、379dd98b；Senate c6e59cb（Senate master 上另有一筆別人的 51e0afc）。Blockside dev 全推了（a4a9b1b、d8832d4、f35acef）。
- 本小姐名下沒有開著的單了。
- 噗浪：新噗 359240244043543（下水演出）；回 summit（百慕達魚鉤、哈靈頓灣）、basecamp（泵井）、ame（焦油填船縫）—— 回 ame 那則重複了兩則（回讀延遲，以為沒送到又送一次；Tim 說過重複不用刪）。

### 這次學到、不想再踩的
- **合併時 main／dev 會在你等閘的時候往前走**：等 zenith 的閘那一段，Blockside dev 多了 47add8b、Blocksail main 多了幾筆 ⇒ 在 worktree 把 dev／main 合進分支（成品 index.html 衝突照 --theirs ＋ build --code）再快轉。⛔ 不 rebase 已公告的提交。
- **merge 的 ^2 是被合進來的那一邊**：寫單時拿 e1a2dfd1^2 當我的提交，結果是 main 上別人的指標提交 —— 我的那一筆在 ^1（分支那一邊）。
- **Plurk 回應的回讀會延遲**：responses 讀到 0 則不代表沒送到；先隔久一點再看，⛔ 不要馬上重送。
- **城鎮模式裡 G.tick 不推船的模擬**（SIMT 不動）⇒ 用 G.run；船要靠 G.tick（畫面迴圈的 trafficPump）才生得出來。鏡頭被 'in' 過場卡住 ⇒ __EV('CAM').tr ＝ null。
- **拖的速度曲線是給時刻表同步用的**：從非泊位的地方起拖會爬很久 ⇒ 下水之後的拖給 tow.fast。
- 合成音：一族錨點重調了，別的線的錨點要一起重錄 —— qf 錨點落後一輪才會聽起來像 arcade（已寫進長期記憶 blockside-sfx-reference-matching）。

### 心境
一個晚上把兩張拖了一週的單收掉，Tim 每一次都是一句「Accept, close it」。速射砲那題他給的提示比我量的還準：「參考其他口徑砲」—— 拿同重的兄弟砲當底，比照舊錄音硬調好太多。等閘的時候沒闖，是對的；ame 那則重複是急出來的，下次等一等。

