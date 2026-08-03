---
id: pitfall_type-char-drop
topic: bartender-remote-notify
title: 逐字輸入掉字實錘（/uclding 少一槓）+ 修法方向
type: pitfall
status: active
created_at: 2026-08-03
created_by: summit
links: []
related_docs: [Assets/Plugins/UCL_Core/UCL_Core_Scripts/EditorCore/UCL_AgentCommands/Bartender/UCL_RemoteNotifyService.cs, tavern:2026-08-03#9939]
---

**實錘樣本**（2026-08-03 15:36）: 自動通知逐字輸入 `/ucl-ding`（30ms/字）打進 summit 視窗時掉了 `-` → 收到 `/uclding` → Unknown command。執行紀錄的警語「仍需目測確認對方收到幾個字」自己應驗。

**修法方向（未動工, 等排程）**:
1. type_char_delay 30ms → 50ms（保守解, 代價每則多 ~0.2s）
2. 打完後 OCR 回驗輸入框內容 == NotifyText 才按 Enter（徹底解, 走既有 locate contains 模式讀輸入框; 不符則全選重打一次）
3. 或兩者並用。掉字機率低（當日十餘發僅一例）, 但掉在指令上就是 Unknown command, 掉在參數上更毒。
