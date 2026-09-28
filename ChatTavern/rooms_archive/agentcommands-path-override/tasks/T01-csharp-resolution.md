---
task_id: T01-csharp-resolution
title: C# 解析層: AgentCommandsDir override + pointer 檔 + Treasury 修正
role: architect
created_at: 2026-05-28T02:31:35Z
---

Phase 1. 首要(Tim): 預設(無 override/無 pointer 檔)路徑解析與現在完全一致, 不破壞現有流程. (1) AgentCommandsPathMode enum 3模式 (2) UCL_RepoPath.AgentCommandsDir 讀 PlayerPrefs override + ResetCache() (3) git-root pointer 檔 .agentcommands_root.local 讀寫+write-through (4) Treasury 改走 AgentCommandsDir (5) ChatTavern/Bartender 改走 AgentCommandsDir. 驗收: compile 0 error + 預設行為不變.
