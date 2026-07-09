---
task_id: T03-microopt
title: SerializeString 去 ToCharArray + GetDouble/GetFloat 補 UInt/ULong
role: programmer
created_at: 2026-07-09T07:18:12Z
---

SerializeString(:731) 去掉 str.ToCharArray() 直接迭代 string。GetDouble(:452) 補 UInt/ULong;GetFloat(key)(:441) 補 ULong。
