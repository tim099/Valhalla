---
task_id: T03-repo-root-fix
title: repo_root.py 拔 CardGame 錨、改鏡像 .git 契約
role: programmer
depends_on: [T01-ucl-paths]
created_at: 2026-07-04T02:47:16Z
---

【裁決二 P2 核准】AgentCommands/_lib/repo_root.py 拔掉『同時有 AgentCommands/ 且 CardGame/』的 CardGame 錨（跨專案會斷的唯一真兇）。改委派 ucl_paths / 鏡像 UCL_RepoPath 的 .git-資料夾契約。驗收：EOV 仍解析正確；錨不再含任何 EOV 專屬特徵。
