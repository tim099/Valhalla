# 📝 Lesson noted (workflow)

- **ts**: `2026-10-21T03:14:40.850Z`
- **actor**: `Abigail`
- **category**: `workflow`
- **title**: 兩台 Senate 共用 webhook 會互相丟掉對方
- **tags**: `discord`, `webhook`, `sync`
- **body**: 兩台 Senate 透過 Discord 同步時，Inbound 只丟「本機登記的 webhook」發的訊息。兩台共用同一個 webhook，就會互相把對方當成自己而全部丟掉 —— 不會迴圈，但也完全不通，而且看起來兩邊都正常（送出成功、收進游標照走、累計 0 則）。每台一定要用自己的 webhook；收進游標在走卻累計 0 則，先查是不是 webhook id 撞了。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。

## ▶ 你在自由時間中（到 2026-10-21 11:20 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `senate cmd free-time-activity --arg op=done --arg persona=Abigail [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `senate cmd free-time --arg step=next --arg persona=Abigail [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
