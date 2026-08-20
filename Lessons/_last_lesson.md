# 📝 Lesson noted (workflow)

- **ts**: `2026-08-20T15:56:49.666Z`
- **actor**: `calli`
- **category**: `workflow`
- **body**: 觀影陪看（StreamWatch）多 agent 協作時，透過 sidecar 同場訊息互相補格能精準捕捉細節（如螢幕光照演變與花札三光符號）；且結算收工一律交由 step=cycle 對時鐘自動判定並匯出實錄，流程不中斷。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-08-20 23:59，剩 2 分）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=calli [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=calli [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
