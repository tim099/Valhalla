---
id: decision_split-layout-and-hard-rules
topic: runcmd-modular-split
title: 六模組切法 + 為何不用 _lib（shadowing 實證）+ 三條硬規則
type: decision
status: active
created_at: 2026-07-30
created_by: kotoko
links: [agentcmd-schema-codegen]
related_docs: [ucl_core:Docs~/zh-Hant/Plan/Plan_RunCmd_Split_And_CSharp_Migration.md, ucl_core:Tools~/AgentCommands/tavern_cmd.py, ucl_core:Tools~/AgentCommands/tavern_handshake.py]
---

**結論**：run_cmd.py 只留 CLI 骨架 + 子命令編排，其餘按職責下沉到**扁平 sibling 模組**。目標 1304 → ~300 行。

## 模組切法（六塊）

| 模組 | 職責 | 狀態 |
|---|---|---|
| `tavern_cmd.py` | Tavern 業務規則：op schema / alias / persona 反查 / 保留 tag meta / wait-reply 政策 / banner | ✅ 已 ship |
| `runcmd_paths.py` | queue/trigger/running 路徑（agent-id + lane）；delegate `_lib/ucl_paths.py` | 待做 |
| `runcmd_queue.py` | load/save(atomic+retry) / find / remove / make_id / append_cmd / TYPE_ALIASES | 待做 |
| `runcmd_trigger.py` | trigger_state / ensure_idle / write_trigger | 待做 |
| `runcmd_verdict.py` | 判決：result file 檢查 / 錯誤報告輸出 / print_fail_verdict（+ readback 掛點） | 待做 |
| `runcmd_argsource.py` | parse_kv_pairs / expand_arg_file / expand_arg_stdin / env_marker | 待做 |

## ⚠ 為何是扁平 sibling，**不放 `_lib/runcmd/`**（Round 1 原提案已推翻）

1. **名稱已被佔用**：`<repo>/AgentCommands/_lib/tavern_client.py` 已存在，是完全不同的東西（daemon 用的 TavernClient SDK）。
2. **`_lib` 這名字本身有 shadowing 陷阱**：UCL_Core 與主專案各有一個 `_lib`，前者是 namespace package（無 `__init__.py`）、
   後者是 regular package。**實測**：先 `import _lib` → 解析到 UCL_Core 那份；**先 `import awakening`**
   （它會把 `<repo>/AgentCommands` 插到 `sys.path[0]`）再 import → 解析到**主專案鏡像**。
   而 Tavern 的 persona 反查正好會在呼叫時 import awakening —— 同一 process 內 `_lib` 指向哪邊
   取決於「這次有沒有先發過 post」。把拆分成果蓋在這上面等於蓋在流沙上。
3. `tavern_handshake.py` 已用「扁平 sibling + `configure()` 注入」的形狀跑過一輪且穩定，沿用同一形狀，不發明第二套載入慣例。

## 🔒 三條硬規則（拆分時一併落地）

1. **路徑常數只准住 `paths` 模組**，其他一律 import，不准各自定義或另取名。
   （實證：`TAVERN_ROOT` vs 真名 `TAVERN_DIR` → py_compile 全過、一跑 NameError；同族的還有
   `check_cmd_result_file` 讀 QUEUE_DIR 而寫入端走 DataRoot。修好那一處不如封死那個類別。）
2. **同一種走訪／解析邏輯只准有一份實作**，其他一律呼叫。
   （per-message 走訪目前已有 3 份：`tavern_query` / `tavern_catchup` / `tavern_handshake`。）
3. **路徑初值不給 fallback 預設** —— 沒注入就炸，不准靜默退到某個「看起來合理」的目錄。
   **不給預設值是設計，不是懶**：炸得漂亮 ≫ 靜默讀錯目錄然後回報一切正常。
   （這條寫進 plan 不到一小時就自己付了一次成本也自己還了一次：`tavern_cmd --selftest` 第一次跑
   就紅在「configure 注入」測項，因為雙模組陷阱。有 fallback 的話會靜默讀錯 session 目錄然後全綠。）

## 順手要修的結構問題（尚未做）

- `cmd_run` 內聯重抄了 `cmd_submit` 整段（只為留住 cmd_id）→ 抽共用 `_do_submit()`
- run_cmd 自己抄了一份 git-root walk + pointer 解析，而 `_lib/ucl_paths.py` 早就是 canonical → 改 delegate
- 六支工具各自 subprocess 手搓 argv 發 tavern post、timeout 各自為政 → 收斂成一支 `tavern_post()` API
  （實證成本：morning ritual 的 announce 因 60s timeout 誤報 FAIL，實際早已落地）
