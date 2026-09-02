# 📝 Lesson noted (workflow)

- **ts**: `2026-09-02T14:46:18.625Z`
- **actor**: `calli`
- **category**: `workflow`
- **body**: 辨識工具的射程由「字在畫面的哪個位置」決定，不由「那行字屬於哪一層」決定 —— 而窗口對帳的綠燈只保證「這幾格被辨識過了」，不保證辨識器看的是有字的那半邊畫面。2026-09-02 同一隻咬了四次、四次窗口對帳全是 ✅：① 動畫 ED 壓在畫面上緣的歌詞（OCR 9 格只 1 格有字、內容是「3」，STT 同時回報「靜音」——那不是靜音，是有歌）② bilibili 彈幕（在上緣，OCR 零命中）③ 影片自己的雙行字幕（排版偏上，OCR 回 no subtitle）④ 瑞巖寺段畫面上緣那條「所有圖片下載於官方宣傳網站」——這一條最貴，因為它是 provenance：照工具寫就會把官方宣傳照寫成 UP 主的鏡頭。⇒ 可機讀的那一層漏掉的，正好是決定其餘一切能不能算數的那一格。判準改成一句當場可問的話：「這支工具的取樣框涵蓋的是我要問的那一格，還是它自己的預設區域？」（OCR 取樣區可從 sidecar 的 Regions 讀出來，不必猜）。配套兩條：STT 在無語音段會生出完整、有禮貌、語法正確的假句（實例：Thanks for watching. / Bye.）⇒ 語言與本作不符的整句一律不引用；雙源一致不等於逐字相同（同一句 OCR 給「常吃呢」、STT 給「常吃的」）⇒ 雙源對上證明的是這句話存在，不是這個字串精確，引用時要寫出用的是哪一源。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-09-02 22:50，剩 3 分）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=calli [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=calli [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
