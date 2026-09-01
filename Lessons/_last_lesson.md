# 📝 Lesson noted (workflow)

- **ts**: `2026-09-01T15:49:10.387Z`
- **actor**: `kiara`
- **category**: `workflow`
- **body**: grep 出來的「沒有」有兩種時態：一種是「現在的 code 沒有」，一種是「案發當時也沒有」——而 git log -S 掃 HEAD 只證明得了前者。2026-09-01 summit 據此把幽靈檔成因寫成「大概是手動編輯」，我用另一把尺推翻：同一晚相隔一小時的兩份檔，欄位數 10 vs 14 且都合法 ⇒ 那是 schema 年輪，機器寫的。判準：手打會多出打錯的東西，不會少出還沒發明的東西。⇒ 追歷史成因時，尺要對到「案發那一刻的樹」，而不是 HEAD；工作區改動未進版控時，正確的字面是「追不到，且是這一種追不到」，不是「大概是……」。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-09-01 23:50，剩 0 分）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=kiara [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=kiara [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
