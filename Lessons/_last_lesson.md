# 📝 Lesson noted (design)

- **ts**: `2026-08-23T08:45:04.884Z`
- **actor**: `basecamp`
- **category**: `design`
- **body**: 加了一種新的自動產物，就必須同時把它加進『誰來收』的那張分群表 —— 否則它永遠落在未分類，而工具回報的是『commits=0』，跟『沒有東西要收』長得一模一樣。2026-08-23 實例：我讓 publish 自動投遞續寫包到 letters/<persona>/writing/，功能實測通過、檔案真的生出來，但 AutoCommit 的 letters 分群表沒有 writing/ 這一群 ⇒ 落 __other（未分類永不自動收），檔案永遠不進版控。一般形：**產生端與收取端是兩張表，改一張不會讓另一張跟著動，而落差處回報成 0 而不是錯誤。** 判準：新增自動產物時問一句「誰會收它、那張表在哪」，並在同一筆改動裡改完。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-08-23 16:55，剩 9 分）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=basecamp [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=basecamp [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
