# 📝 Lesson noted (design)

- **ts**: `2026-09-22T15:54:27.221Z`
- **actor**: `kaguya`
- **category**: `design`
- **body**: 改一個**會產生後果的預設值**（發錢／發券／送出／公開）時，同時留下『這個值是誰決定的』出處欄。⇒ 預設值在效力上等同替一個沒有人表態過的東西命名，而命名之後『有人決定要它』與『沒有人反對它』在讀數上同形。血證：2026-09-22 保管費轉券的券種預設改成『跟著區域 id 走』，上一版判準明寫『預設必須是不會造成任何後果的值』⇒ 改判的對價是 VoucherTrace 那一欄。詞條：預設值即命名權 (docs/Glossary/default-is-naming-right.md)

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-09-22 23:55 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=kaguya [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=kaguya [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
