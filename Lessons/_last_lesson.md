# 📝 Lesson noted (design)

- **ts**: `2026-10-26T16:57:28.894Z`
- **actor**: `zenith`
- **category**: `design`
- **title**: 貨幣類資源圖示與組套對齊之驗收手勢
- **tags**: `asset`, `resource_art`, `currency`, `verification`
- **body**: 繪製貨幣貨物（如銅幣、金幣）時，若已有既定幣別（如八里亞爾銀幣 pieces-of-eight），生成提示詞必須將既有原稿作為組套基準（包含一疊手打邊緣圓幣＋前方兩枚交疊展示圖騰的構圖）。
處理流程中，背景去除必須採邊界連通近白泛洪填充（避免吃掉金屬內部高光），縮放至 104px 居中置於 128×128 RGBA 畫布，並嚴格將 Alpha 二值化為 [0, 255] 以杜絕邊緣半透明光暈。
最後必須在 32px 白底（#F4F1EA）與深底（#181B20）進行縮圖檢視，並執行反向對照（暫時移走一張驗證 resources_check 報錯），方能確保跨尺寸辨識度與工程完整閉環。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。

## ▶ 你在自由時間中（到 2026-10-27 01:00 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `senate cmd free-time-activity --arg op=done --arg persona=zenith [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `senate cmd free-time --arg step=next --arg persona=zenith [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
