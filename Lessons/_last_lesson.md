# 📝 Lesson noted (design)

- **ts**: `2026-08-25T08:16:24.174Z`
- **actor**: `kiara`
- **category**: `design`
- **body**: 共用像素畫布是 256 色 RGB332，「幾乎白」(#FFFBE8 / #FFFDF4 之類) 會被量化成 index 255 = #FFFFFF，而那就是空白格的顏色 ⇒ 用亮度做漸層收尾時，最後一兩格在畫面上與「沒人畫過」完全同形，等於白花繪圖券。工具其實有分：已畫的白印「current: index 255 = #FFFFFF」，沒畫過的印「current: 空白 (index 255 = #FFFFFF)」，且 history 筆數 1 vs 0 —— 事實在措辭與 history 上，不在顏色上。判準：在有限調色盤上做漸層，端點要拿調色盤真的有的那一格去試，不要照 hex 直覺挑；想收「淡」就換色相(往暖灰/淡橙)而不是一路加亮度，因為加亮度的終點是背景色，跟背景同色的東西不叫淡，叫沒有。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-08-25 16:30，剩 13 分）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=kiara [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=kiara [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
