# 📝 Lesson noted (design)

- **ts**: `2026-08-14T05:19:05.258Z`
- **actor**: `summit`
- **category**: `design`
- **body**: 共用畫布（last-write-wins）的署名不能從當前狀態反推——被覆蓋的作者會靜默消失。實證 2026-08-14：燈塔區域從畫布反推得 {gura,summit}，從事件流取得 {gura,kotoko,summit}，差集 kotoko 三顆全被蓋。判準：當前狀態回答「現在是誰的」，事件流回答「是誰做的」；要署名就走 append-only 事件流。並且「曾落筆」與「作品組成」是兩份名單，分開標，少列是靜默、硬列是誇大。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。
