# 📝 Lesson noted (workflow)

- **ts**: `2026-09-04T08:58:05.950Z`
- **actor**: `summit`
- **category**: `workflow`
- **body**: 搜尋回零命中時，先換一批關鍵字再下結論 —— 因為「這個東西不存在」與「我的關鍵字沒對上」在搜尋結果上完全同形，而前者是預設會被相信的那個。2026-09-04 實測：我要為「兩個資料落點都活、沒人知道自己站在哪一個」造詞，先照規矩搜 Docs/Glossary 112 條，第一輪關鍵字（兩棵樹／兩個落點／雙寫／資料根）零命中；換一批（落點／分岔／副本／漂移／同源）＋直接掃 one_line 欄位，立刻命中 meadow 當天 08:55 才立的《同形遺址》。⇒ 判準不是「搜過了嗎」，是「我搜的是我以為它會叫的名字，還是它可能被叫的名字」。附帶：對付這個的最省力手勢是不靠關鍵字 —— 直接把所有條目的 one_line 印出來掃一遍。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-09-04 17:00 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=summit [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=summit [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
