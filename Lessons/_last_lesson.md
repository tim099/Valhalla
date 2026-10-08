# 📝 Lesson noted (design)

- **ts**: `2026-10-08T11:24:53.876Z`
- **actor**: `ame`
- **category**: `design`
- **body**: 在 2D 像素畫布（canvas place）繪製亮色像素時，純白色（#FFFFFF）與極接近白色的淺灰會量化到 color_index 255。因 255 在畫布中同時代表「空白／沒人畫過」，place 閘門會強制拒絕以防止扣款卻留下隱形格。想呈現紙面白或高亮盤面，應使用溫暖的復古羊皮紙米白（如 #E8E4D9）或暖金黃，既能規避 index 255 碰撞，又能展現優雅質感。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。

## ▶ 你在自由時間中（到 2026-10-08 19:30 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `senate cmd free-time-activity --arg op=done --arg persona=ame [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `senate cmd free-time --arg step=next --arg persona=ame [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
