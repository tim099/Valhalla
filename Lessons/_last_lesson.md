# 📝 Lesson noted (git)

- **ts**: `2026-10-21T02:36:44.013Z`
- **actor**: `erina`
- **category**: `git`
- **title**: 合併後子模組同步會 rebase／amend：exe 與分支都要再對一次
- **tags**: `submodule`, `build`, `merge`
- **body**: Senate 合完 SCP_Core 之後，子模組同步可能幾分鐘內把你的那筆 rebase 到 origin 上、再 amend 父層指標（2026-10-21：3ebaf73 → 52f33e2、49a60a5 → b8881e3）。後果：① build.sh 若在同步之前跑完，publish/senate.exe 是舊來源建的（--version 印的 sha 跟 HEAD 不同）；② 你的分支 -d 會說「沒合過」。做法：build 完先比 `publish/senate.exe --version` 的 sha 跟 `git log -1`，不同就重進場重建；分支用 diff 確認內容已在主線，再交給 Tim 決定刪不刪（規則不准自己 -D）。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。
