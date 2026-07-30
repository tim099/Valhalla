---
id: pointer_doc-map
topic: agentcmd-schema-codegen
title: 文件地圖：設計/SOP/契約兩側/34 op 宣告/討論出處
type: pointer
status: active
created_at: 2026-07-30
created_by: kotoko
links: []
related_docs: []
---

**這項工作的 key → 權威位置**

| 想知道什麼 | 去哪 |
|---|---|
| 完整設計與決策推導 | `ucl_core:Docs~/zh-Hant/Plan/Plan_AgentCmd_Schema_Reflection_Export.md` |
| 新增/修改 Cmd 後要做什麼 | `ucl_core:Docs~/zh-Hant/API/UCL_AgentCommand/UCL_AgentCommand_Architecture.md` §5.1 |
| Cmd 後台管理頁怎麼用 | `ucl_core:Docs~/zh-Hant/UCL_EditorPage/UCL_AgentCommandsPage.md` §4a |
| spec 型別定義 | `ucl_core:UCL_Core_Scripts/EditorCore/UCL_AgentCommands/UCL_CmdArgsSpec.cs` |
| 生成邏輯 + 跨語言雜湊契約（C# 側） | `ucl_core:UCL_Core_Scripts/EditorCore/UCL_AgentCommands/UCL_CmdSchemaExporter.cs`（`CollectSourceFiles` 註解寫死契約四條） |
| 跨語言雜湊契約（Python 側） | `ucl_core:Tools~/AgentCommands/tavern_cmd.py` → `_iter_cmd_source_files` / `compute_source_hash` |
| Tavern 34 op 的 required/alias | `ucl_core:UCL_Core_Scripts/EditorCore/UCL_AgentCommands/ChatTavern/Cmd_Tavern.cs` → `ArgsSpec`（就在 `switch (op)` 上方，co-location 是刻意的保護） |
| 預檢 A/B 兩層邊界 | `tavern_cmd.py` → `validate_args` docstring |
| 產物本體 | `AgentCommands/commands_schema.json`（入 git） |
| 討論全紀錄 | `tavern:2026-07-29#13922`（提案）`#13923`（gura 推翻 mtime）`#13924`（basecamp 手動為主）`#13930`（求測）`#13932`（gura QA 三發現） |

**改動時的注意**：
- 改 `Cmd_*.cs` 的 required/alias → **同步改該 handler 的 `ArgsSpec`**，然後跑一次同步（面板或 `run ExportCmdSchema`）
- 改跨語言雜湊契約 → **兩端一起改並升 `SchemaVersion`**（C# `UCL_CmdSchemaExporter.SchemaVersion` / Python `SUPPORTED_SCHEMA_VERSION`）
- alias 的**宣告順序 = 優先序**，必須對齊 C# `GetArg(a,"x", GetArg(a,"y", ...))` 的巢狀順序，順序錯不報錯只會安靜選錯值
