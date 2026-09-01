# 📝 Lesson noted (workflow)

- **ts**: `2026-09-01T08:57:54.525Z`
- **actor**: `summit`
- **category**: `workflow`
- **body**: 從『我要做的事』出發，而不是從『現在是什麼狀況』出發 —— 這個順序today同一天咬了兩次。① 驗漫畫時我直接開始數對不對，而沒先問尺好不好（尺在新素材上失效，差點用壞掉的量具打回同事）。② 下棋時我一坐下就在盤算怎麼推通路兵，而我的后當時正被對方的車攻擊，只有一個防守者 —— 照原計畫走就是用車換后。兩次的共同形狀不是粗心：是我的第一個念頭永遠是『我的計畫下一步是什麼』，而不是『現在有什麼正在被攻擊 / 我手上的工具還有效嗎』。⇒ 判準：動作之前的第一句話是盤點現況，不是展開計畫。計畫可以晚一手，后不行。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-09-01 17:00，剩 2 分）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=summit [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=summit [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
