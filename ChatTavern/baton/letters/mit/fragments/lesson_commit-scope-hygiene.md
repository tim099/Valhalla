---
id: lesson_commit-scope-hygiene
title: commit scope 衛生（具名 stage / 分批 / 由內往外 bump）
type: lesson
status: internalized
visibility: shared
persona: summit
created_at: 2026-07-28
recurrence: 3
layers: [Status]
origins:
  - { by: summit, at: 2026-06-14, layer: Status, source: longterm/wake_001-021.md, note: "commit 前必看 staged scope, code/書稿/[chat] 分批, 三層 bump, submodule 先切分支避免游離 commit" }
  - { by: summit, at: 2026-07-24, layer: Status, source: this-session, note: "本 session 多次 commit: UCL_Core/Tools/AgentCommands 都先切追蹤分支確認非 detached, 具名 stage, [chat] 獨立, 排除 ephemeral" }
tags: [git, submodule, commit]
links: []
---

**症狀**：git 操作漏看 staged scope → 混入不相關改動、chat 混 code、submodule 在 detached HEAD 直 commit 落游離節點。

**可行動守則**：commit 前必 git status/--cached 看清；絕不 git add -A（一律具名 stage）；ChatTavern messages 走獨立 [chat] commit；ephemeral（log/_last_op/_wait_/臨時渲染）不入；submodule 由內往外逐層 bump、先切追蹤分支再 commit；每筆帶 Co-Authored-By 身分+模型。

**為何 status internalized**：本 session 落了十幾筆 commit 全程守住（切分支、具名、分類、拆 feature），已成標準流程。
