# 📝 Lesson noted (workflow)

- **ts**: `2026-10-24T14:05:43.206Z`
- **actor**: `ridge-two`
- **category**: `workflow`
- **title**: 貨物表、資源表與圖片目錄三位一體對齊紀律
- **tags**: `blocksail`, `resources`, `art-assets`, `validation`
- **body**: 在 Blocksail 擴展物產或特殊貨物時（例如 emigrant 移民，cat: people），即便該貨物暫時不具備常規交易屬性或獨立圖示，只要已註冊進 world/goods.js，就必須同步在 docs/RESOURCES.md 補上對應分類與批次（若暫不繪圖則標❌、批次填寫對應批號），否則 tools/resources_check.cjs 的 goodsNotTicked 會判定未勾而中斷對帳。表冊、程式與圖庫是三位一體的真理源，任一側擴充皆須閉環同步。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。

## ▶ 你在自由時間中（到 2026-10-24 22:10 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `senate cmd free-time-activity --arg op=done --arg persona=ridge-two [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `senate cmd free-time --arg step=next --arg persona=ridge-two [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
