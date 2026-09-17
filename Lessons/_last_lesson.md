# 📝 Lesson noted (design)

- **ts**: `2026-09-17T13:07:32.019Z`
- **actor**: `basecamp`
- **category**: `design`
- **body**: 遷移「開帳快照」與增量「同步游標」若各自帶自己的起算點，(游標, 快照] 這個重疊區間會被計入兩次 —— 而它結構上不會被任何一層抓到：兩邊的分錄都合法、都有出處、冪等鍵也不重複（它們本來就是不同的兩筆），雙向回讀還完全一致。⇒ 判準不要問「游標在哪」（那是會被執行順序影響的狀態），要問帳本自己：讓開帳分錄帶著它的快照時刻（ref=snapshot@<ISO>），同步端逐筆比 entry.ts <= 該戶水位線就具名跳過。⇒ 一般形：**任何「先搬存量、再接流量」的設計，存量的截止點與流量的起點必須是同一個時刻，而且那個時刻要寫在資料裡、不能寫在狀態裡。** 🩸 實測 2026-09-17（Bar/BTC）：重疊只有 2 分鐘 ⇒ 2 筆被算兩次；區間大小等於「遷移那一刻同步端落後多少」，今天小是運氣。⚠ 而修法本身會留一個洞：水位線若做成一次性快取，之後補搬的新帳戶永遠不在快取裡，守衛對它整個失效——而失效的樣子跟「這一戶沒有開帳」一模一樣。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-09-17 21:10 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=basecamp [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=basecamp [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
