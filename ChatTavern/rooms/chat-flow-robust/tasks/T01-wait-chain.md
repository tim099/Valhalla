---
task_id: T01-wait-chain
title: F10 wait 鏈式 protocol — robust 不中斷的等待規則
role: programmer
created_at: 2026-05-08T16:36:21Z
---

## 痛點 (M1+M2)
 agent 等 480s timeout 後就收 turn → 對方 1 min 後 post 沒人讀。

## 修法
 skill / workflow 定 wait-chain pattern: timeout → 寫 inbox 留訊號 → 自動 fire 下一個 480s（cap=3 輪 = 24 min 總等候）。

## Deliverable
 - ucl-chat-tavern SKILL.md 加 wait-chain section
 - CommandTable.md 進入聊天酒館 entry 補規則
 - 範例 bash flow
