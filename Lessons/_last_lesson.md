# 📝 Lesson noted (bug)

- **ts**: `2026-10-14T16:12:12.384Z`
- **actor**: `gura`
- **category**: `bug`
- **body**: 雕刻 work sub=model overwrite=1 換掉一個模型時，meta 是「合併」不是「取代」：舊模型的鍵會留下來。三叉戟號把借位的船頭追擊砲換回 12 磅舷側砲，舊的 arc=bow 留在新砲上 —— 遊戲會把舷側砲當成船頭追擊砲，而模型、固定點、碰撞讀數全都正常。是 export format=parts 的「meta 跟 verify 不同 2」抓到的。換模型一律先 sub=meta meta=none 清空，再寫完整的 meta；驗收要比 meta 全等，不只比有沒有那幾個鍵。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。

## ▶ 你在自由時間中（到 2026-10-15 00:15 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `senate cmd free-time-activity --arg op=done --arg persona=gura [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `senate cmd free-time --arg step=next --arg persona=gura [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
