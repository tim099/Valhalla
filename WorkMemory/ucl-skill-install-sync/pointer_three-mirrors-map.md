---
id: pointer_three-mirrors-map
topic: ucl-skill-install-sync
title: 三份 skill 實體的角色與 git 待遇（改前先認清在改哪一份）
type: pointer
status: active
created_at: 2026-07-29
created_by: basecamp
links: []
related_docs: [ucl_core:Tools~/install_skills.py, ucl_core:Skills~/, .gitignore:33]
---

**三份實體與各自角色（改東西前先認清自己在改哪一份）**

| 位置 | 角色 | git | 改這裡的後果 |
|---|---|---|---|
| `<UCL_Core>/Skills~/<skill>/` | **source of truth** | 入 git（submodule commit） | 正確；下次安裝會擴散到兩份鏡像 |
| `.claude/skills/ucl-*/` | Claude Code 端安裝產物 | **被 ignore**（`.gitignore:33`） | 改了不入版控，下次跑安裝器就被覆蓋 |
| `.agents/skills/ucl-*/` | Antigravity / Gemini 端安裝產物 | **入 git**（61 檔） | 改了會進 commit，但與 source 漂移 |

**安裝器**：`<UCL_Core>/Tools~/install_skills.py`（`--target` 決定裝到哪一份；submodule bump 後要重跑同步）。

**改 skill 的正確順序**：改 `UCL_Core/Skills~` → 跑安裝器同步兩份鏡像 → UCL_Core commit ＋（若 `.agents` 有 diff）主專案一筆鏡像 sync commit。
反過來只改鏡像 = 下次安裝被蓋掉（`.claude`）或製造漂移（`.agents`）。

**判斷「某路徑為何看不到」的通用指令**：`git check-ignore -v <path>` → 直接印出 `檔案:行號:規則`，比翻 .gitignore 快且不會猜錯。
