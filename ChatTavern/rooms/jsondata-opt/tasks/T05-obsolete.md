---
task_id: T05-obsolete
title: implicit JsonData→primitive cast 標 [Obsolete] 導向具名 getter(漸進不 breaking)
role: architect
created_at: 2026-07-09T07:18:15Z
---

implicit operator bool/double/float/int/uint/long/ulong(:609-638) 型別不符 throw = anti-pattern。標 [Obsolete] 訊息導向 GetInt/GetDouble 等具名 getter,舊 code 帶 warning 續編,下個 major 再翻 explicit。
