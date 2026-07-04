---
task_id: T02-sync-mirror
title: AgentCommands/_lib 改 auto-synced 鏡像 + hash 漂移偵測
role: programmer
depends_on: [T01-ucl-paths]
created_at: 2026-07-04T02:47:10Z
---

【裁決一 P1】AgentCommands/_lib 那份改為同步鏡像（install_skills.py 模式）。鏡像檔頭必須標『AUTO-SYNCED — 別直接編輯，改 UCL_Core 端』；同步機制要帶 hash 比對的漂移偵測（只靠人記得手抄＝下一個 6/16）。驗收：改 canonical → 跑同步 → 鏡像更新且 hash 對得上；手動改鏡像會被偵測到漂移。
