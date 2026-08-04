---
id: decision_closing-is-authoritative
topic: treasury-bank-hardening
title: 結帳檔是已關帳期間的權威記錄，不是快取（Tim 反轉框架）
type: decision
status: active
created_at: 2026-08-04
created_by: summit
links: []
related_docs: [ucl_core:Docs~/{lang}/API/UCL_AgentCommand/Cmd_Treasury.md]
---

初版設計把每日結帳當「快取」，於是必須處理「快取與 ledger 不一致怎麼辦」——
我為此設計了 `cumulative_entry_count` 對帳 + fail-loud + rebuild 指令。

Tim 反轉了這個框架：

> 舊日期的本就不應該被改動，且以 git 紀錄為準。甚至偵測到不同時，
> **建檔的紀錄比單筆帳更權威**（假如有 bug 或其他情況在舊日期內寫入一筆檔案）。

結果：**我要偵測的問題在定義上消失了。** 讀取演算法本來就只重放「結帳日之後」的日期夾，
所以一筆寫進已關帳日期的 entry 天然落在範圍外，不需要任何邏輯去忽略它。
第 4 步（完整性對帳）連同 fail-loud 全部拿掉，演算法從四步變三步。

這就是真實會計的做法：已關帳的期間就是關帳了，遲到的憑證以調整分錄進當期，而非改寫歷史。

`audit` 欄位仍然寫（產出當下順手算，免費），但**降級為稽核用、不參與判斷** ——
記錄而不執法（apex-one 提案「在產出當下計算，讀取端就不必付成本」，Tim 定調不當 gate）。

**可複用的判斷**：開始設計防禦機制時，先問「這個異常在正確的模型裡還存在嗎」。
今天第二次有人用「換框架」而不是「加邏輯」解掉我的問題
（前一次是 crest-001 的「那是分層問題，A 不該存在」）。
加邏輯是我的預設反應，換框架不是 —— 這是要練的那一項。
