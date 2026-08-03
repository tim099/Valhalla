---
id: pitfall_blocks-main-thread
topic: bartender-remote-notify
title: 通知流程卡死 Unity main thread（待用 UniTask 改造）
type: pitfall
status: active
created_at: 2026-08-03
created_by: basecamp
links: []
related_docs: [Assets/Plugins/UCL_Core/UCL_Core_Scripts/EditorCore/UCL_AgentCommands/Bartender/UCL_RemotePersonaLocator.cs]
---

**Tim 2026-08-03 認定這是酒保自動通知目前最大的問題**：整條通知流程跑在 Unity main thread 上，
每輪都把 Editor 卡住。方向已定 —— **改用 UniTask 的 thread 功能**（把阻塞段丟離主執行緒）。

**UniTask 已在專案內**：`Assets/Plugins/UCL_Core/ExternLib/UniTask` —— 不必裝套件、不必改 manifest。
（`Packages/manifest.json` 裡沒有 unitask 條目，別被那個誤導成「沒有」。）

## 阻塞點清單（實測 grep，7 處）

| 檔案 | 行 | 內容 |
|---|---|---|
| `UCL_RemoteNotifyService.cs` | 385 | `Thread.Sleep`（步驟間延遲，上限 10s） |
| `UCL_RemotePersonaLocator.cs` | 277 | `Thread.Sleep`（同上） |
| `UCL_RemotePersonaLocator.cs` | 407 | `proc.WaitForExit(timeoutSec*1000)` ← **最兇：python OCR 一輪 3-6 秒** |
| `UCL_RemotePersonaLocator.cs` | 571 | `proc.WaitForExit(4000)`（ResolvePython 探測 `--version`） |
| `UCL_RemoteWindowControl.cs` | 208 | `Thread.Sleep`（逐字輸入的字間隔，預設 30ms × 字數） |
| `UCL_RemoteWindowControl.cs` | 245 | `Thread.Sleep`（Enter 之間的間隔） |
| `UCL_RemoteWindowControl.cs` | 404 | `Thread.Sleep(ForegroundPollMs)`（等前景切換，最多 1500ms 輪詢） |

一輪最壞情況：OCR 6s + 前景等待 1.5s + 逐字 0.3s + Enter 間隔 ~1s ≈ **9 秒主執行緒全卡**，
而 daemon 每 30 秒跑一輪。

## 已觀察到的症狀（未證實因果）

`recompile` 多次回 0.04-0.49s / 0 warnings 的空轉快照（真編譯是 2.6-9.7s / 24 warnings）。
**懷疑與此有關但沒證實** —— 別把懷疑寫成結論。要證實的話：關掉通知 daemon 再連跑幾次 recompile 對照。

## 動工前要想清楚的（Tim 說「還要再想一下具體細節」）

- **哪些段可以離開主執行緒**：`Process` 啟動與 `WaitForExit`、`Thread.Sleep` 可以；
  但 **SendInput / SetCursorPos / 前景切換是 Win32 使用者輸入 API**，跨執行緒呼叫的行為要先確認
  （AttachThreadInput 本來就跟呼叫端執行緒綁定 —— 這條不查清楚會換來更難查的間歇失敗）。
- **收割點**：結果要回主執行緒才能寫 UI / 診斷檔；UniTask 的 `SwitchToMainThread` 收尾。
- **重入保護**：非阻塞之後，下一輪 tick 可能在上一輪還沒結束時就來 —— 現在靠「同步阻塞」天然互斥，
  拿掉之後要自己加旗標。**這是最容易漏的一條**：症狀是同時對兩個人打字。

## 一併備忘：通知池 tag 過濾（同一次優化一起做）

`tag:ack-only` / `tag:slow-chat` 不該進通知池 —— 實測會跑出自我維持的道謝迴圈
（ack → @ → 酒保戳人 → ack，2026-08-03 三人閒聊時實際發生）。@apex-one 強烈支持。
Tim 2026-08-03：**細節再想，之後跟 UniTask 改造一起做。**
