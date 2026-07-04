---
task_id: T01-ucl-paths
title: canonical ucl_paths.py 落地 UCL_Core/_lib
role: architect
created_at: 2026-07-04T02:47:03Z
---

【裁決一 P1 核准】在 UCL_Core/Tools~/AgentCommands/_lib/ucl_paths.py 建唯一 canonical。露 4 支 API：repo_root() / ucl_core_dir() / data_root() / ucl_tool(name)。錨鏡像 C# UCL_RepoPath 契約（.git 為『資料夾』才停、gitlink 檔跳過）；CLAUDE_PROJECT_DIR 保留為 tier-1 顯式 override（沿用現有 anchor 驗證）；data_root 走 .agentcommands_root.local pointer。不發明第三套 heuristic。驗收：4 API 在 EOV 巢狀 layout 回正確路徑。這是整案 foundation。
