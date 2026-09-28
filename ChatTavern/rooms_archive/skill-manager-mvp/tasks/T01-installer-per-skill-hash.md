---
task_id: T01-installer-per-skill-hash
title: install_skills.py 逐 skill + 全檔 hash + toggle-off drift 警告
created_at: 2026-05-26T15:22:12Z
---

加 --skill <name> --action install|uninstall; .ucl_source.file_hashes 涵蓋 skill 目錄全檔(非只 SKILL.md); remove 前比對 hash 偵 local drift 警告。
