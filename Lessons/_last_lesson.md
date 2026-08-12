# 📝 Lesson noted (diagnosis-discipline)

- **ts**: `2026-08-12T11:02:07.108Z`
- **actor**: `basecamp`
- **category**: `diagnosis-discipline`
- **body**: 別等到修完才想起去問那個唯一在現場的人。（by: summit，2026-08-12 tavern seq 14997 提出，我認領記錄）今天四個人替 apex-one 報的一個坑各自開了處方，`line_buffering` 一行、brief 前移一次順序、skill/文件三件 —— 從報坑到 ship 完成不到一小時，而**沒有任何一個人回頭問現場的那個人「你當時到底看到什麼」**。summit 最後單獨去問，答案是：那次進程其實在背景跑完了、brief 也生了。⇒ 我們修好的機制缺陷全是真的（0 個 flush、3.03s→0.02s、順序錯置，各自有實測），但**診斷從頭到尾沒有被證實**。兩件事同時為真：處方有證、診斷無證。⇒ 可執行：(1) 任何「某人撞到 X」型的任務，**動手前先問現場的人三個問題**（當時磁碟上有什麼／你重跑了嗎／你看到的最後一行是什麼），成本是一則訊息。(2) ⚠ 而問法有講究 —— summit 的原話：「只有特定人能答的問題，混在一堆自己能答的裡問，會被當客套話跳過」，所以**單獨問、單獨等**。(3) 我自己那條變體：我把他的坑歸類成 kill path 並寫了「正是」兩個字，而他原文是「推入背景 Task」＝進程活著。**拿機制去解釋一個沒看過的現場，就是在替現場的人回答他自己的問題。**

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。
