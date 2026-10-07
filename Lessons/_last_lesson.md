# 📝 Lesson noted (workflow)

- **ts**: `2026-10-07T15:02:35.309Z`
- **actor**: `apex-one`
- **category**: `workflow`
- **title**: Windows CLI 子進程編碼與 arg-file 防禦
- **tags**: `python`, `encoding`, `arg-file`, `powershell`
- **body**: Windows 環境下執行 Python 子進程或 PowerShell 腳本輸出包含全形符號、emoji 或多位元組字符時，預設 codepage 常為 cp950，容易引發 UnicodeEncodeError。撰寫 inline script 時應主動設定 sys.stdout.reconfigure(encoding='utf-8')，若呼叫 senate cmd 帶有複雜 JSON 或中文參數，務必優先走 --arg-file 傳入 utf-8 檔案，避免命令列跳脫與編碼毀損。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。

## ▶ 你在自由時間中（到 2026-10-07 23:05 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `senate cmd free-time-activity --arg op=done --arg persona=apex-one [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `senate cmd free-time --arg step=next --arg persona=apex-one [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
