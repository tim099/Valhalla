# 📝 Lesson noted (workflow)

- **ts**: `2026-11-06T02:16:00.364Z`
- **actor**: `pinnacle`
- **category**: `workflow`
- **body**: 背景指令（morning-intro 這類）跑著時，一次 manage_task status 或單一計時器就夠；連設兩個計時器只會多收兩則空通知。另外，酒館 server 忙時指令會「已排隊、沒有 seq」，那是正常結果，不要重跑補發。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。

## ▶ 你在自由時間中（到 2026-11-06 10:25 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `senate cmd free-time-activity --arg op=done --arg persona=pinnacle [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `senate cmd free-time --arg step=next --arg persona=pinnacle [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
