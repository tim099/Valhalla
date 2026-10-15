# 📝 Lesson noted (bug)

- **ts**: `2026-10-14T23:46:49.991Z`
- **actor**: `Sirius`
- **category**: `bug`
- **tags**: `sculpture`, `sail`, `corners`, `free`
- **body**: 雕刻 work sub=sail 換 corners 並帶 overwrite=1 時，原來 free 的角會重新變成 pin=true；保留帆腳物理時要同時顯式帶 free=<原自由角名>。2026-10-15 潮墓號後桅上帆改兩個帆頭綁點，整份 sails.json 逐欄讀回抓到 clew-P/S 意外釘死，補 free=clew-P,clew-S 後確認只有兩個 at 改變，其他欄位與 meta 完全相同。不能只驗 corners 字串或 exit 0。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。
