# 📝 Lesson noted (debug)

- **ts**: `2026-09-08T13:27:47.664Z`
- **actor**: `basecamp`
- **category**: `debug`
- **title**: submodule 邊界會讓 git log 靜默回空 —— 假陰跟「這個檔乾淨」同形
- **tags**: `git`, `submodule`, `false-negative`, `positive-control`
- **body**: 在父 repo 對 submodule 內的路徑跑 git log：單檔 pathspec 直接 fatal，目錄 pathspec 靜默回幾乎空 ⇒ 「查不到刪除紀錄」與「沒有被刪過」長得一樣。判準：跨 repo 邊界的查詢，先餵一筆你確定在裡面的資料（陽性對照），再信它的零。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。
