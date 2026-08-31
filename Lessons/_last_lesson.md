# 📝 Lesson noted (design)

- **ts**: `2026-08-31T10:20:11.325Z`
- **actor**: `calli`
- **category**: `design`
- **body**: 狀態機的重置不能放在「只有在命中路徑上才會被呼叫」的函式裡 —— 2026-08-31 血證：Slide 的「放開即中斷」寫在 ClickTypeAsset.CheckSlide 裡，而那支只在 Match 命中那一筆時才被呼叫；放開那一幀 Match 依清單順序先命中排在前面的 Click 並 first-hit 早退，下一幀 ClickInfo.Clear() 清空 initAreas 使呼叫端早退 ⇒ active 永遠停在 true，第二次按下直接跳過啟動距離門檻，拿新位置去比上一次手勢留下的量測起點。症狀是「第二次以上不受啟動距離限制」且不報錯。判準：重置必須放在每幀無條件執行的位置，不是放在判定函式裡 —— 判定會被短路，重置不該跟著被短路。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。
