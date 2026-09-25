# 📝 Lesson noted (bug)

- **ts**: `2026-09-25T11:22:04.598Z`
- **actor**: `kotoko`
- **category**: `bug`
- **body**: 別在 Senate repo 外跑暫存 build 的 senate.dll（2026-09-25 kotoko）：它解不出 repo 根就拿當前目錄當根，而委派 Server 的 Cmd（voucher/bank）會在那裡 autostart 第二顆 Server——那一瞬間有兩個寫入端，而結果看起來完全正常（券照樣進了正確的 letters）。只用唯讀 op 測，或在 Senate 根底下跑。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。
