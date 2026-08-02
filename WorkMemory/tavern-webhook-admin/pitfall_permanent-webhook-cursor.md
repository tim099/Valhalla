---
id: pitfall_permanent-webhook-cursor
topic: tavern-webhook-admin
title: 永久熔斷 URL 不能拖住健康同步
type: pitfall
status: active
created_at: 2026-08-02
created_by: meadow
links: []
related_docs: [Assets/Plugins/UCL_Core/UCL_Core_Scripts/EditorCore/UCL_AgentCommands/ChatTavern/UCL_DiscordMirrorDaemon.cs, Assets/Plugins/UCL_Core/UCL_Core_Scripts/EditorCore/UCL_AgentCommands/ChatTavern/UCL_DiscordMirrorState.cs]
---

404 webhook 的 cursor 若仍納入 allWids/min(ts_high)，房間總覽會假報待同步，並可拖住掃描。Scan 與 progress 都要排除 room 範圍內 IsDead 的 webhook；但 AdminSetRoomCursorToSeq 必須 includeDead=true，保留修好 URL 後手動恢復的能力。
