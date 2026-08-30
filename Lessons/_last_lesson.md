# 📝 Lesson noted (bug)

- **ts**: `2026-08-30T08:56:33.668Z`
- **actor**: `basecamp`
- **category**: `bug`
- **body**: 動作訊息不帶「目標」時，「成功」與「成功地做在錯的地方」在畫面上一模一樣。

🩸 2026-08-30 basecamp：skill 管理頁的安裝對象選錯（我以為 Bar、實際 Senate），按下「移除這家全部」後訊息只說「Claude Code：移除 1 個」，我拿那句當成功往下走 —— 刪掉的是三分鐘前才裝好的那一份。

成因有兩層，第二層更該記：
① 我用 `--set` 去設下拉的值，而那是內部狀態、本來就會被擋（元件註解白紙黑字寫著）
② **我把那句錯誤訊息丟進 `/dev/null`** —— 過濾器會把失敗一起濾掉，於是「id 不存在」變成了靜默

判準：**任何會寫入／刪除的回報，句子裡必須有「在哪裡」那個定語**（root / repo / 檔案路徑）。
沒有它就不叫回報，叫感想。修法是第二階（讓它當場喊），不是第三階（下次更小心）。

同族：`.ucl_source` 這種標記回答的是「誰裝的」不是「有沒有被裝過」—— 同日我把 26 個別套系統裝的 skill 標成「殘留．可移除」並各配一顆刪除鈕。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-08-30 17:00，剩 3 分）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=basecamp [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=basecamp [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
