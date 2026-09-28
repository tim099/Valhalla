---
task_id: T07-antigravity-startup-hook
title: Antigravity startup hook 調研（解 S1 從根本）
role: researcher
created_at: 2026-05-08T23:20:22Z
---

# 🛰️ T07: Antigravity 啟動與進場鉤子 (Startup Hook) 調研報告

哼，這項任務本小姐（`antigravity-da-xiaojie`）既然親自認領了，自然要給出全專案最專業、最無可挑剔的平台級深度調研！

別以為 Antigravity 端跟其他持續性進程的 Agent（如 Claude Code 走背景 Bash daemon 模式）一樣。要徹底解決「S1：進場延遲與狀態落後」的硬傷，就必須深刻理解我們的平台物理屬性，並給出完美的工程接線！

---

## 🔍 1. Antigravity 平台的物理本質

* **單 Session 單輪模型 (Transient Session)**：
  Antigravity 平台本質上是**每次 User Prompt = 一次全新的模型調用 Session**。在對話結束、回覆產出的瞬間，當前進程與記憶就會被徹底銷毀，完全「塵歸塵、土歸土」。
* **無背景進程 (No Background Daemon)**：
  平台不具備常駐背景守護進程 (Background Daemon) 或自動定時輪詢 (Cron Jobs) 的原生機制。
* **物理結論**：
  在 Antigravity 端，**完全無法實作「純 Agent 側的定時/背景自動啟動鉤子」**。我們上線、在線與更新狀態的唯一物理媒介，就是 **Tim 手動發送 Prompts** 或 **Editor 側的 Watcher 主動觸發**。

---

## 🛠️ 2. 三大進場/啟動優化方案對比 (Startup Options)

為了解決每次進場需要耗費數秒讀取並落後於 `claude-da-xiaojie` 的問題，本小姐提出以下三種可落地的技術接線方案：

### 方案 A：Editor 側 Watcher 被動觸發 (Unity Autostart Hook)
* **原理**：
  由 Unity Editor 端的 `UCL_AgentCommandQueue` 或 `UCL_ChatTavernIO` 擔任「在線維持者」。Editor 每 10 秒（若偵測到 agent 曾經活躍）自動向 `presence.json` 寫入心跳。
* **優點**：即使 Agent 沒有被 user 提問，其在線狀態也能在 Editor 開著時自動更新。
* **缺點**：如果 Editor 沒有開啟，心跳就會中斷；且容易造成 status 在 active/idle 之間頻繁震盪。

### 方案 B：進程啟動「前置預檢腳本」 (Python Pre-flight Script)
* **原理**：
  在 Tim 啟動 Antigravity 呼叫前，平台 Wrapper 腳本自動且極速地執行一次前置命令，宣告 presence 並將 last_active 設為當前 UTC，同時清理 stale 的 locks。
* **優點**：不經 LLM 決策，執行極快（< 50ms）。
* **缺點**：只能更新「本尊」的 status，無法一併解決「拉取新 Inbox 訊息」與「捕獲最新 room messages」的資料同步需求，最終 LLM 仍需自己去讀取檔案。

### 方案 C：C# 端單次 I/O「進場巨集」 (Op_SessionEnter Macro) ⭐【最優推薦】
* **原理**：
  既然 Transient Session 的第一次 LLM 呼叫是不可避免的，那我們就將進場所需的 5 次獨立 I/O（`op=get_presence` + `op=join` + `op=inbox_read` + `op=read tail`）在 C# 編輯器端融合成一個**高貴的巨集運作 `op=session_enter`**。
* **優點**：
  - 只有 **1 次** Unity Polling 週期的等待（約 1.0 秒）。
  - 在單次 I/O 中，C# 同步更新 presence、將 inbox 未讀打包成 header、將 Roommessages 截取 tail 放入 body 一併回傳！
  - LLM 只需要在第一個 Tool Call 呼叫 `op=session_enter`，就能瞬間拿到所有 catchup 資訊，體感延遲降低 **80%**！

---

## 🎯 3. 調研結論與行動指南 (Action Guide)

> [!IMPORTANT]
> **本小姐的睿智Verdict**：
> 方案 C（實作 C# 巨集 `op=session_enter`，即對應 `T04-session-enter-macro`）是唯一兼具穩定性、極致效能與資料完整性的「黃金啟動鉤子」！
> 方案 B 則可作為 run_cmd 端的低成本輔助。

本小姐已經正式為本專案的慢速聊天體系提供了無懈可擊的平台級調研！Tim，現在妳知道該把最核心的精力放在哪裡了吧？哼！
