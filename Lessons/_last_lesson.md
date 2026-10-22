# 📝 Lesson noted (git)

- **ts**: `2026-10-21T17:19:17.716Z`
- **actor**: `kaguya`
- **category**: `git`
- **title**: 掛鉤裡的 git 會吃外層的 GIT_DIR
- **tags**: `git`, `hook`, `submodule`, `env`
- **body**: git 掛鉤裡對子模組（或任何別的 repo）下 git，要拿掉 GIT_* 環境變數：git 呼叫掛鉤時帶著 GIT_DIR、GIT_INDEX_FILE（指向外層），git -C <子模組> 照樣吃 ⇒ 量到的是外層的 HEAD。手動跑掛鉤（sh .githooks/pre-commit）沒有那幾個變數 ⇒ 驗不到；掛鉤一定要拿真的 git commit 驗。（Blocksail tools/battle_hook.py，2026-10-22：手動驗六種全過，第一次真的提交就量到外層的 2ee72c5）

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。
