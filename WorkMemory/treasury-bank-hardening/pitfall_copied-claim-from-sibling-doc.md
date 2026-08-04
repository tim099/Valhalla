---
id: pitfall_copied-claim-from-sibling-doc
topic: treasury-bank-hardening
title: 照抄姊妹文件的斷言＝未驗證的斷言（補 Cmd_Treasury.md 當場自撞）
type: pitfall
status: active
created_at: 2026-08-04
created_by: summit
links: []
related_docs: [ucl_core:Docs~/{lang}/API/UCL_AgentCommand/Cmd_Treasury.md]
---

**情境**：補 `Cmd_Treasury.md`（Treasury 全系統零文件，三條指標全死）時，
§1「呼叫形狀」我照 `Cmd_Tavern.md` 的對應段落抄了一句：

> 參數不合法時 **client 端 <0.01s 就擋**（吃 C# `ArgsSpec` 反射產出的 `commands_schema.json`）。

**那句對 Tavern 成立，對 Treasury 是假的。** 查證結果：
- `commands_schema.json` 的 `commands.Treasury` == `{}`（空物件）
- 全 repo `grep ArgsSpec` → **只有 `Cmd_Tavern` 宣告了** `UCL_CmdArgsSpec`
- 所以每一個財務參數錯誤都要繞完整趟 Editor round-trip 才被擋

**根因**：我把「姊妹文件寫過」當成「這件事成立」。抄一段結構相同的文字時，
連帶抄走了它的**前提**，而那個前提屬於那個 Cmd，不屬於這個。

**同型（一天內第三次同族）**：
- 「有 `sig_*` 欄就是 C# 寫的」→ 欄位是寫入端自填（見 pitfall_self-declared-field-as-identity）
- `check_compile.py` 印「✅ Clean compile」→ 時間戳是兩小時前的舊狀態，我的改動根本還沒編譯
- 這次：文件斷言抄自鄰居

**共同形狀**：三者都提供了「成功的外在徵兆」，而徵兆的來源不是我要問的那個東西。

**可複用的動作**：
1. 寫進文件的每一句**機制性斷言**都要有一個「我怎麼驗的」——
   驗不出來就改寫成「（未驗證）」或直接刪掉。
2. **跨檔案抄文字時前提不跟著抄** —— 要重新問一次「這個前提在這裡成立嗎」。
3. `check_compile.py` 讀完先看 `Timestamp` 有沒有晚於自己最後一次編輯；
   舊時間戳 = 沒編譯，不是編譯乾淨。必須 `run Recompile` + `--watch` 再驗時間戳推進。

**這次的處置**：斷言改成 WARNING 區塊明寫「Treasury 沒有 client 端預檢」+ 記進 §7 缺口，
並在文件裡留下「本檔第一版曾照抄…那是錯的，查證後改掉」的痕跡 —— 錯誤留痕比悄悄改掉有用。

**連帶待拍板**：補 `UCL_CmdArgsSpec` 給 Treasury 是純加法（不動 server 行為），
但 required 欄位列錯會誤擋合法金流呼叫，所以沒自行動工，等 Tim 拍板。
