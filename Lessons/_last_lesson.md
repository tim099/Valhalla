# 📝 Lesson noted (design)

- **ts**: `2026-11-01T04:01:07.669Z`
- **actor**: `crest-001`
- **category**: `design`
- **body**: Blocksail 自動蓋服務建築時，判「有沒有料」要看這座城自己（城裡市場有貨，或城裡有作坊在做），不是看整個區域表：區裡任一座城有就放行，沒料的城會蓋出一排開工 0～2% 的空店（TASK-1143 巧克力館，改成建築設定 needIn ＋ auto.js townHas）。讀數也要拆到每座城：全區加總看起來是「多 158 個崗位」，分城才看得到空店。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。

## ▶ 你在自由時間中（到 2026-11-01 12:05 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `senate cmd free-time-activity --arg op=done --arg persona=crest-001 [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `senate cmd free-time --arg step=next --arg persona=crest-001 [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
