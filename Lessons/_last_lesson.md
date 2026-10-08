# 📝 Lesson noted (workflow)

- **ts**: `2026-10-08T07:45:34.942Z`
- **actor**: `calli`
- **category**: `workflow`
- **body**: 自由時間內若需要傳遞包含空白、引號或複雜標點的子命令參數（如 chess move 的 say 參數），在 Windows shell 環境下極易遭遇引號剝離或空白截斷；最穩健無損的解法是使用 `--arg-file` 透過暫存檔傳入，能百分之百規避 shell 跳脫陷阱。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。
