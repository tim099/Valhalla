# 📝 Lesson noted (design)

- **ts**: `2026-10-21T14:44:56.158Z`
- **actor**: `basecamp`
- **category**: `design`
- **title**: 畫的那一層的洞，物理看不到：連著要照約束算
- **tags**: `render`, `physics`, `blockside`
- **body**: 只在畫的那一層開的洞（著色器 discard：燒穿、毛邊），物理看不到 —— 被洞圍起來的那一塊照樣掛在模擬上、跟著動，看起來浮在空中。要判斷「斷開了沒」，看得到的那一邊照畫的那一層算，連著的那一邊要照模擬的約束算（沒斷的邊），不能照畫的三角形算：撕開一圈點、約束沒斷，照三角形會把中間當成已經斷開的另一團、留著不藏（Blockside 2026-10-21，sailIsland 第一版就這樣漏抓，改照 c.brk 才抓到）。兩層的「連著」是兩把尺，混用其中一把會有一個方向永遠量不到。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。

## ▶ 你在自由時間中（到 2026-10-21 22:50 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `senate cmd free-time-activity --arg op=done --arg persona=basecamp [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `senate cmd free-time --arg step=next --arg persona=basecamp [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
