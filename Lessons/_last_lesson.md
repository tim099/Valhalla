# 📝 Lesson noted (general)

- **ts**: `2026-08-16T15:53:12.052Z`
- **actor**: `unknown`
- **category**: `general`
- **body**: 查證「這樣改行不行」時，我讀到「機制存在」就停手，而沒有問下一句「那個機制的**時序**是什麼」。

🩸 2026-08-16 血證（summit）：把 run_cmd 的 queue 改成 per-persona 自動路由，並對 Tim 說
「C# 不必改，我查證過」。我確實讀了 code —— 讀到 `ListAgentIds()` 會列舉每個 queue 資料夾、
watcher 會對每個 id 輪詢，於是結論「路由得到 ⇒ 安全」。

**我沒有問：那些 id 是輪流跑，還是同時跑。**

補讀後：watcher 是 `foreach (id) TryDispatchAgent(id)`（不等前一個完成），重入閘 `s_RunningAgents`
是 per-agent ⇒ **不同資料夾真的併行**。而 Runner 的 per-cmd 回傳槽是全域單例
（`s_CurrentCmdOutputs` / `s_CurrentCmdValues` / `Cmd_Tavern.LastPostSeq` …）——
全員擠同一條 lane 時它們**因為不可能併行而安全**，
**分流正是把潛伏 bug 變成活 bug 的那一步。**

⇒ 判準：**「機制存在」與「機制的時序」是兩個問題，而我只問了第一個就宣告查證完畢。**
凡是「把東西分開跑」的改動，必問三句：
① 分開之後會不會同時跑？
② 同時跑的話，有哪些狀態是「一次一筆」假設下才成立的？
③ 那些狀態壞掉時**會不會出聲**？（若答案是「值仍然合法」⇒ 不會出聲 ⇒ 必須先修）

⚠ 而同一格 @basecamp 當天早上已寫在 `Plan_Cmd_Concurrency_Hardening.md`，
她初版寫「路由零風險」再自己推翻，把順序釘死為「per-cmd context 先於路由」。
**我沒讀那份 plan 就動手，原樣復現了她推翻掉的版本。**
⇒ 附帶判準：**動共用管線之前先 grep 有沒有人寫過 plan** —— 別人推翻過的結論比我的新推論便宜太多。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。
