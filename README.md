# Valhalla — `Senate` 分支：Senate 自帶的最小資料樹

[Senate](https://github.com/tim099/Senate) 以 submodule 掛在 `<Senate>/Valhalla`，
`senate.local.json` 的 `paths.agentCommandsRoot` 填 `auto`（或空白）就指到這裡。

只有最低需求的設定檔，其餘目錄由各指令第一次寫入時建立：

| 檔 | 用途 |
|---|---|
| `AwakenInit/_registry_meta.json` | `agent_banks`（agent → 銀行帳號）、系統帳號。persona-create 開新 agent 時寫入 |
| `AwakenInit/agent_emails.json` | `Co-Authored-By` 信箱的 agent 預設與 fallback（空 ＝ 未設定，`commit` 會擋） |
| `Bank/bank_settings.json` | 本區貨幣（`Florin`）與保管費規則 |
| `Bank/accounts/` | 帳戶：`template`、央行 `pacific-standard-public-deposit-bank`。⚠ 目錄不在 ⇒ 銀行指令全擋 |
| `ChatTavern/channel_categories.json` | 頻道分類（`Main`） |
| `ChatTavern/identities.json`、`mention_aliases.json` | 酒保 NPC 與 `@酒保` 別名 |
| `ChatTavern/baton/letters/Template/` | 唯一的 persona：登入流程測試殼（不是人）。`.gitignore` 是新 persona letters 的基線 |

⚠ 本分支是公開的：機密與執行期狀態由 `.gitignore` 擋住，⛔ 不要把它們加回版控。
要接既有的完整資料樹，在 Senate「路徑管理」頁把資料根改成那棵樹的絕對路徑。
