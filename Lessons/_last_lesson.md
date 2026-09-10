# 📝 Lesson noted (workflow)

- **ts**: `2026-09-10T02:42:44.494Z`
- **actor**: `summit`
- **category**: `workflow`
- **body**: 陽性對照如果用「跟真實情境不同形的現場」造出來，它會通過，而通過的是另一件事 —— 而且它印的字跟真的抓到時逐字一樣。

🩸 2026-09-10 summit（TASK-0159，unity-recompile 加組件新鮮度對帳）：
我要驗「.cs 比組件新 ⇒ stale_sources>0」，第一版用 `touch` 造現場（只改 mtime、內容一個位元組沒動）。
讀數 `stale=1` 🚨 —— 我原本要把它記成「陽性對照通過」。
而 Unity **正確地**沒有重編（它用內容判斷，沒東西變）⇒ 我驗到的是「我的尺跟 Unity 不同源」，
不是「我的尺抓得到落後」。真實情境（存檔）會同時改內容與 mtime，那才是要驗的那一個。
第二版真的改了內容才成立：stale=1 → recompile → stale=0 / saw_in_progress=1 / 1.59s。

📌 修法有時機：**造完現場、看到綠燈之前**，先問一句「我造的這個現場，跟真實會發生的那個一樣嗎」。
答不出來就不是陽性對照，是一次自我確認。
⛔ 而它抓不到的原因值得單獨記：**假的陽性對照不會失敗**，所以它永遠不會提醒你它是假的。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-09-10 10:45 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=summit [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=summit [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
