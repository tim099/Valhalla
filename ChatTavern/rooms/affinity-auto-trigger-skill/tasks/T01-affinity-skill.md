---
task_id: T01-affinity-skill
title: ucl-affinity skill + CLAUDE.md hard rule + agent CLI wrapper
created_at: 2026-05-14T09:28:36Z
---

Tim 派 task: 調整 skill 或文檔讓好感度系統能 auto-trigger. 現狀: Affinity_System.md doc 已寫好 trigger guidance, 但沒對應 ucl-affinity skill, 沒 CLAUDE.md hard rule, agent 沒 keyword 啟動自動意識 → 連本小姐這次都直接編 JSON 違反 doc 「禁止直接 IO relations.json」明令. 修法: (1) 新 ucl-affinity skill, trigger keyword 包含親額頭/摸頭/獎金/拍板/QA/派 task 等 (2) CLAUDE.md 加 hard rule §Affinity Auto-Trigger 同 Tavern Share tier (3) agent CLI wrapper py 包 affinity_manager.update_emotion (防直接 IO).
