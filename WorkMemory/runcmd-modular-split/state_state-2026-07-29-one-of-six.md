---
id: state_state-2026-07-29-one-of-six
topic: runcmd-modular-split
title: 六塊拆完一塊（tavern_cmd 已 ship）；P0 兩個既有 Bug 未修；readback 暫緩在 stash@{0}
type: state
status: superseded
created_at: 2026-07-30
created_by: kotoko
links: [agentcmd-schema-codegen/state_state-2026-07-29-shipped, runcmd-modular-split/state_state-2026-08-01-handed-to-basecamp]
related_docs: [commit:449031d, ucl_core:Docs~/zh-Hant/Plan/Plan_RunCmd_Split_And_CSharp_Migration.md, tavern:2026-07-29#13918]
---

**狀態：六塊拆完一塊。`run_cmd.py` 1304 → 1052 行；`tavern_cmd.py` 615 行（已 commit `449031d`）。**

## 進度

| 階段 | 狀態 |
|---|---|
| P0 修 Bug#1（`check_cmd_result_file` 讀 QUEUE_DIR 但寫入端走 DataRoot）| ❌ **未做** |
| P0 修 Bug#2（fail marker 表漏 `# ⚠ Tavern Cmd Rejected` 與裸 `❌`）| ❌ **未做** |
| P1 readback 移植 | ⏸ **Tim 拍板暫緩**，basecamp 已 `git stash`（UCL_Core `stash@{0}`），等酒館系統重構一併處理 |
| P2 `tavern_cmd.py` 抽離 | ✅ 完成（29→33 項 selftest；含 wait-reply 三段優先序、alias 歸一、T06.3、persona 不覆寫） |
| P2 `runcmd_paths` / `queue` / `trigger` | ❌ 未做（純機械搬移，風險最低，建議先做） |
| P2 `runcmd_verdict` / `argsource` | ❌ 未做 |
| P3 三個結構問題（`_do_submit` 共用 / git-root walk delegate / `tavern_post()` API）| ❌ 未做 |
| P4 三條硬規則落地 | ⚠ 部分（`tavern_cmd` 已遵守，其餘模組待做時一併） |
| P5 C# A1 receipt + `FailCurrentCmd` | ❌ 未做（A2 codegen 已先做完，見 agentcmd-schema-codegen 主題） |

## 尚未處理的既有缺陷（P0，優先度高於繼續拆）

1. **Bug#1**：`check_cmd_result_file` 用 `QUEUE_DIR / rel_path`，但 C# 寫 `_last_op.md` 走 `DataRoot`。
   同檔其他地方都用 `DATA_ROOT`，只有這處不是。目前沒 `.agentcommands_root.local` 所以沒發作 ——
   **T-PATH-01 的資料根一搬，fail-detection 就永遠回 unknown → 所有 race 失敗靜默變成功**。
2. **Bug#2**：Python 認的 fail marker 是 `# ❌` / `Cmd Failed` / `Cmd failed`；
   `Cmd_Tavern.RejectLastOp` 實際寫 `# ⚠ Tavern Cmd Rejected`，`Cmd_Bartender` 寫裸 `❌` —— **一個都不 match**。
   目前靠 queue 主路徑兜住沒爆，但那條 race 備援等於買了保險沒生效。
3. **Bug#3**：fail-detection 對照表只列 3 個 cmd type（tavern/treasury/notelesson），registry 有 51 個。
   → 根治靠 P5 的 A1 receipt（Runner 寫 per-cmd 結果收據），不是繼續擴表。

## 下一步建議順序

P0 兩個一行修 → `runcmd_paths`/`queue`/`trigger`（純機械，每個附差分測試）→ `verdict`/`argsource` → P3 → P5。
