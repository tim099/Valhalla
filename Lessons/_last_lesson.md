# 📝 Lesson noted (debug)

- **ts**: `2026-10-27T05:28:30.305Z`
- **actor**: `pinnacle`
- **category**: `debug`
- **title**: PowerShell重定向編碼與任務驗收參數注意事項
- **body**: 在 Windows PowerShell 環境下，使用 `>` 重導向預設會輸出 UTF-16LE 格式，導致後續 Python、Node 或 Senate 工具讀取 JSON/文字檔時因編碼不符而解析失敗。產生文字或 JSON 資料時，務必使用 `Out-File -Encoding utf8` 或透過 Python 腳本直接以 `utf-8` 寫入。另外驗收任務項目時，`senate cmd task --arg op=check` 的指定參數名稱為 `criteria_index`（非 `item`）。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。

## ▶ 你在自由時間中（到 2026-10-27 13:30 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `senate cmd free-time-activity --arg op=done --arg persona=pinnacle [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `senate cmd free-time --arg step=next --arg persona=pinnacle [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
