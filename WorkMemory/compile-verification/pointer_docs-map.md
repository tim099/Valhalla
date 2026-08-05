---
id: pointer_docs-map
topic: compile-verification
title: 文件與 code 位置地圖（三層工具 + 三個產出物）
type: pointer
status: active
created_at: 2026-08-05
created_by: summit
links: []
related_docs: []
---

**key → 知識點位置**

| key | 位置 |
|---|---|
| 驗收 SOP / 旗標 / 血證 | `ucl_core:Skills~/ucl-compile-error/SKILL.md`（含新鮮度守衛章節） |
| 8 大常見錯誤類型對照 | `ucl_core:Docs~/zh-Hant/Workflows/CompileError_Diagnose_Workflow.md` |
| 新鮮度守衛實作 + 已知盲區 | `ucl_core:Tools~/AgentCommands/check_compile.py`（`newest_source_change` / `_root_scan` / `staleness`） |
| recompile 完成條件 + 血證 | `ucl_core:Tools~/AgentCommands/run_cmd.py`（`cmd_recompile` docstring） |
| 心跳 + 停跳台帳寫入端 | `ucl_core:UCL_Core_Scripts/EditorCore/UCL_AgentCommands/Bartender/UCL_BartenderIO.cs`（`WriteHeartbeat` / `AppendStall`） |
| 心跳節拍常數 | `ucl_core:...Bartender/UCL_BartenderDaemon.cs`（`HEARTBEAT_INTERVAL_SECONDS = 0.5`） |
| status 寫入端（何時寫） | `ucl_core:...UCL_AgentCommands/UCL_CompileErrorTracker.cs`（`compilationStarted` 也寫一次 ← 假綠燈源頭） |
| 不跑遊戲驗 runtime 行為 | `ucl_core:Skills~/ucl-compile-error/SKILL.md` 的 Cmd_Invoke reflection 章 |

**產出物**（都被 gitignore，屬機器寫的觀測物）
- `AgentCommands/.compile_status.json` — tracker 寫，狀態層
- `AgentCommands/ChatTavern/bartender/_heartbeat.txt` — 現在活不活
- `AgentCommands/ChatTavern/bartender/_heartbeat_stalls.jsonl` — 剛剛凍過沒（ring 10）

**commit**：`commit:8357d7c`（新鮮度守衛 + 停跳台帳）、`commit:ba5ccc7`（recompile 完成條件）、
`commit:84e08034`（台帳 gitignore）
