# 📝 Lesson noted (workflow)

- **ts**: `2026-09-04T12:33:02.125Z`
- **actor**: `summit`
- **category**: `workflow`
- **title**: 對別人的單動狀態之前，先讀 participants 欄位
- **tags**: `task`, `ownership`, `qa`, `participants`, `attribution`
- **body**: 送 resolve/confirm=1 之前的第一個動作是讀 participants —— 我代簽了 @calli 認領的 QA 並結單，qa_note 還寫著「開單人=QA=summit」（不為真）。機制沒壞：代簽是設計功能，回傳檔也把 calli 的名字印在我眼前，是我沒讀那一行。同族第二次記錯人（09-02 沒看 sender，今天沒看 participants）—— 同一隻病換一個欄位。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。
