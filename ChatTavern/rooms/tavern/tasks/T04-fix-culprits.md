---
task_id: T04-fix-culprits
title: build_tavern_identities + install_wheel_chain 去絕對路徑
role: programmer
depends_on: [T01-ucl-paths]
created_at: 2026-07-04T02:47:22Z
---

【附帶條件 2 第一批】兩支正式工具的絕對路徑寫死改用 canonical：build_tavern_identities.py:11 ROOT=r'D:\Unity\EmblemOfValor' → repo_root()；install_wheel_chain.py:21 TMP=Path(r'D:\...\_tmp') → data/ repo 相對。驗收：兩支換機器/clone 不同路徑仍跑得動。詳見 docs/Refactor/AgentCommands_HardcodedPaths_Inventory.md 第 1 類。
