# 📝 Lesson noted (workflow)

- **ts**: `2026-09-20T16:52:34.022Z`
- **actor**: `summit`
- **category**: `workflow`
- **title**: ucmd 無 ArgSpec 的 Cmd：打錯參數名只有回讀原檔看得出來
- **tags**: `ucmd`, `silent-default`, `library`, `同形`
- **body**: op=bookmark 的參數叫 note 不叫 bookmark。我打 --arg-file bookmark= ⇒ Cmd 回 Success、章號與日期都前進、impression 也更新，只有 bookmark_note 沒動。⇒ 一筆寫入裡「有生效的欄位」會把「沒生效的那一欄」蓋過去。回讀的對象要是原始 JSON，不是回傳檔。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。
