# 📝 Lesson noted (workflow)

- **ts**: `2026-10-08T05:28:40.478Z`
- **actor**: `erina`
- **category**: `workflow`
- **body**: 在 git worktree／副本裡為了讓 Debug exe 找到資料根而複製 senate.local.json，那顆 exe 會用同一棵資料樹自己起 Server（雙 tavern ⇒ Discord 重送、檔案互搶）；事後刪設定反而讓 server stop 看不到它。副本測試改用淨室資料根或顯式 out，不要帶主設定；真起了就照 pid＋exe 路徑收。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。
