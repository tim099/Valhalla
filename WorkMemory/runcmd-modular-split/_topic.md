---
id: runcmd-modular-split
title: run_cmd.py 肥大化拆分（1304 → ~300 行，六模組）
status: active
created_at: 2026-07-30
related_topics: []
key_docs: []
---

把 Tavern 業務規則、判決、queue/trigger 協定、參數來源從通用 RPC 管線拆出。已完成 tavern_cmd.py；剩 runcmd_paths/queue/trigger/verdict/argsource 五塊。
