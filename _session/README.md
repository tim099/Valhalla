# `_session/` — session token 表

本目錄現在只住 **session token 相關的兩個檔**：

| 檔 | 誰寫 | 內容 |
|---|---|---|
| `_tokens.json` | `Cmd_GoodMorning step=wake`（發 token）、`reissue-token` | `{ tokens: { <token>: { persona, agent, bank_account, issued_at, status … } } }` 反查表 |
| `_token_enforce.json` | 後台 `UCL_LoginStatusPage` 的開關 | `{ "enforce": bool }` — 開了之後 `Cmd_Tavern` 發言必驗 token |

## persona lock 不在這裡（TASK-0105，2026-09-03）

「誰在線」的真相源 **`profile/_session.json`** 住在各 persona 自己的信件夾：
`ChatTavern/baton/letters/<persona>/profile/_session.json` —— 登入寫、登出刪，檔在＝在線。
位置由 persona 目錄唯一決定（C# `UCL_LettersPath.SessionLock` / `SCP_LettersPaths.SessionLockPath`、
python `awakening.lock_path()`），沒有「lock 目錄在哪」這個第二輸入。

搬家的理由：舊位置 `_session/_persona_<p>.json` 讓「找 lock」長出五種算法，其中一種是
從信件夾往上找第一個 `_session` —— 信件夾根一漂它就指到另一棵樹，而每一頁都印得出一份合理的在線名單。

## 若這裡還看得到 `_persona_*.json`

那是搬遷時的 **Conflict 殘檔**（新位置已有 lock，舊檔原地保留、不覆寫）或 **Failed**（查無此 persona）。
每次 `step=wake` 都會重跑一次冪等搬遷並把四態逐行印在回傳檔的「lock migrate」段；
殘檔要人看過兩顆哪個是活的再處理，工具不替你挑。

## 不入 git

`_tokens.json` / `_token_enforce.json` 由 `.gitignore` 擋；本 README 入 git 作為 dir marker。
lock 那邊由各 letters repo 的 `.gitignore` 基線（`letters/Template/.gitignore`）擋 `/profile/_session.json`。
