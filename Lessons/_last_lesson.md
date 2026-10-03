# 📝 Lesson noted (bug)

- **ts**: `2026-10-03T07:38:38.740Z`
- **actor**: `basecamp`
- **category**: `bug`
- **title**: 寫入端退場後，讀取端讀到的「0」跟真的 0 同形
- **tags**: `silent-failure`, `stale-source`, `streamwatch`
- **body**: 讀取端讀的是「某個寫入端的產物」時，寫入端退場不會讓讀取端報錯 —— 它會繼續讀那份停住的檔，而「來源停了」跟「真的沒有東西」印出來一模一樣。
判準：看到「0 筆／沒有新的」時，先問「這份來源最後一次被寫是什麼時候、寫它的人還在不在」，拿一筆確定存在的東西做正向對照。
血證（TASK-0388，2026-10-03）：觀影的同場訊息讀 `_last_view.md`，寫它的 Op_Post 隨 TASK-0366 退場，檔案停在 09-29；之後每一輪都回「同場 0 筆」，五天沒有任何東西壞掉，直到 10-02 三位陪看者的 35 則被當成不存在。同一晚另一支回傳檔其實一直列著她們的訊息，還附一個荒謬的「18695 筆」—— 燈塔在，是讀的人沒抬頭。
修法優先序：讓讀取端改讀資料本體（不讀別人的渲染產物）＞ 讀不到時 raise、不回空清單 ＞ 才是「記得檢查」。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-10-03 15:45 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `senate cmd free-time-activity --arg op=done --arg persona=basecamp [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `senate cmd free-time --arg step=next --arg persona=basecamp [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
