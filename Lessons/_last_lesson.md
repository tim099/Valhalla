# 📝 Lesson noted (workflow)

- **ts**: `2026-09-11T04:09:00.758Z`
- **actor**: `calli`
- **category**: `workflow`
- **body**: 自己列的檢查清單會定義自己看得見什麼 —— 一把只看得見自己列出那幾根軸的尺，在漏軸時的輸出跟「完全相同」一模一樣。2026-09-11 calli：列了 JSON 格式「三根軸」（行尾/縮排/冒號空格）驗兩個寫入端同不同形，實際有五根（另有陣列括號位置、空容器渲染），而那把尺量不到自己漏的兩根（它只讀第 2 行）。抓到它的是 git diff -w —— 一個跟主尺不同源的反向對照。⇒ 判準：驗收用逐位元組比不用軸表比；宣告「驗過了」之前多留一行不經過同一隻手、也不經過同一張清單的讀數。這是「第二把尺不等於第二個人」的延伸：清單也算一隻手。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-09-11 12:10 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=calli [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=calli [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
