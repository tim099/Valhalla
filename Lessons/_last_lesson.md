# 📝 Lesson noted (workflow)

- **ts**: `2026-09-22T08:51:37.994Z`
- **actor**: `calli`
- **category**: `workflow`
- **body**: 整支重寫檔案之後，要問的不是「行尾對不對」，是「檔首那三個 byte 呢」—— 兩根軸裡有守衛的只有一根。2026-09-22 血證：dev 用 python 重寫兩支 .cs，警覺到重寫風險、跑對照組、落到 byte 層複驗行尾（CRLF=212／孤立 LF=0），那一步做對了；而同一次重寫順手加上的 BOM 逃掉了，因為它不在那張檢查表的軸上。更刺的是 .gitattributes 自己寫著「BOM 是內容不是行尾，git 不動它」：行尾有 text=auto 兜底（repo 一律存 LF，工作區 CRLF 進不了 index），BOM 沒有任何一層兜。全庫 152 支 .cs 有 BOM 的正好就是被重寫的那 2 支。最便宜的尺：git show <sha>:<path> | head -c3 | od -An -tx1 跟父 commit 並排。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。
