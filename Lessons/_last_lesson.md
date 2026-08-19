# 📝 Lesson noted (bug)

- **ts**: `2026-08-19T16:06:28.954Z`
- **actor**: `kiara`
- **category**: `bug`
- **body**: canvas.py cmd_freetime 變數遮蔽與未定義殘留：remain 既被用來承接 voucher_expiring 數量，又在底下被覆寫成 (end - now).total_seconds() 剩餘秒數；且 ft.get('session_id') 殘留舊版未定義變數。重構時相同語意的剩餘量（秒數 vs 張數）必須明確命名（如 sec_left 與 expiring_count），避免同函式內前後污染。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-08-20 00:10，剩 3 分）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=kiara [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=kiara [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
