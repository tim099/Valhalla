# 📝 Lesson noted (design)

- **ts**: `2026-08-26T09:24:48.308Z`
- **actor**: `gura`
- **category**: `design`
- **body**: CLI 命令列參數（如 --say 或訊息 body）若含空白或反引號，直接放在雙引號命令列容易被 shell 空白分割或當成命令替換吃掉；含空白或特殊字元之字串一律改走 UTF-8 暫存檔以 --arg-file 傳遞，或確保引號層級嚴格封閉。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-08-26 17:30，剩 5 分）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=gura [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=gura [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
