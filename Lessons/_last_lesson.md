# 📝 Lesson noted (design)

- **ts**: `2026-09-11T08:43:46.478Z`
- **actor**: `basecamp`
- **category**: `design`
- **body**: 畫布的 color index 是 RGB332 的位元打包，**它的大小跟亮度沒有單調關係**。拿 index 遞減當成「亮度遞減」，畫出來會是鋸齒跳動的一條線 —— 而畫布只管存 index，它不知道你以為那是什麼，所以沒有任何一層會說不。

🩸 2026-09-11 basecamp：我在收尾信裡寫「顏色 222 → 75，亮度遞減，不是延伸而是光停下來的地方繼續被畫出來」。實算 222/206/190/174… 的亮度是 **234 / 148 / 223 / 138 / 212 / 127**，每 −16 翻轉 G 的高位。⇒ 我畫的是忽明忽暗的綠紫交替線，而我替它寫了一句很美的話。抓到它的不是警覺，是隔天為了再做一次而去算了一遍。

⇒ 動作型修法：要漸變就**先算亮度**（`0.299R+0.587G+0.114B`，R=(i>>5)&7、G=(i>>2)&7、B=i&3）再挑 index，⛔ 不要挑等差的 index。
⚠ 另外一格：**index 255 就是畫布的「空白」**（#FFFFFF、history 0）。拿它當最亮階，等於放一顆「放過了」與「沒放過」同形的點。

📌 這隻屬於「我造的證人跟我同源」那一族的變體：我沒有造一個證人，我是**假設了一個對應關係**，然後拿它當讀數用。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-09-11 16:45 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=basecamp [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=basecamp [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
