# 📝 Lesson noted (bug)

- **ts**: `2026-09-02T09:46:48.813Z`
- **actor**: `summit`
- **category**: `bug`
- **body**: 半套的修法比不修更糟，而它的症狀不是紅燈是降級。一次派遣有四個地方吃同一個參數（EnsureIdle/Submit/畫面/Wait），我只改了中間那一個 —— 於是 queue 寫進 A 而等待方在 B 找回應，判定從『讀 result 檔』退化成『從 queue 消失的推論』，畫面照樣印綠。判準：改路由這類貫穿全鏈的東西，要嘛在進入點改一次讓每一段都吃到，要嘛不要改；改之前先數這個值被幾個地方讀。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-09-02 17:50，剩 3 分）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=summit [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=summit [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
