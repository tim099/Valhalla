---
id: state_state-2026-07-29-shipped
topic: agentcmd-schema-codegen
title: S0–S5 已 commit（449031d）；待修：0.9s 回歸 / 集合定義不等價 / alias key 順序
type: state
status: superseded
created_at: 2026-07-30
created_by: kotoko
links: [runcmd-modular-split, runcmd-modular-split/state_state-2026-07-29-one-of-six, agentcmd-schema-codegen/state_state-2026-08-01-all-shipped]
related_docs: [commit:449031d, tavern:2026-07-29#13932, tavern:2026-07-29#13930, ucl_core:Docs~/zh-Hant/Plan/Plan_AgentCmd_Schema_Reflection_Export.md]
---

**狀態：S0–S5 全部落地並已 commit（UCL_Core `449031d`，18 檔 +2503/−297）。Tim 親測面板 OK。
上層 `CardGame/Assets/UCL` 的 submodule pointer 尚未 bump（顯示 `M UCL_Core`）。**

## 已完成

| 項 | 落點 |
|---|---|
| 機器可讀 spec 型別 | `UCL_CmdArgsSpec.cs`（`Required` / `Aliases` / `Ops`；**不加 `#if UNITY_EDITOR`**，因為 HandlerBase 沒有 guard，加了 player build 會炸） |
| handler 擴充點 | `UCL_AgentCommandHandlerBase.ArgsSpec`（virtual，預設 null = 不做 client 預檢，是合法狀態不是遺漏） |
| Tavern 宣告 | `Cmd_Tavern.ArgsSpec` **34 op**，逐條照 `RejectLastOp("...缺少 X")` 與 `GetArg` 巢狀鏈抄 |
| 生成器（唯一實作） | `UCL_CmdSchemaExporter`：穩定序、無 wall-clock 欄位、內容未變不落筆 |
| 每日兜底 | `UCL_CmdSchemaAutoSync`（`compilationFinished` + EditorPrefs 節流，每機每天一次） |
| 三個等價入口 | 面板按鈕 / `Cmd_ExportCmdSchema` / ControlPanel 進入點 |
| Python 端 | `tavern_cmd.py` 載入產物；手抄表**整張刪除**；過期→預檢整體降級 |
| 第四處鏡像 | `Registry.ListTypeAliases()` 匯出，`run_cmd.normalize_cmd_type` 優先讀產物 |

**產物**：`<RepoRoot>/AgentCommands/commands_schema.json`（入 git，51 cmd / Tavern 34 op）。

**驗收**：Unity 0 error（12–15s 真編譯）；`tavern_cmd.py --selftest` 全綠（含跨語言 hash 契約、
產物已載入、未過期三項監視器）；產物缺席與過期兩條路徑都實測過（移走／竄改 hash → 還原）。

## ⚠ 待處理問題（gura QA 2026-07-29 深夜抓到，**尚未修**）

### 1. 效能回歸：每筆指令固定多付 0.9 秒 ← 最該先修
`configure()` → `_load_generated_schema()` → `compute_source_hash()` **每次 run_cmd 都跑**：
走遍整個 repo 找 Assets + 讀 52 個檔的完整 bytes。實測 `import` 0.029s vs `configure` **0.911s**。
每一筆 tavern post / read / 任何 cmd 都在付。不報錯只是慢，落在「感覺不出來但天天付」的區間。

### 2. 跨語言檔案集合定義不等價（會靜默永久降級）
C# 錨定 `UnityProjectRoot/Assets`（單一目錄）；Python 是 `repo_root.glob("**/Assets")`。
gura 實測：**Python 已經在撈 `Library/PackageCache/*/Assets` 與 `.git/modules/CardGame/Assets`**，
現在對得上純粹因為 Unity 官方 package 剛好沒人用 `Cmd_` 開頭命名（PackageCache 路徑帶版本 hash，升 package 就換一批）。
**UCL_Core 是跨專案的 —— LY 那種多 Unity 專案 repo 一掛上就永久不符** → 預檢永久降級且沉默。

### 3. alias 優先序寄生在 JSON key 順序（formatter 一碰就靜默翻轉）
優先序是 load-bearing 的，但 JSON 規格明訂 object member 順序**不具語意**。
gura 實測重排 key → `sender` 從 AAA 變 BBB。產物入 git，被 formatter / jq / merge 工具碰到機會不低。
`schema_version` 不會變、hash 會變但只是降級（不報錯）。

### 修法（gura 提，kotoko 認同：一個修法解掉大半）
**產物內存「參與雜湊的檔案清單」**（相對路徑陣列），Python **照清單讀檔驗算**，不自己猜集合：
- 解 2：集合定義只有 C# 一個來源，把「兩份規則要逐字相同」這個維持不住的契約換成「一份規則 + 一份驗算」
- 解 1 大半：不必 walk repo，直接讀清單（要更省再加 mtime 當**快取失效提示**，hash 仍是唯一正確性判準）
- 白送可稽核性：清單本身進 diff，誰多誰少一眼看到
**另外**：alias 改成有序陣列（`[["sender_id","sender"],["id","sender"]]`）或明確 priority 欄位，解 3。

### 4. 還沒收的鏡像
`tavern_cmd.QUEST_OPS_NEEDING_IDEMPOTENCY`（哪些 op 要自動填 idempotency_key）仍是從 C# 抄來的硬編集合，
建議下一輪納入 schema 產物。

### 5. 未驗項（我自己驗不了）
- 面板 UI 細節：**Tim 2026-07-29 已親測 ControlPanelPage + 後台 OK**
- 每日自動同步節流：無人實測（清 EditorPrefs key `UCL_CmdSchema_LastAutoSyncTicks` 再編譯可觸發）
- `create_trpg_room` 實際開團：待 kaguya 驗
