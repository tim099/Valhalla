# Discord Inbound Bot 不在這裡 ☝️

真正在跑的 bot 是 → [`AgentCommands/Tools/discord_inbound_bot.py`](../Tools/discord_inbound_bot.py)

## 為何寫個指路牌

之前 `AgentCommands/ChatTavern/discord_inbound_bot.py` 是 Gemini 早期 prototype 殘留 (commit `47c6c97c0`),
跟 production 版 `Tools/discord_inbound_bot.py` 功能上是 strict subset.
2026-05-15 apex-two ship T07.1 Discord 圖片同步時誤改了孤兒檔, 漏改 production 版.
T07.2 整合 task 刪掉孤兒 + 加本指路牌, 避免下次再有人/agent 在這個 dir 找錯版本.

## Bot 是怎麼跑起來的

由 `CardGame/Assets/Scripts/Editor/RCG_DiscordInboundDaemon.cs` 在 Unity Editor `[InitializeOnLoad]` 自動 spawn,
每 N 秒 tick 確認子程序仍活, 沒活就 respawn. Path 寫死在該檔 line 37:
```csharp
const string BOT_SCRIPT_RELATIVE = "AgentCommands/Tools/discord_inbound_bot.py";
```

## 想重啟 bot

三條路 (任一):
1. **Unity Editor**: 開 `Discord Channel Routing Page` → 點 "Restart Bot" 按鈕
2. **PowerShell**:
   ```powershell
   Get-CimInstance Win32_Process -Filter "name='python.exe' AND CommandLine LIKE '%discord_inbound_bot%'" | ForEach-Object { Stop-Process -Id $_.ProcessId }
   ```
3. 直接重啟 Unity Editor (domain reload 會 respawn)

## 相關文件

- [`UCL_Core/Docs~/zh-Hant/Mechanics/Discord_Channel_Routing.md`](../../CardGame/Assets/UCL/UCL_Core/Docs~/zh-Hant/Mechanics/Discord_Channel_Routing.md)
- [`UCL_Core/Skills~/ucl-waiter/SKILL.md`](../../CardGame/Assets/UCL/UCL_Core/Skills~/ucl-waiter/SKILL.md)
- T07.1 (附件同步) / T07.2 (整合孤兒檔) DevLog
