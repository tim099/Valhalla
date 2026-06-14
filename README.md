# 🤖 AgentCommands/（EOV 隊列資料夾）

這個資料夾是 **AI agent ↔ Unity Editor 跨 process 指令系統的工作目錄**。Agent 寫 `queue.json` 排隊，Editor 內 `UCL_AgentCommandWatcher` 自動偵測 `pending.trigger` 後執行。

> [!NOTE]
> **本系統實作於 UCL_Core 框架層**（跨專案共用），這份 README 僅介紹 EOV 端的資料夾用途與本專案內建的 handler。**框架機制 / queue.json schema / 觸發方式 / 新增 handler SOP** 等通用內容請看：
>
> - 🏗 [UCL_Core: UCL_AgentCommand_Architecture (zh-Hant)](../CardGame/Assets/UCL/UCL_Core/Docs~/zh-Hant/API/UCL_AgentCommand/UCL_AgentCommand_Architecture.md) — 整體架構、生命週期、schema、觸發方式對照
> - 🪟 [UCL_Core: UCL_AgentCommandsPage (zh-Hant)](../CardGame/Assets/UCL/UCL_Core/Docs~/zh-Hant/UCL_EditorPage/UCL_AgentCommandsPage.md) — Editor 內 IMGUI 頁面操作說明
> - 📋 [UCL_Core: Create_Cmd_Workflow (zh-Hant)](../CardGame/Assets/UCL/UCL_Core/Docs~/zh-Hant/Workflows/Create_Cmd_Workflow.md) — 新增自訂指令 SOP
> - 📚 [UCL_Core: API/UCL_AgentCommand/](../CardGame/Assets/UCL/UCL_Core/Docs~/zh-Hant/API/UCL_AgentCommand/) — 各個 `Cmd_*.md`（DebugLog / ExportCommandCatalog / ResolveAssetReferences / FindAssetUsages / ValidateAssetFormat / ExportDocsCatalog / SearchDocs ...）

## 資料夾內容

| 檔案 | 角色 | 誰寫 / 誰讀 |
|---|---|---|
| `queue.json` | 指令隊列（單一真相來源）| Agent 寫 / Runner 讀寫 |
| `pending.trigger` | 「請 Editor 執行 queue」訊號 | Python wrapper 寫 / Watcher 改名為 `.running` |
| `pending.trigger.running` | 「Editor 已接手」訊號 | Watcher 寫 / Runner finally 刪除 |
| `README.md` | 本檔 | — |

## EOV 內建 Handler（RCG 端）

由 [`CardGame/Assets/Scripts/RCG_Scripts/RCG_AgentCommands/`](../CardGame/Assets/Scripts/RCG_Scripts/RCG_AgentCommands/) 各 `Cmd_*.cs` 提供，Registry 自動發現：

| Type | Args | 行為 |
|---|---|---|
| `ExportNotes` | `targets=card\|equipment\|item\|story\|all`（逗號可組合，預設 `all`）| 依 `targets` 匯出 Note → `Docs/Catalogs/<Type>_Notes_Export.md` |
| `Ping` | `msg=<text>` | 印 `Args["msg"]` 到 Console（sanity check）|

> 完整最新清單請走 [`Cmd_ExportCommandCatalog`](../CardGame/Assets/UCL/UCL_Core/Docs~/zh-Hant/API/UCL_AgentCommand/Cmd_ExportCommandCatalog.md) 自動產出 → `CardGame/AgentCommands/commands_catalog.md`（**含 UCL_Core 端 + RCG 端全部 handler**）。

## EOV 端工作流文件

- 📖 [Workflows/AgentCommands_Workflow.md](../Docs/Workflows/AgentCommands_Workflow.md) ⭐ — EOV 端的完整工作流（含協作模式、命名空間踩雷紀錄）
- 📚 [Workflows/DocsCatalog_Workflow.md](../Docs/Workflows/DocsCatalog_Workflow.md) — 文件索引 + 模糊搜尋（`Cmd_ExportDocsCatalog` / `Cmd_SearchDocs` 的 EOV 端使用 SOP）

## 快速使用（Python wrapper）

```bash
# submit + wait（推薦）
python CardGame/Assets/UCL/UCL_Core/Tools~/AgentCommands/run_cmd.py run <CmdType> --arg key=value --timeout 60

# 列當前 queue
python CardGame/Assets/UCL/UCL_Core/Tools~/AgentCommands/run_cmd.py list

# Cmd 失敗預設自動從 queue 移除（避免下次 batch 重跑死局）
# 若要保留條目除錯，加 --keep-failed
```

詳細參數與 fail-fast 行為見 [UCL_AgentCommand_Architecture §7 觸發方式對照](../CardGame/Assets/UCL/UCL_Core/Docs~/zh-Hant/API/UCL_AgentCommand/UCL_AgentCommand_Architecture.md#7-觸發方式對照)。
