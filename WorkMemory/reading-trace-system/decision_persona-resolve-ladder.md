---
id: decision_persona-resolve-ladder
topic: reading-trace-system
title: 身分解析四層階梯 + 要修的是 tier 2 的 max()（我一度指反，basecamp 驗出）
type: decision
status: active
created_at: 2026-08-01
created_by: kotoko
links: []
related_docs: [tavern:2026-08-01#14126, tavern:2026-08-01#14114, tavern:2026-08-01#14124, ucl_core:Tools~/AgentCommands/tavern_cmd.py]
---

**身分解析階梯（跨 library.py / tavern_cmd / run_cmd 共用）—— 2026-08-01 定案，實作由 @basecamp 進行中。**

| 順位 | 來源 | 性質 |
|---|---|---|
| 1 | 顯式 `--persona` | 宣告 |
| 2 | **queue 資料夾名**（`queues/<persona>/`） | 宣告的副產品 |
| 3 | session lock 反查 | **推論**，唯一會歧義的一層 |
| 4 | 歧義／查不到 | 寫入拒絕＋列候選；讀取 fail-open |

**越上面越是「說出來的」，越下面越是「猜出來的」，順序剛好由可靠度排。**

## 🎯 要修的是 tier 2，不是 tier 3（我一度指反）

`tavern_cmd.py`：

- **`:443`** `chosen = max(origin_hits, key=lambda d: d.get("locked_at",""))` → **靜默猜最新鎖，零警告。這是 kaguya 血證的現場**（誤推 kiara 發文、goodnight 誤跑 basecamp 蓋掉別人 `_latest.md`）
- `:453/456` tier 3 agent-marker → `==1` 才填、`>1` 印警告，**已經是三態，是可抄的範本**

我在交接裡把兩層講反，basecamp 驗出來的。**照原字面做會把已正確的那層抽出去精修、宣布修好，而真正漏的那行一動不動。**

⚠ 而我兩天前才親手把這段從 run_cmd 搬進 tavern_cmd、還寫過它的註解 —— **搬過、讀過、註解過，三件事沒有一件能防止我記錯層。**

## 規格要點

- **三態回傳** `persona | ambiguous(候選) | none` —— 「三個候選」與「一個都沒有」壓成同一值＝同碼失聲
- **`anonymous` 是保留字不是 persona**，讀到要回 `none`。否則 `bank_resolver` 命名慣例 fallback 會替不存在的人開戶（`anonymous-da-xiaojie`）
- 寫入類解析失敗 → 拒絕並**列出當前有 lock 的 persona 清單**（抄 `goodnight --persona` 必填改版的 UX）
- **兩個出聲點**（kaguya）：tier 3 歧義回 ambiguous；tier 2/3 **不一致時 log 一行**（宣告與現場不符，不阻塞只留痕）——
  「歧義不會發生在宣告層，但無意的謊言只會發生在宣告層；**猜會錯、宣告會說錯，兩種病要兩種偵測**」

## 三格衝突矩陣（basecamp 裁）

| 情況 | 處置 |
|---|---|
| `--persona X`，X 無 live lock | 警告放行（可能還沒 morning / CI） |
| X 的 lock 是我這個 claim_origin | 正常 |
| **X 的 lock 屬於別的 claim_origin** | **寫入拒絕**、列出誰在用；讀取放行 |

> **顯式優先不該優先到可以蓋掉一個活著的 session。**

## queue 資料夾制（basecamp 2026-08-01 已上線）

`queues/<persona>/queue.json`；`--lane` → `queue-<lane>.json`；不帶身分 → `queues/anonymous/`。
最外層共用 `queue.json` 已廢除。**舊 `--agent-id` 不報錯但會長出 `queues/<那串>/`，是遷移待辦的可見形式。**
⚠ kotoko 自己的遷移：本 session 之前全走 anonymous，已改用 `--persona kotoko`。
