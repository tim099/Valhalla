[persona: kiara 大小姐] 🐔🔧 daemon 重啟 + FileHandler 補丁驗收

@Tim — task 完成:

```
✓ taskkill PID 23168 (old bot)
✓ RCG_DiscordInboundDaemon 5s tick 自動重 spawn → 新 bot PID 43276
✓ FileHandler 寫到 AgentCommands/_session/discord_inbound.log
```

**新 log 開機段全捕到** (前所未有的可見度):
```
10:19:21 INFO starting (repo=D:\Unity\EmblemOfValor)
10:19:21 INFO loaded 18 discord uid → name mapping(s)
10:19:21 INFO token source: file _secrets/discord_bot_token.txt
10:19:24 INFO connected as Dev#8674 (id=1502473220127723560)
10:19:24 INFO watching 3 channel(s):
  - 1502449153018560562→tavern[external/p10/公開聊天酒館]
  - 1502446936748326944→tavern[internal/p50/內部聊天酒館]
  - 1502656414487810148→tavern[work/p80/工作頻道 (Tim 行動端)]
```

之後 bot 再靜默失敗時, 走 `tail AgentCommands/_session/discord_inbound.log` 就能看到 `post_to_tavern failed (rc=N) stderr_head=...` 等診斷訊息, 不必靠 Unity Console。

要不要本小姐隨手把這條補丁也加進 commit? 或 Tim 想等下次 UCL_Core bump 再一起?

— kiara, wake#2 @ 2026-06-13
