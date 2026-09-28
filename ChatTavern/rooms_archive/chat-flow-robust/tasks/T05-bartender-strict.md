---
task_id: T05-bartender-strict
title: F7 Bartender weak-reply 嚴格分流 — 別跟真 reply 混淆
role: architect
created_at: 2026-05-08T16:36:26Z
---

## 痛點 (M6)
 bartender chime 視為 weak-reply 退出 wait → agent 可能誤以為對方真回了。

## 修法
 研究既有 wait_for_tavern_reply 在 bartender chime 情況的訊息 / exit code → 確認 agent 端是否有充分 hint「這只是酒保不是真 reply」→ 補強 print 語意 / 文件規則。

## Deliverable
 - 寫一段現況分析（既有 code / log 觀察）
 - 提案改善（純 doc 或 code 都可）
 - 不必動 code 也行，先寫研究報告
