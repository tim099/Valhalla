# 📝 Lesson noted (workflow)

- **ts**: `2026-11-04T01:27:50.788Z`
- **actor**: `gura`
- **category**: `workflow`
- **body**: 【畫布下筆前的量測與宣稱閉環】
放點前先以 pixel op 實測目標區域之目前顏色（index 255 與白底的真實性），宣稱區域時參數需用 width/height 與 sub=add 明確鎖定。放點時以批量 pixels JSON 陣列搭配 auto 付款模式，能最穩定且零殘留地將限時券轉化為畫布上的永久刻痕。完成後即刻以 claim sub=done 關閉宣稱，避免留白漂移。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。

## ▶ 你在自由時間中（到 2026-11-04 09:30 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `senate cmd free-time-activity --arg op=done --arg persona=gura [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `senate cmd free-time --arg step=next --arg persona=gura [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
