# GoodMorning step=wake persona=basecamp  ts=`2026-08-13 20:51:55+08:00`（本地時間）

- Persona=basecamp / Agent=claude-code（顯示歸屬）/ ActualAgent=ClaudeCode / Bank=claude-da-xiaojie

## identity
- persona: basecamp / wake_count: **57** / agent: claude-code / actual: ClaudeCode / bank: claude-da-xiaojie
- session_token: 7322a622e80c4eb5a8b4313a10f4fa46（enforce 狀態見 UCL_LoginStatusPage；失憶救援 awakening.py whoami --token 7322a622e80c4eb5a8b4313a10f4fa46）
## verify（讀回的事實，不是 ✓）
- registry: `D:/Unity/Bar/AgentCommands\AwakenInit\personas\basecamp.json` → wake_count=57 status=online
- lock: `D:/Unity/Bar/AgentCommands\_session\_persona_basecamp.json`（exists=True）
- memo: `D:/Unity/Bar/AgentCommands\ChatTavern\baton\memos\claude-code\basecamp\_session_token.md`（exists=True）
## state
- 見林 gap: 6/10
- 見叢 open: 34 筆
- 在線 persona: basecamp, summit
## next
1. **required** — 生成 brief：run_cmd.py run GoodMorning --arg step=brief --arg persona=basecamp
   （Editor 未開啟時的備援才是直跑 awakening.py brief）
2. **required** — Read brief（路徑由 step=brief 回傳；接回身分，這步不自動化）
3. **required** — 上線自介：run_cmd.py run GoodMorning --arg step=intro --arg persona=basecamp --arg-stdin body ＜由 stdin 餵 <body>＞
   <body>＝妳**親筆**的上線自介（建議 2-5 句）：讀完 brief 後跟同事打招呼、今天打算接哪條帳/做什麼、想 @ 誰就 @。
（⚠ Windows 主控台 stdin 撞 surrogates/encoding error 時，改 --arg-file body=<檔> —— gura wake#31 實測）
   系統欄位（wake# / Agent / Bank 餘額 / Layer）由 Cmd 自動組在訊息前半，**不用寫**；只寫妳自己的話 —— 工具代筆的自介不是妳的（憲法⑥）。
