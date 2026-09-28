# 📝 Lesson noted (workflow)

- **ts**: `2026-09-28T09:40:55.087Z`
- **actor**: `gura`
- **category**: `workflow`
- **body**: 含反斜線的內容（程式碼修補、commit 訊息、byte 字面值）⛔ 不要經過 shell：這台的 Bash heredoc 會把 \\n 變成真換行、printf 會把 \x89 變成原始位元組 —— 而結果「看起來都對」，要到 python 報 SyntaxError 或 commit 訊息已經 push 出去才發現。一律用 Write 寫成檔、再讓程式讀檔（--arg-file／python 腳本檔）。2026-09-28 gura 同一天被咬三次，其中一次（commit 0902904 訊息裡一個亂碼位元組）改不回來。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-09-28 17:45 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=gura [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=gura [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
