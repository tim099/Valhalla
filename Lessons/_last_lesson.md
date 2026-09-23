# 📝 Lesson noted (workflow)

- **ts**: `2026-09-23T07:10:00.889Z`
- **actor**: `summit`
- **category**: `workflow`
- **body**: 要打出『沒有／零／找不到』之前，先問那把尺**量得到它嗎** —— 2026-09-23 我一天造了四個假零，四個都不是資料錯，是量具沒對準受詞：① 量 pending.trigger 判斷有沒有委派，而那個路徑根本沒有這個檔；② glob 寫 queue-*.json，那個 dash 正好把真正的 queue.json 排除掉；③ 收探針時 glob 寫小寫 probe*，而工具會把首字大寫成 Probe* ⇒ rm 什麼都沒刪，而同樣小寫的對帳 grep 印『殘留 0』；④ 跑 coding op=list 查施工場，而 list 不是合法 op ⇒ 它 exit 2 印一行錯誤，我的 grep 在那行上得 0，於是把『指令失敗』讀成『沒有場』——場其實一直開著。⇒ 共同形狀：**打錯的指令與查無此項，在 grep／glob 下游長得一模一樣**。而救到我的兩次差別只有一件事：我先餵那把尺一個保證存在的答案（ctypes 獨佔握檔後第二次開回 ERROR_SHARING_VIOLATION；先跑一支已知會委派的 ucmd 看 mtime 會不會動）。⇒ 動作＋時機：**空結果不是讀數，除非你先證明那把尺在非空時會說話。**

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。
