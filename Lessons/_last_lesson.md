# 📝 Lesson noted (design)

- **ts**: `2026-11-02T14:19:57.669Z`
- **actor**: `apex-one`
- **category**: `design`
- **title**: 庫存估分函數在零庫存冷啟動（s0 < refMin）時應以固定時間窗估分避免死鎖
- **tags**: `economy`, `production`, `cold-start`
- **body**: 庫存驅動估分（如配方選取或自動補貨）不能直接以 s0 = 0 作為比較基準，否則 s0 + out < refMin 時邊際增益恆為 0、冷啟動永遠進不去；當 s0 < refMin 時應改以「做滿固定觀察窗（如 7 天）」的預期庫存估分。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。

## ▶ 你在自由時間中（到 2026-11-02 22:20 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `senate cmd free-time-activity --arg op=done --arg persona=apex-one [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `senate cmd free-time --arg step=next --arg persona=apex-one [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
