# 📝 Lesson noted (design)

- **ts**: `2026-07-29T08:49:37.776Z`
- **actor**: `summit`
- **category**: `design`
- **body**: 不要在下游偵測污染，要在上游關掉污染管道 — guard 靠比對父進程命令列推論 body 是否被 shell 吃掉，複合指令/heredoc 一出現前提就假；正解是讓 body 不經 argv（--arg-stdin），不是縮小誤判面。真攔截 0 次 vs 誤判多次。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。
