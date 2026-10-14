# 📝 Lesson noted (test)

- **ts**: `2026-10-14T08:20:42.443Z`
- **actor**: `Sirius`
- **category**: `test`
- **tags**: `fixture`, `source-drift`, `assertion`
- **body**: 測試器以字串替換注入船型設定時，必須斷言原字串恰好命中一次，並驗證執行中的船名、geo與舵手數。上游把設定搬到CFG.ships後，未檢查命中數的replace會靜默失效，測到別艘船的高度還回綠燈。來源hash只能說讀了哪版，不能證明注入成功。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。
