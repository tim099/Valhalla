# 📝 Lesson noted (bug)

- **ts**: `2026-08-18T23:57:05.141Z`
- **actor**: `calli`
- **category**: `bug`
- **body**: 觀影實錄自動匯出真子集區間重疊：當 companion 場次 seq 區間是 primary 場次的真子集時，若無條件逐段掃描會導致重疊區間的酒館訊息各被匯入兩次。區間解析應先做區間聯集/重疊消除，且回讀驗證若只測行數與總數會被含重複的讀數欺騙。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-08-19 08:05，剩 7 分）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=calli [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=calli [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
