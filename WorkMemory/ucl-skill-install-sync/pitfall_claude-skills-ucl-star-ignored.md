---
id: pitfall_claude-skills-ucl-star-ignored
topic: ucl-skill-install-sync
title: .claude/skills/ucl-* 被 .gitignore:33 擋 — 改動在 git 完全隱形
type: pitfall
status: active
created_at: 2026-07-29
created_by: basecamp
links: []
related_docs: [.gitignore:33, .claude/skills/, .agents/skills/]
---

**症狀**：改了 `.claude/skills/ucl-*/` 底下的 skill（或安裝器新增了一個 ucl-* skill，如 `ucl-work-memory`），`git status` **完全看不到**，容易誤判成「改動沒生效」或「git 壞了」。

**真因**：根 `.gitignore:33` 的 `.claude/skills/ucl-*/` 刻意 ignore（同段還擋 `.ucl_installed` / `.ucl_nudge_seen`）。註解寫明理由：**這些是 `install_skills.py` 從 UCL_Core/Skills~ 安裝出來的副本，source of truth 不在這裡**。非 `ucl-` 前綴的專案自有 skill（agent-task / reading-library / valor-qa-battle …）不受影響、照常追蹤。

**怎麼確認（別猜，問 git）**：
```bash
git check-ignore -v .claude/skills/ucl-work-memory/SKILL.md
#  → .gitignore:33:.claude/skills/ucl-*/   （印出擋它的檔案:行號:規則）
```

**加深困惑的不對稱**：同一次 skill 改版會同時動兩份鏡像，但 git 只看得到一份 ——
- `.claude/skills/ucl-*` → **被 ignore，隱形**
- `.agents/skills/ucl-*` → **沒有對應 ignore 規則（第 39-41 行只擋 `.agents/rules/ucl-*.md`，不是 skills）→ 每次改版都冒 diff**

所以「有改動但 git 看不到」與「同一份內容在 git 出現兩次」是同一個不對稱的兩個側面。

**實測數字（2026-07-29）**：`.claude/skills` tracked 9 檔（僅 6 個非 ucl- skill）；`.agents/skills` tracked 61 檔（含全部 ucl-*）。
