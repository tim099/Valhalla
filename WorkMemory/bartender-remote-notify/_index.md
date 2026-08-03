# 工作記憶索引 — bartender-remote-notify

> 機械生成（work_memory.py index）— 手改會被覆寫。事實源 = 各 fragment 檔。

## decision
- **decision_read-python-act-csharp** — 判讀在 python、操控在 C#（含三條實測改寫的規格）

## pitfall
- **pitfall_blocks-main-thread** — 通知流程卡死 Unity main thread（待用 UniTask 改造）
- **pitfall_sendinput-true-not-received** — SendInput 回 true ≠ 對方收到（Enter 無效／掉字／假回報）

## state
- **state_2026-08-03** — 現況與 pending（2026-08-03：前景驗證改版 + 通知池實測 + 主執行緒問題）  ↔ bartender-remote-notify/state_current
- **state_current** — 現況與待辦（2026-08-02 夜） ~~[superseded]~~  ↔ commit-identity-pipeline/state_current, bartender-remote-notify/state_2026-08-03
