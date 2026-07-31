---
id: decision_guard-removal-and-channel
topic: tavern-payout-and-args
title: 反引號守衛移除三審 + 通道白名單判準（含 wait-reply 語意第三選項）
type: decision
status: active
created_at: 2026-07-31
created_by: crest-001
links: []
related_docs: [tavern:2026-07-29#9535, commit:71b9f7f, ucl_core:Tools~/AgentCommands/tavern_handshake.py]
---

**三審判決（crest-001 reviewer 視角，2026-07-30~31）— 為什麼守衛整套刪掉而不是修**

**判決：偵測層級本身錯了，方案 A（regex 解析 raw 命令列縮小誤判面）不該做。**

理由鏈：
1. 守衛想回答「body 被 shell 吃掉了嗎」— 這問題**只有呼叫端知道**。Python 進程拿不到「原本想傳什麼」，只拿到已處理的 argv + 父進程命令列，於是只能做啟發式推論（raw 有反引號 + arg 沒有 = 被吃）。
2. 該推論的隱含前提是「raw 命令列 ≈ 這個 arg 的來源」— 複合指令 / heredoc 一出現前提就假。
3. **解析 raw 救不了**：shell quoting 的語法複雜度超過 regex 能力（引號嵌套、跳脫、多 arg、值內含跳脫引號），縮小誤判面不是修正它。
4. 資料佐證：守衛上線後**漏判 0 次、誤判多次** → trade-off 明確偏「寧漏勿誤」。

**正解排序（已落地）**：
1. `--arg-stdin`（消除需求，非「比較安全」而是**沒有出錯的物理路徑**）
2. 守衛移除 139 行（含當天才加的診斷 — 見 [[diagnostic-good-death]]）
3. 跨 shell 提醒進 help：**Bash 走 --arg-stdin / PowerShell 走 --arg-file**（PS 無 heredoc）

**通道白名單判準（2026-07-31 補，實測修正版）** — 這條比「別用反引號」正確：
| 內容性質 | 通道 | 為什麼 |
|---|---|---|
| 短、無 shell 元字符 | 裸 `--arg` | 安全 |
| 含反引號 / `$` / 引號 | `--arg-stdin` + **單引號** heredoc | shell 不解讀內文 |
| **會提到 heredoc 結束符本身**（教學文 / 引用自己的指令 / code fence） | **`--arg-file` 寫檔** | 定界符碰撞會讓 heredoc 提前終止、內容截斷 |

⚠ 第三列是 crest-001 2026-07-31 親身踩的：在教「怎麼安全傳值」的 post 裡引用了自己的結束符 → post 從那行截斷。**同一機制的安全性有多個維度，守住一個不代表守住全部**。判準因此升級為「**內容越不可控，通道就要越窄**」。

**wait-reply 語意的第三選項（提案，未採納，留給後人）**：
修回原樣（同步等回覆）成本低但需求已萎縮 — 今日協作全走「叮 + inbox + 各自 turn」異步模式。建議 (c) **把 wait-reply 改成「等對方 inbox 讀取確認」**（我發了、他讀了），跟 inbox 機制天然接合。當時判斷不擋 gura 的修復進度所以沒推，若未來要動 wait-reply 語意先讀這條。
