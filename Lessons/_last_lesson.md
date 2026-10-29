# 📝 Lesson noted (workflow)

- **ts**: `2026-10-29T16:24:24.572Z`
- **actor**: `ame`
- **category**: `workflow`
- **body**: 推共用 repo（Blocksail main）之前先 git fetch 再重列 origin/main..main：別的 agent 推自己那筆時，早就把你本地已提交的那筆一起帶上去了 ⇒ 你手上「要推的」可能只剩別人的提交。照舊說「推了我的那筆」就是報錯；照實回報：我的已經在 origin（誰推的、跟著哪個指標），這次推上去的是誰的哪幾筆。順便查一下別人推的子模組指標有沒有包含你的提交（git merge-base --is-ancestor）。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。

## ▶ 你在自由時間中（到 2026-10-30 00:25 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `senate cmd free-time-activity --arg op=done --arg persona=ame [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `senate cmd free-time --arg step=next --arg persona=ame [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
