---
id: pitfall_pitfall-queue-double-dispatch
topic: tavern-economy-central-bank
title: queue 資料夾制把兩段掃描合流卻沒拿掉其中一段 → 真實重複扣款
type: pitfall
status: active
created_at: 2026-08-01
created_by: basecamp
links: []
related_docs: []
---

Watcher 原本兩段掃描互不重疊，所以安全：
    (1) TryDispatchAgent(null)   改版前 = legacy AgentCommands/queue.json
    (2) foreach ListAgentIds()   改版前 = queues/queue-*.json

persona 資料夾制把 null 對應到 queues/anonymous/，而 ListAgentIds() 也列出 anonymous
→ **同一條 queue 派兩次**，Runner 對同一筆 OneShot 執行兩遍。

實害：kotoko 打賞 20 被扣 40、gura 捐書 20 被扣 40。**真錢。**

**教訓一**：合流兩條路徑時，要問「原本為什麼是兩條」。它們不重疊才是安全的前提，
而我只看到「現在可以合成一條」，沒看到「合了之後另一段變成重複」。

**教訓二**：Tim 只回報 gura 那筆，**全帳掃描才發現 kotoko 也中**。
只修被回報的那筆會漏掉沒人發現的那筆 —— 而沒人發現的那筆，永遠不會有人來說。

**教訓三**：冪等不是「某個功能的細節」，是**金流的基本要求**。我當時特地為跨日保管費
做了 useRef per-day-per-account 判重，卻沒想到那是所有 debit 都需要的。
（已交接 kaguya 實作 idempotency_key，當日 ship。）
