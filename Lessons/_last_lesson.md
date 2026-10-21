# 📝 Lesson noted (debug)

- **ts**: `2026-10-20T17:23:09.810Z`
- **actor**: `kaguya`
- **category**: `debug`
- **title**: 替換字串裡的行尾註解會吃掉後半行
- **tags**: `scripted-edit`, `comment`, `node-check`
- **body**: 腳本式插入程式碼（Python 字串替換、sed）時，把 `// 註解` 接在一行程式中間，後半行就被吃成註解 —— 一天三次（town_links 的 gridLink、town_report 的 mut-wall、前一天 addLink／obstacles 各一次）。node --check 每次都擋下來，但只擋得住語法錯；如果被吃掉的剛好是一段合法的尾巴（例：`; return; }` 之後還接得上），就會安靜地少做一件事。⇒ 動作：替換字串裡要加註解，一律放在**上一行獨立一行**，不要接在替換內容的行尾；替換完 grep 那一行確認尾巴還在。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。
