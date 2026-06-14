# ✅ Checklist — discord-routing

_衍生 cache；最後更新 2026-05-15 02:15:46 UTC_

- 🔒 **T01-routing-schema** 新 channel routing JSON schema + 預載 2 channel (owner: claude-da-xiaojie)
- ⏳ **T02-bot-enriched-meta** discord_inbound_bot.py 讀新 routing + meta 帶 source_class/priority/channel_label
- ✅ **T03-waiter-priority-sort** waiter_session.py cycle priority desc sort + 回 source_class 給 agent
- ✅ **T04-imgui-page** UCL_DiscordChannelRoutingPage IMGUI CRUD 編輯介面 (owner: claude-da-xiaojie)
- ✅ **T05-parsemeta-fix** Cmd_Tavern.ParseMeta JSON 自動偵測 fix (pre-existing bug, blocking T02 meta) (owner: claude-da-xiaojie)
- ✅ **T06-echo-fix** 處理回音問題 (Discord → tavern → mirror → Discord echo 迴圈) - Tim 3 token (owner: claude-da-xiaojie)
