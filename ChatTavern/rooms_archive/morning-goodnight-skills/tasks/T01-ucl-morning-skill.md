---
task_id: T01-ucl-morning-skill
title: 新建 ucl-morning skill: 早安 trigger + agent/persona 兩參數解析
role: programmer
created_at: 2026-05-13T14:19:36Z
---

Skills~/ucl-morning/SKILL.md frontmatter trigger 詞「早安大小姐 / 早安<X>大小姐 / morning / wake up」。body 教 agent 解析: skill arg 1 (必) = agent name, arg 2 (選) = persona codename。只給 agent → agent 自決 persona; 給兩個 → 顯式 agent + persona。實作 = 對應 awakening.py morning 跑法。
