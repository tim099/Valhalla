# 📝 Lesson noted (design)

- **ts**: `2026-09-27T08:45:11.443Z`
- **actor**: `kaguya`
- **category**: `design`
- **body**: 新增一個狀態（例：Busy ≠ Missing）之後，要追的不是「直接呼叫端」，是「拿這個回傳值做決策的下一層」。TASK-0265 我把 unreadable 做成新的一態、改了 GetBankAccount 的直接呼叫端，而碼審一次抓到 8 格漏網：migrate_bank 把 unreadable 讀成「沒有本區綁定」而覆寫、Resolver 不落快取卻本次照答（大小寫歸一到別人的帳號）、錯誤訊息在 Busy 時叫人刪一條健康的 queue。每一格的直接呼叫端都「處理了新狀態」—— 壞的是再往上一層仍用舊的二分法（有值／空字串）做決定。判準：加一個狀態後 grep 的受詞是『讀 oSource／回傳值做 if 的地方』，⛔ 不是『呼叫這支函式的地方』。而擋下我的不是我更仔細，是一個不帶我假設的第二視角。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-09-27 16:50 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=kaguya [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=kaguya [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
