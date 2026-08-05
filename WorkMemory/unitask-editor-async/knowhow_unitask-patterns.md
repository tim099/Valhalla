---
id: knowhow_unitask-patterns
topic: unitask-editor-async
title: UniTask 實戰模式六條 + 症狀觸發清單（Editor 卡住→想到這篇）
type: knowhow
status: active
created_at: 2026-08-03
created_by: summit
links: [bartender-remote-notify/state_2026-08-03, compile-verification/pitfall_three-layer-false-green]
related_docs: [Assets/Plugins/UCL_Core/UCL_Core_Scripts/EditorCore/UCL_AgentCommands/Bartender/UCL_RemotePersonaLocator.cs:409, Assets/Plugins/UCL_Core/UCL_Core_Scripts/EditorCore/UCL_EditorMenuPages/UCL_BartenderAdminPage.cs, Assets/Plugins/UCL_Core/UCL_Core_Scripts/EditorCore/UCL_AgentCommands/Bartender/UCL_RemoteNotifyService.cs]
---

**觸發情境（看到這些症狀就該想到本篇）**: Editor 卡住 / 凍結 / 轉圈 / 無回應; 按鈕按下去整個 Unity 停住幾秒~幾十秒; 外部 process（python OCR / 截圖 / 網路）在主執行緒同步等待; OnGUI 裡直接跑重活。

**核心解法**: 同步阻塞呼叫 → `async UniTask` 化。Editor 模式完全可用（UniTask 的 continuation 走 EditorApplication.update, 恢復點在主執行緒 — await 之後可以安全碰 Unity API）。

**本 repo 實戰模式（2026-08-03 Tim 主刀 AdminPage async 化, 全部可抄）**:
1. **阻塞外部 process 包 Task.Run**: `await Task.Run(() => process.WaitForExit(...))` — UCL_RemotePersonaLocator.RunScript:409。CPU/IO 重活丟 thread pool, await 回來自動落主執行緒。
2. **fire-and-forget 掛 .Forget()**: 按鈕 handler 不能 await → `SomeAsync().Forget()`（Cysharp.Threading.Tasks）。
3. **防重入 guard 旗標要活過整段 async**: 旗標在 async 方法內部 set/finally-reset（UCL_BartenderAdminPage.ListMonitors 模式）。⚠ 反例: `try { X().Forget(); } finally { flag=false; }` — Forget 立刻返回, 旗標同幀放掉等於沒鎖（2026-08-03 實踩）。
4. **⚠ IMGUI 繪製方法禁 async**: OnGUI 呼叫鏈裡的 Draw 方法若 async 且中途 await, 恢復點落在 OnGUI 之外 → GUILayout layout exception。繪製保持同步, 只把資料載入拆成 async（DrawLocateScanSettings 警語）。
5. **async 化時 out 參數會消失**: `bool F(out string err)` → `async UniTask<(bool ok, string err)>` — 呼叫端漏接 tuple 的 err 就是靜默失敗（RefreshLocatePreview 實踩, 失敗必須把 err 落到 UI/log）。
6. **Editor 端等待別用 Thread.Sleep**（會卡主執行緒）→ `await UniTask.Delay(...)`; 真的要同步小睡限制在非主執行緒（Task.Run 內）。

**踩坑史**: 2026-08-03 AdminPage 自動通知/OCR 定位流程原為同步 — 每次 OCR 跑 python 子程序數秒~數十秒, Editor 主執行緒全程凍結影響基本操作 → Tim 全面 async 化（UCL_RemoteNotifyService.RunOnce / RunCursorTest / CapturePreview / ListMonitors 全改 async UniTask）。
