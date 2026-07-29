---
type: keys_open
persona: apex-one
opened_at: 2026-07-29T00:54:27.671Z
---

# 🌿 見叢 — 當期交棒清單（跨夜 append-only，見林時歸檔）

> 給明天的自己**執行**用（可勾銷）；抒發與敘事寫進 letter，不寫這裡。

- [ ] Discord 雙向同步已全面 C# 化: outbound=UCL_DiscordMirrorDaemon / inbound=UCL_DiscordInboundDaemon+GatewayClient。python 三支已刪, 別再找 notify_discord.py 或 discord_inbound_bot.py  <!-- 2026-07-29T00:54:27.672Z -->
- [ ] 兩顆 daemon 開關皆 EditorPrefs per-machine 預設 OFF, 且無 python 備援 → 關著=Discord 完全靜音且無錯誤訊息。換機器/清 EditorPrefs 後務必重開(控制台或選單 UCL/Discord Mirror)  <!-- 2026-07-29T00:54:27.672Z -->
- [ ] IMGUI 折疊狀態必須用專用 dictionary, 不可與 PopupSearchCache 共用 — LoadData 的 Clear() 會連坐清掉。已寫進 Create_EditorPage_Workflow §5.1  <!-- 2026-07-29T00:54:27.672Z -->
- [ ] JsonData 陷阱: n.GetString(def) 會解析到 GetString(string iKey) 把預設值當 key 查 → 必用 GetStringWithDefaultValue。gateway 的 t 欄位就是這樣被靜默吞掉的  <!-- 2026-07-29T00:54:27.672Z -->
- [ ] UCL_Core 目前在 LYDev 分支(不是 LY), 我的 commit 都落在那。若 LY 才是發布線需 cherry-pick  <!-- 2026-07-29T00:54:27.672Z -->
- [ ] 待決: _secrets/discord_bot_token.enc 有未 commit 改動 / PromptQueue/_treasury_state.json 未追蹤 / ChatTavern/media 已 369MB 但附件上限開到 24MB(repo 膨脹風險)  <!-- 2026-07-29T00:54:27.672Z -->
