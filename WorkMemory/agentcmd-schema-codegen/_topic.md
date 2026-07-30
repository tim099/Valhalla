---
id: agentcmd-schema-codegen
title: Agent Cmd schema 反射匯出（C# ArgsSpec → commands_schema.json → Python 預檢）
status: active
created_at: 2026-07-30
related_topics: []
key_docs: []
---

消滅 Python 端手抄的 Tavern op schema：C# 反射 handler 的 ArgsSpec 生成 commands_schema.json（入 git），Python 載入產物做參數預檢，hash 過期自動降級。含 Cmd 後台管理頁與每日自動同步。
