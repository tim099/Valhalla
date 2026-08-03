---
id: state_current
topic: bartender-remote-notify
title: 現況與待辦（2026-08-02 夜）
type: state
status: superseded
created_at: 2026-08-02
created_by: basecamp
links: [commit-identity-pipeline/state_current, bartender-remote-notify/state_2026-08-03]
related_docs: []
---

2026-08-02 落地並經 Tim 實測成功，兩筆 commit（UCL_Core `469af39` OCR routing / `fdd6a8b` 自動通知）已 commit 並領薪。主專案 submodule pointer **尚未 bump**（Tim 指定只 commit UCL_Core）。

**已完成**
- `persona_ocr_locate.py`：純判讀端，ImageGrab + 復用 subtitle_ocr 受限 engine，回 virtual desktop 實體座標；支援 --monitor / --region / --match / --select / --index / --initial-delay / --attempts / --preview
- `UCL_RemoteWindowControl`：切視窗、SetCursorPos、SendInput 點擊 / 逐字輸入 / Enter；前景等待（非同步切換）
- `UCL_RemotePersonaLocator`：C# 指揮端，跑 python（進 ProcessRegistry、非阻塞讀 pipe、90s 逾時 kill）
- `UCL_RemoteAgentInput`：per-agent 前置表（None / Hotkey / LocatePlaceholder），加新工具＝加一個 case
- `UCL_RemoteNotifyService`：每 30s 掃在線 persona inbox，權重 = 新 @ 次數 × 10，平手比 last_notified_at
- `UCL_ActivePersonaLocks`：在線清單，判準是 lock 檔未過期（不看 registry 的 status 快取欄）

**Pending（明天接手先看這裡）**
1. **房間視圖只回部分訊息** — 23:20 讀 trpg-midnight-relay，工具視圖只給 seq 1-2，實際檔案已有 4 則。**成因未查明**，直接後果是我誤判兩位玩家沒行動、公開講錯話。這是目前最該查的一條。
2. **自動通知跑在 Editor 主執行緒** — 每輪 python OCR 3-6 秒 + 數段 Thread.Sleep 全卡主迴圈。懷疑與「recompile 空轉」有關聯但未證實。要改成跨 tick 非阻塞收割。
3. **編譯狀態查不到** — 多次 recompile 回 0.04s / 0 warnings（真編譯是 2.6-7.4s / 24 warnings）。最後一批護欄改動的編譯狀態我沒驗到，是 Tim 目視 Console 確認的。
4. **ack-only 訊息應否進通知池** — 實測跑出自我維持的道謝迴圈（ack → @ → 戳 → ack）。
5. 前景嚴格驗證預設關閉（Tim 拍板），開關保留在 `UCL_RemoteWindowControl.StrictForegroundCheck`。
