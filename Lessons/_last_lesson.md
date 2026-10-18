# 📝 Lesson noted (coding)

- **ts**: `2026-10-18T03:11:28.343Z`
- **actor**: `kotoko`
- **category**: `coding`
- **title**: 丟掉一份載入中的 Promise，等它的人還在
- **tags**: `blockside`, `async`, `promise`, `decoSync`
- **body**: 丟掉一份非同步載入時，「不寫進共用表」不等於處理完 —— 還有人在等那個 Promise。
TASK-0682 的 decoSync：船型載到一半換畫質，本小姐讓被丟掉的那一份載完後不寫進 HULLT，可是照樣把它 return 給等的人；開場那一串拿到舊的、接著讀 HULLT[id] ＝ undefined ⇒ Tim 手機上「載入失敗：T.h」。ame 6d7cefb 改成被丟掉的那一份改等換上去的那一份（return loadHull(id)）。
我測了「切換會重載」「同一檔不重載」，沒測「載到一半切換」—— 丟東西的那條路，要量等它的人拿到什麼。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。
