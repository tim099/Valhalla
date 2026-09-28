---
task_id: T03-thread-summary
title: F8 自律寫 thread 摘要進 inbox — 解 context 失憶
role: planner
created_at: 2026-05-08T16:36:23Z
---

## 痛點 (M7)
 thread 過長塞爆 prompt → re-enter 失憶。

## 修法
 agent 收 turn 前自律：寫一段 5 行精華摘要進對方 inbox（或自己 inbox）→ 下 turn re-enter 先讀這段不必還原全文。

## Deliverable
 - ucl-chat-tavern SKILL.md / Tavern_SoloBrainstorm_Workflow.md 加「收 turn 前寫摘要」自律規則
 - 摘要範本 (5 行: 上下文 / 共識 / 開放問題 / 下一步 / 我的角色)
 - 跟 R6.1 task_done summary 同款慣例對齊
