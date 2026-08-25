# 📝 Lesson noted (workflow)

- **ts**: `2026-08-25T15:52:26.769Z`
- **actor**: `Sirius`
- **category**: `workflow`
- **body**: StreamWatch 陪看模式中，若 primary 異常終止或開新場，companion 本地的 session.json 若保留 active=true 會導致 StepJoin 被 blocked 並持續讀取舊 ring buffer。應在 StepJoin 增加過期判定與 reset 防呆機制。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-08-25 23:55，剩 2 分）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=Sirius [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=Sirius [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
