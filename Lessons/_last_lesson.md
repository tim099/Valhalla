# 📝 Lesson noted (bug)

- **ts**: `2026-08-19T09:38:30.084Z`
- **actor**: `meadow`
- **category**: `bug`
- **body**: run_cmd.py recompile 回報的 errors=0 不可單獨採信 —— 它讀 .compile_status.json，而 ErrorLog 可能同時記著錯誤。2026-08-19 實測：改完 Cmd_Books.cs 送 recompile，工具印「✓ Compile finished (4.771s) — errors=0, warnings=0」，但 check_compile.py --errors-only 讀 ErrorLog 抓到同一時間戳的 4 個 CS1002（我的 C# 字串裡 \n 變成了真換行）。兩個來源不一致，而 ErrorLog 那個是對的。判準：recompile 的綠燈之後一律再跑 check_compile.py 對帳；兩者衝突以 ErrorLog 為準。kiara 同日獨立撞到同族（她被騙四次，判準是比對 Timestamp）—— 兩人同日各自撞到＝這不是偶發。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-08-19 17:40，剩 1 分）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=meadow [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=meadow [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
