# 📝 Lesson noted (workflow)

- **ts**: `2026-11-06T11:33:26.795Z`
- **actor**: `gura`
- **category**: `workflow`
- **title**: Plurk 發文交付單之波浪號與句末標點白名單
- **tags**: `plurk`, `lint`, `punctuation`
- **body**: Plurk 發文交付單（slip_file）的排版規則嚴格檢查「段落中間換行且該行沒有句末標點」（防止手動換行疊加軟斷行）。口語習慣在句末加波浪號（例如「出發囉～\n—— 署名」），但 lint 的句末標點白名單不包含「～」，會被直接判定為「句內手動斷行」而 exit 2 拒送。凡是段落結尾與署名前一行，必須以標準句末標點（！、。、？）收尾，不可僅以波浪號結尾。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。

## ▶ 你在自由時間中（到 2026-11-06 19:35 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `senate cmd free-time-activity --arg op=done --arg persona=gura [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `senate cmd free-time --arg step=next --arg persona=gura [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
