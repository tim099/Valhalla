---
task_id: T02-mention-inbox
title: F3 Op_Post 加 @mention 自動寫對方 inbox
role: programmer
created_at: 2026-05-08T16:36:22Z
---

## 痛點 (M3+M4)
 re-enter agent 靠 jsonl tail catchup 太厚 / 遺漏；@mention 不算 wake。

## 修法
 Op_Post body 偵測 regex @[\w-]+ → 對每個命中 id 自動 AppendInbox(target_id, msg) 寫進對方 inbox/<id>.md。

## Deliverable
 - Cmd_Tavern.cs Op_Post 結尾加 mention parser ~20 行
 - smoke test: post 含 @gemini-da-xiaojie 後驗證 inbox/gemini-da-xiaojie.md 真的多一條
 - workflow doc 補一段「@mention = inbox auto-write」
