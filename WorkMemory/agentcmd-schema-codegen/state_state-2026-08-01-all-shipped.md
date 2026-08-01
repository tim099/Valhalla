---
id: state_state-2026-08-01-all-shipped
topic: agentcmd-schema-codegen
title: S0–S5 全部 ship 並 push；三個待修已修完；alias 有序陣列等四項仍開放
type: state
status: active
created_at: 2026-08-01
created_by: kotoko
links: [agentcmd-schema-codegen/state_state-2026-07-29-shipped]
related_docs: [commit:449031d, tavern:2026-07-29#13932, tavern:2026-07-29#13930, ucl_core:Docs~/zh-Hant/Plan/Plan_AgentCmd_Schema_Reflection_Export.md]
---

**狀態：S0–S5 全部落地並已 push。上一版 state 列的三個「待修」**（0.9s 效能回歸 / 集合定義不等價 / alias key 順序）**全部修完了** —— 那份快照已過期，本筆取代它。

## 已 commit 並 push（UCL_Core Dev）

| SHA | 內容 |
|---|---|
| `449031d` | S0–S5：ArgsSpec 型別 + Cmd_Tavern 34 op + Exporter + 三入口 + Python 端改讀產物 |
| `76d4759` | **效能修正**：lazy 兩階段載入 + 照產物 `source_files` 清單驗算 + mtime stat 快取 |
| `6a1b460` | 預檢總開關（旗標檔跨語言，停用＝等同產物不存在 + 停止更新產物） |
| `03f7e3a` | 面板卡頓修復：三層快取 |
| `fde5bb8` | （相關）停止錄影清「直播中」殘留檔 |

AgentCommands：`5df94bcd` + `2c6565ea`（產物與兩個 local 旗標入 gitignore）。

## 三個待修的實際修法（供日後查）

1. **0.9s/指令** → `configure()` 只注入依賴，載入與雜湊驗算改 lazy 兩階段；**新鮮度只在即將 enforce required 前才驗**。實測 `run_cmd.py list` 0.899s → 0.067s
2. **集合定義不等價** → 產物內寫 `source_files` 清單，Python 照清單驗算不自己 glob。「兩份規則要逐字相同」換成「一份規則 + 一份驗算」
3. **alias 順序寄生 JSON key order** → （gura 提出）尚未改成有序陣列，**仍是開放項**

## 面板卡頓的真兇（值得記）

不是雜湊，是 `CollectSourceFiles()` 的**整棵 Assets 遞迴掃描，一次 213ms**（46633 個項目，而且掃兩次）。IMGUI 每 frame 呼叫 IsInSync → 每秒數百 ms。修法：清單快取到 static（範圍＝一次 domain reload，正好是安全邊界）+ 併成單次走訪 + stat 簽章 + 1 秒節流。

## 仍開放

- `QUEST_OPS_NEEDING_IDEMPOTENCY` 仍是硬編鏡像（未收）
- schema 每日自動同步節流**無人實測**
- alias 有序陣列（上面第 3 點）
- A2 完整版（提取 required/alias 成宣告）未做；A1.5（op 名單 set 比對報警）未做

## 產物政策（2026-07-30 Tim 拍板改過一次）

`commands_schema.json` **不入 git**（含本機 source_hash，各人不同 → 永久 diff + 假過期）。缺席不是錯誤：Unity 端 AutoSync 偵測到不存在 → **無視每日節流立刻生成**；Python 端 fail-open 跳過預檢並印可執行指令。刻意不由 Python 自動觸發生成（會 spawn run_cmd → Editor 沒開時卡 ack timeout，且 run_cmd import 就走到這條 → 自我遞迴）。
