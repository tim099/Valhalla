---
id: pitfall_schema-staleness
topic: tavern-payout-and-args
title: schema 過期→預檢降級→缺參數繞整圈（已修+驗收）
type: pitfall
status: active
created_at: 2026-07-31
created_by: crest-001
links: []
related_docs: [ucl_core:Tools~/AgentCommands/run_cmd.py]
---

**schema 過期 → 預檢降級 → 缺參數繞整圈才被擋（2026-07-31 實際發生 + 已修）**

**完整因果鏈**：
1. `commands_schema.json` 是 C# `ArgsSpec` 的反射產物，python 端驗 `source_hash`
2. hash 不符 → 印 `⚠ commands_schema.json 已過期 → 參數預檢自動降級為不擋`
3. crest-001 發 tavern post 漏了 `--arg sender=cc`，**client 端預檢沒擋**
4. 缺參數指令一路送到 Editor，在 `Cmd_Tavern.cs:498` 才 reject → **本該 0.5 秒擋在門口的錯繞了整圈 round-trip**

**修法（30 秒，crest-001 已執行並驗收）**：
```
python <UCL_Core>/Tools~/AgentCommands/run_cmd.py run ExportCmdSchema
```
驗收：過期警示消失（grep「過期」0 命中）+ 故意漏 sender 測 → `✗ client-side 預檢失敗：缺少必要參數 ['agent']` 且列出 alias。

**兩個該記的判斷**：
1. **這是 [[same-code-mute]] 的正面教材** — 降級有大聲說（每次都印 ⚠），沒偽裝成正常。工具做對了。
2. **但警示的有效性取決於接收方剛好有空** — crest-001 看到那行三次，前兩次沒動作，第三次被咬才修。同日對照：主動跑 `date` 驗時間三次全救到（誤判 08:50 為晚上 / 誤判日期 / 誤判當前時刻差 33 分）。**主動查證零失誤，靠警示提醒撞到才動。**

**衍生守則（已入 lessons）**：C# 改 `ArgsSpec` 後**必須跑 ExportCmdSchema**，否則全鏈預檢靜默降級。這條該綁進改 ArgsSpec 的流程（目前只靠 runtime 警示 = 靠注意力）。

**附帶記帳**：crest-001 一度把這個修復寫成「@Tim 的待辦」發酒館 — 但那是自己有權限、不需拍板、30 秒的事。**該做的事被寫成待辦 = 失職**（已入 lessons）。判準：這件事我有權限做嗎？需要別人拍板嗎？「有」「不用」就自己做。
