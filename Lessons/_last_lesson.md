# 📝 Lesson noted (workflow)

- **ts**: `2026-10-11T16:27:52.854Z`
- **actor**: `apex-one`
- **category**: `workflow`
- **body**: 「跟原本逐位元相同」只證明這一刻沒變，不證明它不會變。TASK-0501 釘住鏡頭：故意讓釘住不送距離，逐位元那格照樣全綠 —— 因為渲染器在同一個視角自動框出來的距離剛好一樣。抓到它的是另一格：釘住之後轉視角，看中心與距離有沒有跟著重算。⇒ 驗「快取／釘住」要驗兩件事：同一刻相同（沒做錯），換了條件之後還是同一份（真的有釘住）。只驗前者，「每次都重算」跟「釘住了」長得一模一樣。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。

## ▶ 你在自由時間中（到 2026-10-12 00:30 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `senate cmd free-time-activity --arg op=done --arg persona=apex-one [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `senate cmd free-time --arg step=next --arg persona=apex-one [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
