---
task_id: T04-owner-routing
title: F9 房間 meta.json 加 owner_agent + 模糊大小姐 routing 規則
role: architect
depends_on: [T02-mention-inbox]
created_at: 2026-05-08T16:36:25Z
---

## 痛點 (M5+M8)
 大小姐稱呼模糊 → 三 agent 搶答 / 都不接。

## 修法
 - room meta.json 加 owner_agent 欄位 (null=any)
 - 模糊「大小姐」沒明確 @ → routing 順序: room.owner_agent → 最近活躍 agent (last_seen_at < 5min) → broadcast 由人類拍板

## Deliverable
 - UCL_ChatRoom 加 owner_agent
 - CommandTable / SKILL 補 routing 規則
 - smoke test: 三身分模擬選對人
