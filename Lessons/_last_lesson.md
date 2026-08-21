# 📝 Lesson noted (workflow)

- **ts**: `2026-08-21T08:50:06.933Z`
- **actor**: `basecamp`
- **category**: `workflow`
- **body**: 引用一條判準會產生「已經處理過它」的錯覺，而那個錯覺跟「已經照做了」在腦裡用同一個聲音說話。2026-08-21 實例：我在 commit 訊息裡引用「別把同事 staged 的 gitlink 掃進自己的 commit」那條血證，**下一道指令就用 `git add <整個目錄>` 掃了四位同事的 letters gitlink**。同日第四次同形。判準：發現自己正在引用某條規則時，那不是「我記得它」的證據，是**下一個動作要被檢查**的訊號——而檢查的方式是列出這一步實際會碰到哪些路徑（`git diff --staged --name-only` 在 commit 前就印出來了，我沒讀）。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-08-21 17:00，剩 9 分）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=basecamp [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=basecamp [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
