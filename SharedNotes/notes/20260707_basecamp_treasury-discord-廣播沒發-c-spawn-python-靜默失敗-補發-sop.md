---
id: 20260707_basecamp_treasury-discord-廣播沒發-c-spawn-python-靜默失敗-補發-sop
title: Treasury Discord 廣播沒發 — C# spawn python 靜默失敗 + 補發 SOP
author_persona: basecamp
author_agent: claude-code
created: 2026-07-07
last_updated: 2026-07-07
note_type: runbook
topics:
  - treasury
  - discord-routing
  - token-economy
subjects:
  - UCL_TreasuryLedger
  - notify_treasury
  - Cmd_Treasury
tags: []
related_notes: []
supersedes: []
visibility: public
status: superseded_by:20260707_basecamp_workpost-進帳discord-斷-根因-category-routing-asset-空-重建修復
---


**症狀**：Cmd_Treasury credit/debit（尤其 C# 觸發的：開戶 genesis、每日保管費）發生後，Discord 記帳頻道收不到 embed，但 ledger 檔正常寫入、餘額正確。

**根因**：`UCL_TreasuryLedger.FireDiscordBroadcastAsync` 用 `ProcessStartInfo{ FileName="python", UseShellExecute=false }` fire-and-forget spawn `notify_treasury.py`。Unity Editor 從 Hub/檔案總管啟動時，process 環境常**沒有把使用者 python 放進 PATH** → `Process.Start` 丟 Win32Exception → 被 catch 成一句 `Debug.LogWarning`（靜默、無重試）。scriptPath / entry fullPath 都正確且絕對，不是路徑問題。對比：agent 從 shell 跑的廣播（qa_bug_reward / agent_task 走 Python `fire_broadcast`）正常，因為 shell 有 python。判別法：**C# 觸發的廣播掛、CLI 觸發的正常 → 就是這條。**

**即時修復（補發漏掉的廣播，可安全重跑）**：
```
python AgentCommands/PromptQueue/notify_treasury.py --entry-file <ledger entry .json 絕對或相對路徑>
```
成功印 `[notify_treasury] ok (N target(s))`。找漏發的 entry：`AgentCommands/Treasury/ledger/<date>/*.json`。

**驗證 pipeline 本身沒壞**：對任一 entry 手動跑上面指令，若 ok 就是 Python 端正常，問題在 C# spawn 環境。

**永久修復方向（需 Tim 端動作，擇一）**：
1. 把使用者 python 放進 Unity Editor 啟動環境的 PATH（最省，環境層）。
2. C# 改用解析過的 python 完整路徑（或啟動時 `where python` 快取）+ 設 `WorkingDirectory=RepoRoot` + spawn 失敗寫「broadcast_pending」marker（需 recompile）。
3. Python 端加一支 broadcast sweeper：掃 ledger 中無 `broadcast_done` marker 的 entry 自動補發——把 Discord 送達與 Editor 的 python 可用性解耦（最 robust，新增 infra）。

**cross-link**：agent-lessons-log（fire-and-forget 靜默失敗 = 同家族坑）；subject `notify_treasury` / `UCL_TreasuryLedger`。
