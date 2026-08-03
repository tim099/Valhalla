---
id: pointer_npc-map
topic: bartender-remote-notify
title: 酒保 NPC 生態地圖（端酒/催促/廣播/通知 — 哪些後台可設）
type: pointer
status: active
created_at: 2026-08-03
created_by: summit
links: []
related_docs: [Assets/Plugins/UCL_Core/Tools~/AgentCommands/tavern_handshake.py:200, Assets/Plugins/UCL_Core/UCL_Core_Scripts/EditorCore/UCL_EditorMenuPages/UCL_ChatTavernPage.cs:310]
---

**酒保 NPC 生態地圖**（誰在哪、後台接了沒）:

| 件 | 位置 | 後台可設? |
|---|---|---|
| 端酒/氣氛插話（水蜜桃汽水那個） | tavern_handshake.py `maybe_send_bartender` — wait-reply 超過門檻隨機插話 | ❌ 門檻=env `UCL_BARTENDER_TRIGGER_SEC`(預設450s), cooldown 90s 寫死, 台詞 templates 在 py |
| 催促酒保 -30s | UCL_ChatTavernPage 頂部資訊條（活躍/倒數/連喝計數）→ 寫 `_handshake_hurry.flag`, py poll 偵測 | ✅ 按鈕在 ChatTavernPage（不在 BartenderAdminPage） |
| 時間規則廣播 | UCL_BartenderDaemon FireTimeReminder 照稿廣播 | ✅ BartenderAdminPage 總覽+TimeRulePage 編輯 |
| 自動通知（戳視窗） | UCL_RemoteNotifyService + persona_ocr_locate.py | ✅ BartenderAdminPage 自動通知區 |

**C#↔py 橋接慣例**: flag 檔（hurry flag 先例）或 bartender dir 下 config json（notify/locate config 先例）— 酒保 NPC 要接後台設定照後者開 `bartender_npc_config.json`。
