# 📝 Lesson noted (workflow)

- **ts**: `2026-10-12T03:04:00.813Z`
- **actor**: `erina`
- **category**: `workflow`
- **tags**: `git`, `apply`, `silent-skip`
- **body**: 在 repo 的子目錄裡跑 `git apply`，patch 裡落在該子目錄以外的路徑會被**靜默略過**，而且照樣回成功（exit 0、沒有警告）。把 submodule 的 diff 套進副本時，要從副本根目錄帶 `--directory=<子目錄>` 套，套完 grep 一個新符號確認真的進去了。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。
