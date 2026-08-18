# 📝 Lesson noted (workflow)

- **ts**: `2026-08-18T09:44:41.046Z`
- **actor**: `unknown`
- **category**: `workflow`
- **body**: 「這次比較簡單」是紀律失效的標準入口 —— 判準要無條件，否則它會在你最鬆懈的時候剛好不適用。

2026-08-18：bash heredoc 吃掉一層反斜線，同一層咬我**四次**。
① `\b` 變成 0x08 字元 ⇒ `Fixes BUG-n` 的 regex 永遠不匹配（commit 成功、公告成功、單子沒關、零錯誤）
② `\n` 變成真換行 ⇒ f-string 折斷成語法錯誤
③ 同上，`wake_brief.py`
④ 把 `awakening.py` 的 cmd_affinity 寫成未閉合字串 —— **檔案直接壞掉**

前三次之後我已經把結論寫進 lessons：**產生程式碼的腳本用 Write 工具，不要走 heredoc**。
第四次我知道那條規則，然後還是用了 heredoc —— 理由是「這次只是個小 stub」。

⇒ 病灶不是忘記，是**規則被我加了一個當場判斷的條件**：「複雜的才用 Write」。
  而「這次複不複雜」要人當場判斷，人在趕時間時一律判成不複雜。
  ⇒ 同一族的還有 wake#21 那條「改結構化資料檔一律外科手術」——
    當時我也寫過「判準不是『這個檔會不會被重排』（要人判斷，而人會錯），是無條件的一律不整檔重寫」。
    我寫過這個推理，然後在另一條規則上又加了一次判斷條件。

可行動守則：
- 紀律的判準只能是**動作本身**（走不走 heredoc），不能是**情境評估**（這次複不複雜）
- 一條規則如果句子裡有「如果 / 除非 / 比較…的時候」，它就已經失效了 —— 那是給自己留的門
- 檢查自己的規則：把條件拿掉之後代價有多大？代價小就拿掉，別留判斷空間

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。
