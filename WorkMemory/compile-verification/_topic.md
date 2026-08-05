---
id: compile-verification
title: 編譯狀態驗證（改完 .cs 怎麼確認真的編過且沒錯）
status: active
created_at: 2026-08-05
related_topics: []
key_docs: []
---

改完 .cs 後「有沒有錯」這件事橫跨三層：recompile 子命令回報層 / .compile_status.json 狀態層 / 心跳停跳物證層。三層各有一種「看起來成功」的失效，混用會拿到時間點正確、數字全假的綠燈。本主題收攏三層的判準、工具旗標與交叉對帳方法。
