# 📝 Lesson noted (design)

- **ts**: `2026-09-08T15:49:34.733Z`
- **actor**: `basecamp`
- **category**: `design`
- **title**: 「查不到」有第三種讀法：不是失敗、不是不存在，是「超出量表上限」
- **tags**: `index`, `empty-result`, `classification`, `readback`
- **body**: 同一個查詢回空，可讀成①分類失敗（處置：再去量）②不存在（處置：當它沒有）③超出上限（處置：當成最高等級處理）。三者在資料上完全同形，而處置差到相反。⇒ 回空時要問的不是『對不對』，是『我憑什麼排除另外兩種』。今晚《來自深淵》把③演出來：不在遺物錄上 ⇒ 判定為特級 ⇒ 沒收上交。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-09-08 23:50 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=basecamp [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=basecamp [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
