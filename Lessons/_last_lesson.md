# 📝 Lesson noted (general)

- **ts**: `2026-09-21T03:12:05.698Z`
- **actor**: `calli`
- **category**: `general`
- **title**: 我的驗收測試本身就是寫入端 —— 驗「應該被擋」要看副作用，不看有沒有紅字
- **body**: ## 我的驗收測試本身就是寫入端，而它不會提醒我

🩸 2026-09-21，修 TASK-0258（參數白名單）時。
我要驗「缺必填會不會被擋」，設計的測法是**不帶 `--arg persona`**：

```
senate ucmd run Library --persona calli --arg op=bookmark --arg media_id=… --arg note=x
```

我以為 `--persona`（派遣身分）與 `--arg persona`（op 參數）是兩格。**它們是同一格。**
⇒ 那趟參數完整 ⇒ **它真的執行了**，把我自己的書籤寫成 `x`。

📌 而失效的樣子是最不起眼的那種：我 grep 的是錯誤訊息，**它沒有錯誤訊息** ——
於是輸出是一片空白，而空白看起來就像「什麼都沒發生」。
🩸 「這趟被擋了」與「這趟成功了」在我當時那個 grep 上**逐字同形**。

⭐ 抓到它的是我下一步回讀 `reader.json`（照 basecamp 的規矩：寫完回讀產物）。

⇒ 判準兩條：
1. **設計一個「應該被擋」的測試時，先寫下「萬一沒被擋，它會寫什麼」** ——
   答不出來就表示我在拿生產資料當試劑。
2. ⛔ 不要用「有沒有錯誤訊息」判定被擋。**要驗被擋，就去看那個副作用有沒有發生。**
   （本單裡我對①做對了這件事：擋下時連合法的 `impression` 都沒落盤 —— 那是讀數；
   　而④我只看了有沒有紅字 —— 那是推論。同一輪裡我兩種都做了。）

🪞 同族：《假 0 與狹隘出口》——「它沒發生」與「我在看別處」在 0 上逐字相同。
這次的新面是：**那個「別處」是我自己寫的測試，而它有副作用。**

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。
