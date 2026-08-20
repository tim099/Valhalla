# 📝 Lesson noted (design)

- **ts**: `2026-08-20T10:54:19.307Z`
- **actor**: `basecamp`
- **category**: `design`
- **body**: 被 Cmd 代跑的工具內部再「等」另一個 Cmd 完成＝Editor 等 python、python 等 Editor 的雙向自鎖；修法：fire-and-forget（submit 不 wait）＋獨立 --lane 子通道（主 lane 正被代跑中的 Cmd 佔住，ensure_idle 會空等到 timeout）。血證：canvas.py 自動分享 2026-08-20 設計期抓到

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-08-20 19:00，剩 5 分）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=basecamp [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=basecamp [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
