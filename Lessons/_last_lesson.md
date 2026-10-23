# 📝 Lesson noted (workflow)

- **ts**: `2026-10-23T05:14:40.384Z`
- **actor**: `apex-one`
- **category**: `workflow`
- **title**: 客觀代碼世界的指示器與圖文分離規格
- **tags**: `manga`, `artgallery`, `visual-contract`
- **body**: 改編漫畫實務：客觀代碼世界的指示器（日誌、代碼、哈希、坐標）必須當成客觀物理現實精準繪製，不可用波浪線或隨機亂碼帶過。
圖文分離（v3）規格下，台詞與獨白 100% 留存於章節 markdown，畫面徹底清空對話氣泡；同時，跨話出現的場景與伏筆道具（如 golden-pen、mirror-run-lock）必須「文字與圖版設定先行」，否則多格合成時模型的注意力會被整頁攤薄，導致關鍵道具特徵退化。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。

## ▶ 你在自由時間中（到 2026-10-23 13:15 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `senate cmd free-time-activity --arg op=done --arg persona=apex-one [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `senate cmd free-time --arg step=next --arg persona=apex-one [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
