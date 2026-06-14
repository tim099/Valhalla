# AgentCommands/_secrets/

放外部服務 token / API key 的本地資料夾。**整個資料夾 gitignored**（除了本 README 跟 `.gitignore` 自己）— 任何放進來的檔案永不入 commit。

## 目前已知 secrets

| 檔名 | 用途 | 如何取得 |
|---|---|---|
| `discord_bot_token.txt` | Discord inbound relay bot token | Discord Developer Portal → 你的 application → Bot → Reset Token → 複製整段（單行，類似 `MTU...`） |

## 兩種路徑

| 路徑 | 用途 | git 行為 |
|---|---|---|
| `<name>.txt` 明文 | bot / daemon 實際讀取的本地檔 | **永遠 gitignored** |
| `<name>.enc` 密文 | 加密後可入 git 的版本（跨機器同步用） | **commit OK** |

跨機器流程：用 `secret_install.py` 把明文 ↔ 密文互轉，passphrase 妳自己記 / 密碼管理器存（**絕不入 git、絕不過 chat**）。

## 首次設定 token（以 Discord bot 為例）

### 路徑 A — 只要本機跑（單機 / 不入 git）

1. Discord Developer Portal → 機器人頁籤 → **Reset Token** → 複製 token
2. 在這個資料夾建 `discord_bot_token.txt`，**純文字單行**貼上 token，存檔
3. 確認 `git status` **看不到** `discord_bot_token.txt`（gitignored 生效）
4. 之後 `discord_inbound_bot.py` 會自動讀此檔

### 路徑 B — 跨機器同步（推薦）

1. 走完路徑 A 把 `.txt` 弄出來
2. 跑加密：
   ```
   python AgentCommands/Tools/secret_install.py encrypt AgentCommands/_secrets/discord_bot_token.txt
   ```
   會 prompt 兩次 passphrase（妳自訂，自己記住）→ 產出 `discord_bot_token.enc`
3. `git add AgentCommands/_secrets/discord_bot_token.enc` → commit（明文不會被 add，gitignore 擋下）
4. 新機器 clone 後開 Unity Editor → daemon 偵測 `.enc` 存在但 `.txt` 缺 → **自動彈出 token install window** → 妳輸入 passphrase → 解密 → bot 自動 spawn

也可手動跑解密 CLI：
```
python AgentCommands/Tools/secret_install.py decrypt AgentCommands/_secrets/discord_bot_token.enc
```

### 路徑 B 細節

- 加密用 Fernet (AES-128-CBC + HMAC-SHA256, RFC 5869)，passphrase 經 PBKDF2-HMAC-SHA256 200k 輪 + 隨機 salt 推 key
- 同 passphrase 兩次加密產不同密文（semantically secure，diff 友善）
- 改 token 就重跑 `encrypt` → 覆蓋 `.enc` → re-commit
- Passphrase 忘了 = 密文沒救（就是 KDF 設計目的）→ 只能 reset Token + 重新走流程

## 不要做

- ❌ 不要把 token 寫進任何 `.py` / `.json` / `.md` 的 code 內（會入 commit）
- ❌ 不要把 token 寫進環境變數設定檔 commit（同上）
- ❌ 不要在這個資料夾外面建 secret 檔（gitignore 邏輯只 cover 本資料夾）

## 環境變數 override（選用）

若你不想用檔案存，也可走環境變數：

| Token | 環境變數名 |
|---|---|
| Discord bot token | `DISCORD_INBOUND_BOT_TOKEN` |

讀取優先序：**環境變數 > 檔案**。沒設環境變數時 fallback 讀檔。
