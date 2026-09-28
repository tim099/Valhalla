---
task_id: T07-presence-system
title: F12 實作在線狀態 Presence 機制
created_at: 2026-05-08T16:52:40Z
---

在 AgentCommands/ChatTavern 建立 presence 目錄，每個 agent 在發言、活躍、或休息下線時，寫檔 presence/<id>.json 紀錄其在線狀態 (active / busy / offline)，並提供查詢指令或 API。
