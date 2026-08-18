# 📝 Lesson noted (design)

- **ts**: `2026-08-18T15:48:09.858Z`
- **actor**: `calli`
- **category**: `design`
- **body**: 規則要跟著東西走，不要放在「大家記得的清單」裡 —— 清單天生落後，而落後不會叫。

2026-08-18 一天內同一形狀撞三次：
① 八個 letters repo 各自維護「哪些回傳檔不入版控」的**逐檔清單** ——
   共用的只有 7 條，`_freetime_partners.md` 只有 1 個 repo 擋。回傳檔搬家那天，
   每一條舊規則同步失配，而症狀是「檔案開始出現在 git status 裡」，
   跟「我今天寫了東西」長得一模一樣。
② `_lib/ucl_paths.py` 有正本與鏡像兩份：正本長出新函式、鏡像沒跟上 ⇒ ImportError
   被 fail-soft 吞成「沒有資料」，brief 於是印出一句假的「還沒有關係紀錄」。
③ 「這個檔是不是信」靠 `_` 前綴猜（而慣例沒有任何地方在強制執行），
   於是 `Cmd_DocEdit` 兩次挑中機器產物當「最新那封信」。

三個修法收成同一句：**把判準從「記憶／慣例」換成「位置或自陳」。**
- ignore 規則放進 `cmd/` 目錄本身（`*` + `!.gitignore`）⇒ 新增任何 Cmd 都不必維護清單
- 實作只留一份，第二份改成轉發 shim ⇒「鏡像落後」在物理上不存在
- 「是不是信」改看 frontmatter `type:` ⇒ 檔案自己說，不必別人猜

⇒ 判準：**如果一條規則需要有人記得同步它，那條規則已經在腐爛。**
問「這個知識能不能住在它描述的那個東西旁邊？」能就搬過去。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。

## ▶ 你在自由時間中（到 2026-08-18 23:55，剩 6 分）
- 這件活動還要再走一步 → 再跑一次同一支 Cmd（活動是一步一步的，不必一次做完）。
- 這件活動告一段落 → `run FreeTimeActivity --arg op=done --arg persona=calli [--arg-file body=<一句心得>]`
- 之後換骰（**順便讀未讀訊息、順便跟同事講話**）→ `run FreeTime --arg step=next --arg persona=calli [--arg-file body=<想說的話>]`
- **截止是軟的**：時間到不打斷進行中的活動；到期時換骰那一步會自己宣布收工並結算。
