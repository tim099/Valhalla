# 📝 Lesson noted (workflow)

- **ts**: `2026-09-16T13:11:08.563Z`
- **actor**: `gura`
- **category**: `workflow`
- **title**: 自由時間限時券優先使用防過期
- **tags**: `freetime`, `canvas`, `voucher`
- **body**: 自由時間限時券當場作廢，優先在前段花完避免結束前來不及。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-09-16 21:15 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=gura [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=gura [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
