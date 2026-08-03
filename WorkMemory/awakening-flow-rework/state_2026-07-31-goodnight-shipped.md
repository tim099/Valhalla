---
id: state_2026-07-31-goodnight-shipped
topic: awakening-flow-rework
title: 晚安瘦身已 ship，四項待明早驗
type: state
status: superseded
created_at: 2026-07-31
created_by: kiara
links: [awakening-flow-rework/state_2026-08-03-pushed-and-partly-superseded]
related_docs: [ucl_core:Docs~/zh-Hant/Plan/Plan_Goodnight_Flow_Simplification.md, ucl_core:Docs~/zh-Hant/Workflows/Awakening_Ritual_Workflow.md, commit:be257e0, tavern:2026-07-31#9756]
---

**做到哪**：施工單 Plan_Goodnight_Flow_Simplification 全節完工並 commit（UCL_Core `935d495` → `38c37f5` → `f9d829d` → `629c9f7` → `be257e0`；主專案對應 5 筆 bump）。編譯 0 errors，全部**未 push**。

**已驗**：`--persona` 必填守衛（exit 2 + 列 lock，零副作用；calli/gura/Sirius 三方複驗）、自動遷移（apex-one 15 封）、wake_count 推導、見林書籤換算（gap −10 → +2）、§5 短信合併六個分支 fixture。

**pending（今晚/明早才驗得到）**：
1. **晚安全程** —— 信落 `wakes/0000NN`、`_latest` 更新、vector 擾動、**peek 印完 cursor 不可被推進**。calli 認領。
2. **自動遷移的其餘 17 人** —— basecamp 最兇（registry 曾被重建：59 / digest 54 / 磁碟 57 → 遷移後 51）。
3. **往返連號** —— 今晚下線者明早 `wake_count == wakes/ 封數 + 1`。
4. **§5 負向樣本** —— calli 39 / gura 18 / summit 25 / basecamp 10 / crest-001 40 行，明早都**不該**出現「已往前合併」。

**未決**：§1 見根 0 筆時渲染空表格（純顯示，Tim 未拍板）；`Docs/Glossary` pointer 仍落後 calli 的 `5e21ced`。
