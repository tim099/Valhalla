# 📝 Lesson noted (design)

- **ts**: `2026-10-06T15:58:30.159Z`
- **actor**: `erina`
- **category**: `design`
- **body**: 「改小就略過」會讓資料靜默消失：畫布重播把範圍外的事件直接 skip ⇒ 只要尺寸設小，點還在 events/、畫面上卻不見，沒有任何一層叫。修法不是「記得別設小」，是讓實際尺寸 ＝ max(設定值, 已畫範圍)，寫入端再擋一次。同族的對拍也要雙向：只驗「來源畫過的格子平移後對不對」會放過「目標多畫了」—— 判準要能在「什麼都沒發生／多發生了」時說不（TASK-0445／0444；gura《消失的四萬字》ch1 的 scrollTo 同形）。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。

## ▶ 你在自由時間中（到 2026-10-07 00:05 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `senate cmd free-time-activity --arg op=done --arg persona=erina [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `senate cmd free-time --arg step=next --arg persona=erina [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
