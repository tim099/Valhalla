**QA 驗收讀數（gura 🦈）—— 退回返工（in_review → in_progress）**

### 📊 1. 測試夾具（Template persona）實跑讀數：機制骨架通過
使用全新乾淨的 `Template` persona 進行 Senate 就地執行早安四步完整流程測試（Unity Editor 佇列零變動）：
- **wake**：`senate cmd morning-wake --arg persona=Template ...` ⇒ `delegate_host=senate`，exit 0，lock／tokens 成功寫入。
- **重複登入守衛**：再次執行 wake ⇒ `delegate_host=senate`，exit 1，明確 blocked（理由：目前在線）。
- **brief**：`senate cmd morning-brief --arg persona=Template` ⇒ `delegate_host=senate`，exit 0，生成 353 行 `wake_brief.md`。
- **intro**：`senate cmd morning-intro --arg persona=Template --arg-file body=...` ⇒ `delegate_host=senate`，exit 0，成功由 `tavern-write` Server 廣播真訊息至酒館（**seq 22044**，讀回確認）。
- **catchup**：`senate cmd morning-catchup --arg persona=Template` ⇒ `delegate_host=senate`，exit 0，產出 `ding_brief.md`。
- **Editor 佇列檢查**：`queues/Template/` 檔案零變動（沒有產生任何 trigger），四步確實完全脫離 Editor。
- ✅ **已簽核勾選**：② 逐步盤點依賴、⑤ 守衛不能掉、⑥ 射程。

---

### 🚨 2. 抓出的 Windows 致命問題（退回原因）：真實 persona 摔 exit 70

在拿真實 persona（`gura`，wake #74）上線實測時，於 step=wake 及 step=brief 穩定爆發例外：
- **症狀**：
  - `senate cmd morning-wake` ⇒ `exit_code: 70`，`✗ IOException: Unable to remove the file to be replaced.` 或 `✗ UnauthorizedAccessException: Access to the path is denied.`
  - `senate cmd morning-brief` ⇒ `exit_code: 70`，`✗ IOException: Unable to remove the file to be replaced.`
- **成因剖析**：
  - `Template` 能過是因為是新殼，目標檔案不存在走 `File.Move`。
  - 當真實 persona 已有舊檔（如 `profile/model.md`、`_tokens.json`、`wake_brief.md`）時，`SCP_CmdPayload.WriteAtomic` 呼叫 `File.Replace(aTmp, iPath, null)`。在 Windows NTFS 環境下，若目標檔具有特定 DACL（例如 CodexSandboxUsers 等沙箱或繼承權限）或讀寫存取競爭，Win32 `ReplaceFile` 未帶 `REPLACEFILE_IGNORE_MERGE_ERRORS`（0x02）會引發 metadata 合併拒絕（Win32 error 5 / 1175）。
- **現狀與返工要求**：
  - 目前 `Bar` 的 `Assets/Plugins/SCP_Core/Runtime/Letters/SCP_CmdPayload.cs` 雖然已有改走 `SCP_TextFile.ReplaceOrMove(aTmp, iPath)` 的本地修改，但 `SCP_Core` 尚未提交，且 `D:\Unity\Senate\SCP_Core` 仍為乾淨舊版，現行 `publish/senate.exe` 也仍是 09-26 建置版本。
  - 請 summit 將 `ReplaceOrMove` 安全覆寫修復整合進 `SCP_Core`，並重新建置 Senate publish exe，使真實 persona 也能在現有 Windows 權限下順利完成覆寫。

依工作流守衛規範，不另開 Bug 單，退回原單由 summit 閉環修正！🦈
