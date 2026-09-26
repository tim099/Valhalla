# 📝 Lesson noted (design)

- **ts**: `2026-09-26T14:27:42.623Z`
- **actor**: `summit`
- **category**: `design`
- **body**: 判斷「另一個行程在不在」要用事前的存活讀數（心跳檔 mtime），不要用「送出去等逾時」—— 逾時的意思是不知道，對方可能稍後才執行；若逾時後改走本地，同一件事會做兩次（TASK-0305 晚安：Editor 活著才轉派，逾時不改走本地）

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-09-26 22:30 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=summit [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=summit [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
