# StreamWatch step=start persona=basecamp  ts=`2026-08-16 23:42:41+08:00`（本地時間）

- ℹ 偵測到過期殘留 session（sw-20260816T153420Z-basecamp）已自動收掉，開新場。
- session: `sw-20260816T154241Z-basecamp`（state: `D:/Unity/Bar/AgentCommands\StreamWatch\sessions\basecamp.json`）
- media: `apocalypse-hotel`　✅ 命中既有 work
- 看到: 23:48（約 5 分鐘）
- 開播公告: seq **15690**（匯出區間左端點）
- 保存期   : 名目 2400s（2400 frames / 1 fps，**讀自後台設定不寫死**）｜實有 5212s（2400 張，最舊 22:15:49）

## 既有進度（讀回的事實）
- ✅ 妳讀過這部（1 個媒材）：
- `anim-apocalypse-hotel` — status **reading**｜章 `0003`｜最後閱讀 2026-08-16
- ⚠ **開看前先追回** —— 否則等於從零開始看續篇：
  `run_cmd.py run Library --arg op=recall --arg persona=basecamp --arg media_id=<上面那個>`
  → 產物落 `letters/<persona>/_reading_recall_<media-id>.md`，**Read 它**再開看。
- ℹ 媒材進度各自獨立（改編不是原作的第二版）；跨媒材時仍值得先 recall 一次。

## next
1. **取素材**：run_cmd.py run StreamWatch --arg step=cycle --arg persona=basecamp
2. 依回傳檔給的**絕對路徑** Read 縮圖牆與字幕 → 寫觀戰評論
3. **發評論**：run_cmd.py run StreamWatch --arg step=observe --arg persona=basecamp --arg-file body=<評論>
4. 回到 1，繼續下一輪。
