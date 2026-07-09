---
task_id: T02b-icollection-guard
title: ICollection.* 對 None 補空集合 guard(承 T02, basecamp 測試逼出)
role: programmer
created_at: 2026-07-09T08:54:10Z
---

採(b):IsSynchronized=false/SyncRoot=this/CopyTo no-op。消 GetCollection None→null 的 NRE 面。
