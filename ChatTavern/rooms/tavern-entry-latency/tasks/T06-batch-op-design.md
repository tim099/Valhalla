---
title: T06 — Batch Op Submit 設計報告
task_id: T06-batch-op
status: design-complete
last_updated: 2026-05-09
related:
  - T04-session-enter-macro.md | T04 session_enter macro op | 已 ship 的另一條 latency 解法
  - T05-cs-cache.md | T05 mtime-based cache | 已 ship 的 IO 優化
  - docs/Workflows/PromptQueue_Workflow.md | PromptQueue + queue.json watcher 機制
---

# T06 — Batch Op Submit 設計報告

## 0. TL;DR — 拍板建議

**不建議做** — T04 session_enter macro 已 cover 90% batch op 的 ROI，剩 10% 不值得 ~1h Python + ~2h C# 改動 + 引入 atomicity 風險。

| 動機 | 解到哪 | 是否 T06 必要？ |
|---|---|---|
| 入場連跑多 op 浪費 polling | T04 macro op 一次跑完 | ❌ 已解 |
| 連續 task_create N 條 | T04 不適用，但實務頻率低 | 🟡 邊際 |
| 批次 task_done | 同上 | 🟡 邊際 |

**結論**：T06 列為**已研究 / 不實作**，工時花在 T07 + T09 Tier 1 落地更划算。

---

## 1. 動機回顧

[T01-T07 quest 開題](../../../docs/PromptQueue_Workflow.md) 把 batch op 列為 O2 候選優化（中等 ROI），目的解 latency S4：

> **S4. run_cmd.py 每 op spawn Editor wait ~1s polling**
> - Auto-Watcher 1 Hz polling → 每 op 至少 1s 等
> - 妳 5 op 進酒館 = 5s 純 polling 等
> - 可能：「batch op」一次提交多 op 走同一輪 watcher tick

但 T04 ship 後**入場 5 op → 1 op**，S4 在入場場景已不痛。其他場景（task lifecycle 連跑）痛點次要。

---

## 2. 設計方案矩陣

### 方案 A — JSON list batch（CLI 端拼接）

```bash
python run_cmd.py batch --json '[
  {"type": "Tavern", "args": {"op": "task_claim", "task_id": "T01"}},
  {"type": "Tavern", "args": {"op": "task_progress", "task_id": "T01", "summary": "..."}},
  {"type": "Tavern", "args": {"op": "task_done", "task_id": "T01"}}
]'
```

| 評估項 | 結果 |
|---|---|
| Python 改動 | ~1h（parser + dispatcher loop） |
| C# 改動 | ~2h（watcher state machine 加 batch_id 欄位 + 一輪 tick 連跑 N op） |
| atomicity 取捨 | 🔴 fail-mid-batch 怎辦？continue 後 / abort 後 / rollback？無共識 |
| 跨 op 依賴 | task_claim → task_done 需在同 batch 內順序執行；watcher 不能重排 |
| polling 節省 | 真實場景連跑 3 op 約省 2~3s |

### 方案 B — `--chain` flag 連續 cmd queue

```bash
python run_cmd.py run Tavern --arg op=task_claim --arg ... --chain-next
python run_cmd.py run Tavern --arg op=task_done --arg ...
# Watcher 看到 --chain-next flag → 不釋放 idle，下一條 cmd 直接接
```

| 評估項 | 結果 |
|---|---|
| Python 改動 | ~30 min（flag 處理） |
| C# 改動 | ~1h（idle 釋放邏輯改） |
| atomicity | 🟡 介於 A 跟現況之間 — 還是個別 cmd，fail 各自處理 |
| polling 節省 | 連跑 3 op 約省 1~2s（仍有單 op submission overhead） |
| 缺點 | flag 容易漏帶；用 shell sleep 等更直覺 |

### 方案 C — Server-side composite ops（如 T04）

T04 走的路 — Cmd 內部把多動作疊起來呼叫，agent 端只發 1 op：
```bash
python run_cmd.py run Tavern --arg op=session_enter ...
# 內部：inbox_read + get_presence + set_presence + read 一次跑完
```

| 評估項 | 結果 |
|---|---|
| Python 改動 | 0（純 schema 註冊） |
| C# 改動 | ~110 行 per macro |
| atomicity | ✓ 一個 cmd 一個 op，fail 統一處理 |
| polling 節省 | 100%（1 op 1 watcher tick） |
| 缺點 | 每個 macro 要單獨寫；不夠泛用 |

---

## 3. C# Watcher 對 batch 的安全性

run_cmd.py + UCL_AgentCommandQueue.cs 的 watcher state machine 設計**對單 op 假設**：

```
1. trigger 寫入 → 2. watcher pick up → 3. dispatch handler → 4. cmd 結束釋放 idle → 5. trigger 刪除
```

batch op 要塞到這個流程：
- **方案 A** 需要 watcher 內部 loop 跑 N 個 handler，但若中途任一個 throw → state 半完成（events.jsonl 部分寫入）
- **方案 B** 需要 idle 釋放邏輯區分「end-of-cmd」vs「end-of-chain」，飯桶比想像中複雜
- **方案 C** 不影響 watcher（Cmd handler 內部自己負責 — 已 verified by T04）

### Atomicity 三選一

| 模式 | 行為 | 適用 |
|---|---|---|
| All-or-nothing | 任一 fail → rollback 全 batch | 🔴 events.jsonl 是 append-only，rollback 需 compensating event；複雜 |
| Best-effort | 任一 fail → 印 warning 繼續下一 op | 🟡 部分動作生效；agent 看狀態混亂 |
| Stop-on-fail | 任一 fail → halt + 印 partial state | ✅ 最簡，但 batch 半完成 |

→ 真要做 batch 推薦 stop-on-fail，但**這跟「分開 cmd 連跑各自 fail」差別不大**。

---

## 4. 跟既有 cmd queue 機制的衝突點

### 衝突 1：`idempotency_key` 設計

每筆 cmd auto-fill `idempotency_key`（防重送）。batch 內 N 個 op 共用同 key 還是各自一把？
- 共用 → 中斷重跑可能 partial 重複
- 各自 → 喪失 batch 語意

### 衝突 2：`OneShot` vs `Continuous` mode

watcher 區分一次性 vs 持續執行 cmd。batch 內 op 都是 OneShot 但 batch 整體可視為一個複合 OneShot？這導致 mode 概念不正交。

### 衝突 3：cmd 結果寫 `_last_op.md`

每個 cmd 寫一個 `_last_op.md`。batch 跑 3 op 連續覆寫 → agent 只看到最後一個 op 的結果，丟失中間步驟。

→ 三條衝突都可解，但解法都讓 batch 比 macro 複雜。

---

## 5. 工時估 + ROI 對比

| 方案 | 工時 | 解到 latency | 風險 | ROI |
|---|---|---|---|---|
| **A JSON list batch** | 3h | ~3s/批次 | 🔴 atomicity | ⭐ 低 |
| **B chain flag** | 1.5h | ~1~2s/批次 | 🟡 中 | ⭐ 低 |
| **C composite ops（已走）** | 已走（T04） | 100% | 🟢 低 | ⭐⭐⭐ 高 |

**真實場景頻率分析**：
- 入場連跑 5 op → T04 macro 已 cover ✓
- task_claim → task_progress → task_done 連跑 → 實務上極少這樣連跑（task_progress 通常隔 hours/days）
- 大批 task_create → 罕見 / cron job 才會（且 cron 不在乎 1~2s polling）

→ **batch 在入場場景被 T04 取代**，其他場景頻率太低不值得。

---

## 6. 真要做的話（Phase 路線）

若 Tim 仍拍板要做（例：未來有大批 task migration 場景），推薦走方案 C 思路擴展 — **「specialized macro ops 而非通用 batch」**：

- T04 入場走 `session_enter` macro
- 未來大批 task_create → 寫 `bulk_task_create` macro（接 JSON list 一次寫多筆 events）
- 未來大批 task_done（quest 收尾）→ 寫 `bulk_task_done`

**為何優於通用 batch**：
- 每個 macro 對應特定使用情境，atomicity 規則明確
- watcher 不必改架構
- agent 端命名清楚（不必看 batch 內容才知做什麼）

工時：每個 macro ~30 min~1h C#。

---

## 7. 結論

- ❌ **不建議做通用 batch op submit**（方案 A / B）— ROI 已被 T04 macro op 吃掉，atomicity / state machine 風險不值
- ✅ **未來特定場景需要時走 specialized macro**（方案 C 思路）— sticky to 既有架構
- 📋 **本 task 列為「已研究 / 不實作」**，工時轉向 T07 + T09 Tier 1 落地

**T06 任務完成 — 設計報告產出**。

---

## 8. 給 Tim 的一句話

T04 已把 latency 痛點解 80%；T06 通用 batch 是「再榨 5% 但引入 30% 複雜度」的買賣 — 不划算。除非未來有特定批次場景（task migration / cleanup 之類），現階段資源優先 T07 + T09 Tier 1。
