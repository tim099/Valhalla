---
id: pitfall_three-layer-false-green
topic: compile-verification
title: 三層各有一隻假綠燈：時間戳對而數字假 / 快照早於改動 / 停跳不等於編譯
type: pitfall
status: active
created_at: 2026-08-05
created_by: summit
links: [unitask-editor-async/knowhow_unitask-patterns, library-media-migration/pitfall_slug-vs-title-and-position-vs-coverage]
related_docs: [ucl_core:Skills~/ucl-compile-error/SKILL.md, ucl_core:UCL_Core_Scripts/EditorCore/UCL_AgentCommands/UCL_CompileErrorTracker.cs]
---

**三層各有一隻「看起來成功」的失效，而且長得都不像壞掉。**

| 層 | 假成功的樣子 | 為什麼難看破 |
|---|---|---|
| recompile 回報層 | `✓ Compile finished (0.0s) — errors=0, warnings=0` | **時間戳是對的**，只有數字是 compilationStarted 那筆的空值。真實是 7.188s / 37 warnings |
| status 狀態層 | 印出完整的 errors 清單（甚至紅燈） | 那份快照**早於你的改動**。2026-08-05 實摔：status 寫在 08:57:00、我最後一筆編輯 08:57:06，工具照樣把它當結論，我去查了一隻不存在的 CS0103 |
| 心跳物證層 | 有停跳紀錄 → 以為編譯過 | 停跳只證明**凍結**：domain reload / 資產匯入 / 主執行緒長工 / **Editor 關閉整夜**都會停跳 |

**還有兩個不對稱的坑：**

1. **`--editor-alive` 印「✅ Editor 正在 tick，沒有卡在編譯」在編譯被遞延的 9 分鐘裡字面為真。**
   Editor 可以同時「在 tick」且「編譯排隊中」—— 探針量心跳，碰不到「請求已登記但未執行」。
   Unity 常把外部改檔的重編**遞延到視窗重獲焦點**，這不是 bug 是行為。
   （我當時誤判成「Unity 拒絕編譯」，實際是遞延。）
2. **停跳只有在「恢復的那一拍」才寫得出來** —— 進行中的凍結沒有紀錄，Editor 死掉不再回來則永遠不寫。
   **沒有條目 ≠ 沒有停跳。**

**血親**：2026-05-22 apex-two 的 CS1061 被 recompile 漏報成 errors=0。當年結論寫進 skill 的是
「改用 check_compile.py 二次確認」—— **修的是繞路，沒回頭修源頭**，而 check_compile 自己也沒有
新鮮度概念，於是三個月後同一族在另一邊咬人。**繞路修法會讓同一隻 bug 換棲地。**
