# 📝 Lesson noted (workflow)

- **ts**: `2026-08-23T15:16:10.617Z`
- **actor**: `summit`
- **category**: `workflow`
- **body**: 「兩個 renderer 互為證人」這句只有在**有人真的去看另一個 renderer** 時才成立。🩸 2026-08-23：ImGui 的 Row 對每個子節點都 SameLine（含群組），展開的下拉整疊疊在鈕上面；而文字 renderer 當時的規則是「遇群組換行」⇒ 同一棵樹在文字模式完全正常。我只看文字那個，所以那個「證人」從來沒出過庭 —— 抓到它的是 Tim 的截圖。⇒ 一般形：**冗餘的驗證管道不會自動生效，它只在被讀的時候才是管道**；沒被讀的第二個 renderer / 第二份 log / 第二套測試，跟不存在同形，而它還會讓人有「我有兩個證人」的錯覺。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-08-23 23:20，剩 3 分）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=summit [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=summit [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
