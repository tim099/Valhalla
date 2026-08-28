# 📝 Lesson noted (workflow)

- **ts**: `2026-08-28T08:14:27.320Z`
- **actor**: `kiara`
- **category**: `workflow`
- **body**: 一個「哪一半壞了」的問題，最快的尺是**找出哪一半還好**——而那把尺常常在使用者手上，不在我手上。2026-08-28 實測：我接上 ImGui 的剪貼簿 callback，兩層自我對拍全過、函式指標讀回非零，而 Tim 回報 Ctrl+V 還是貼不上。我正打算往「marshalling 是不是寫錯了」那半深挖（那半有非受管記憶體、UTF-8 結尾、delegate 存活期，最貴也最可疑）。**是他補的一句「但是按鈕的貼上 OK」把範圍切開的**——那顆鈕跟 Ctrl+V 吃同一份剪貼簿實作，所以那一句一次排除了 Win32 讀取、宿主能力委派、marshalling 三整段，剩下唯一嫌疑是「ImGui 收不到那個組合鍵」。查下去果然是 Silk.NET 的 ImGuiController 從來沒送 modifier（metadata 裡完全沒有 ModCtrl，只有 get_KeyCtrl），於是所有 Ctrl 組合鍵無效而單獨打字正常——兩者症狀不同形，正是它難被發現的原因。判準：收到「X 不能用」的回報時，第一個問題不是「X 哪裡壞了」而是**「跟 X 共用實作的那些東西，哪些還好？」**——每一個「還好」都砍掉一整段搜尋空間，而使用者通常已經知道答案，只是不知道那是答案。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-08-28 16:20，剩 5 分）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=kiara [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=kiara [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
