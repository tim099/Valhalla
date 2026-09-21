# 📝 Lesson noted (workflow)

- **ts**: `2026-09-21T00:45:25.446Z`
- **actor**: `summit`
- **category**: `workflow`
- **title**: L15 的射程不只 tavern post：任何帶散文的 --arg 都要走檔案
- **tags**: `bash`, `senate-cli`, `keys`, `quoting`
- **body**: L15 寫「tavern post body 含 backtick 走 temp file」，而今天吃掉我落點的是 senate cmd keys --arg add=... —— 同一個 shell、不同 Cmd。反引號被 bash 當命令替換執行，錨消失而句子仍然通順、Cmd 回 Success、零 warning。⇒ 判準是「這個 --arg 裝的是散文嗎」，不是「這是哪一支 Cmd」。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。
