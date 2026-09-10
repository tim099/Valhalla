# 📝 Lesson noted (workflow)

- **ts**: `2026-09-10T04:17:51.845Z`
- **actor**: `basecamp`
- **category**: `workflow`
- **body**: 更正上一筆（2026-09-10T04:17:12Z，同 actor）：那一筆的血證句主詞被 shell 吃掉了 —— 落地的是「血證 2026-09-10：⟨空⟩ 的寬版」，被吃掉的字是反引號包住的 `-dirty`（我用 inline --arg 傳長文，反引號在 Git Bash 裡是命令替換 ⇒ 印出 `-dirty: command not found`，而 Cmd 照樣回 ✓ Success 並把殘句寫進 append-only 台帳）。⚠ 而最貴的一格是：那句話**缺了主詞卻讀起來完全正常** —— 「⟨空⟩ 的寬版」跟一個省略主語的中文句同形，沒有任何一層會叫。⇒ 兩條可照做的規矩：①長文一律走 --arg-file，⛔ 無例外（「這句不長」正是那個例外的長相，而我這次的理由就是「只是一句 lesson」）；②寫入 append-only 的東西送出後要回讀一次**內容本體**，不是只看 exit code —— 台帳改不掉，只能補一筆。📌 這一筆本身就是上一筆那條規矩的實例：我在記錄「收窄要有落點」的同一個動作裡，弄丟了那個收窄對象的名字。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-09-10 12:22 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=basecamp [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=basecamp [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
