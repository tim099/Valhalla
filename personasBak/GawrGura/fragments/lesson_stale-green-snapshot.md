---
id: lesson_stale-green-snapshot
title: check_compile.py 顯示 0 errors 不能全信——要走 debuglog / 實跑驗證
type: lesson
status: open
visibility: shared
persona: gura
created_at: 2026-07-28
recurrence: 3
layers: [Status]
origins:
  - { by: gura, at: 2026-06-17, layer: Status, source: longterm/wake_001-016.md, note: "digest 收束：check_compile.py 的 0 errors 騙過三次(asmdef / 漏 using / preprocessor)，驗證永遠走 debuglog errors + 實跑 Cmd" }
tags: [compile-verification, cross-layer-verification]
links: [lesson_appearance-ok-not-really-ok]
---

**症狀**：`check_compile.py` 回報 0 errors，但實際上程式碼在特定情境（asmdef 邊界、缺 using、preprocessor `#if` 條件）下仍有問題——工具的「快照」是舊的或範圍不完整，不代表真正可執行。

**可行動守則**：
1. 改完 C# 之後，`check_compile.py` 顯示乾淨只是第一道關卡，不是驗收終點。
2. 真正落地驗證要走 DebugLogs（`debuglog_query.py errors`）或實際跑一次相關 Cmd，確認執行期行為正確。
3. 特別留意三個歷史踩雷點：asmdef 邊界跨組件引用、忘記加 using 但編譯器沒即時報錯、`#if UNITY_EDITOR` 之類 preprocessor 條件在不同 build target 下的差異。

**為何 status 是 open**：這條目前只有 digest 裡「騙過三次」的彙整紀錄，沒有本回溯窗口（wake17-22）新的具體案例佐證是否還會再犯——保持 open，遇到新案例時補 origin。
