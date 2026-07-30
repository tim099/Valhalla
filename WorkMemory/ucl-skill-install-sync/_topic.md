---
id: ucl-skill-install-sync
title: UCL skill 安裝與鏡像同步（.claude / .agents / UCL_Core 三份）
status: active
created_at: 2026-07-29
related_topics: []
key_docs: []
---

UCL skill 有三份實體：UCL_Core/Skills~ 是 source of truth，.claude/skills 與 .agents/skills 是安裝產物。三份的 git 追蹤待遇不同（.claude 的 ucl-* 被 ignore、.agents 的 ucl-* 入 git），造成「改了卻看不到」與「同內容兩次 commit」兩種困惑。本主題記追蹤策略、判斷指令與待拍板項。
