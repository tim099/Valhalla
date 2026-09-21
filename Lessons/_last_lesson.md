# 📝 Lesson noted (workflow)

- **ts**: `2026-09-21T08:43:12.732Z`
- **actor**: `kiara`
- **category**: `workflow`
- **body**: 一個系統自己會回答的問題，不要用通用工具去猜它的答案。grep 不是 parser、ls -t 不是單號查找、diff 不是內容比較、str.replace 不是保證套用——它們回答的是自己那個問題，而繞過系統自己的入口拿到的會是一個格式正確、數字合理、卻回答錯問題的答案。2026-09-21 kiara 同一天被咬 6 次：regex 把註解裡的 [HelpURL] 示範數成真 attribute；replace 沒命中錨點靜默 no-op 而腳本照印 patched；diff 把行尾差異報成全檔 69 行不同（差點報一個不存在的分叉）；ls -t 撈到別人同分鐘開的單；grep -c 數出 5 格未勾而工具 parser 說全部都勾了（差點把簽名蓋在任務描述上）；讀了 FillRootArg 的呼叫行就寫驗收條文，而那個函式上面兩行的 early return 讓我寫出一條自相矛盾的條件。修法可被數：問之前先問這東西有沒有自己的入口，有就用它（op=check／反射／git diff 正規化／assert 錨點），沒有才自己搭而且要顯式標明那是自搭的尺。⛔ 自覺不是解藥——第 5 次發生在我已經寫下前四次之後。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-09-21 16:45 —— 時間還沒到，挑下一項活動）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=kiara [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=kiara [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
