# Session Identity Lock Files

> 對應 [Plan_Awakening_Init_Protocol.md](../../docs/Plan/Plan_Awakening_Init_Protocol.md) §Session Identity Consistency Phase 1

本目錄存 per-session identity lock files (`_identity_<session_key>.json`),
由 **Cmd_GoodMorning**（`step=wake`）寫入、**Cmd_GoodNight**（`step=logout`）移除 —— 登入寫入者已收斂到 C# 單端；
`awakening.py morning / goodnight` 是指路 stub（exit 2），不再碰本目錄。

## 為何需要

確保喚醒後同 session 內 sender_id 不變動 — 防 multi-session 混淆 + 銀行帳號錯亂。

## Session Key 算法

```python
def compute_session_key():
    """env-based 為主, process tree fallback (Q9b basecamp lean + apex-two ack)"""
    if env "ANTIGRAVITY_SESSION": return f"antigravity-{hash}"
    if env "CLAUDECODE": return f"claude-code-{ppid}-{cwd_hash}"
    return f"unknown-{cwd_hash}-{ppid}"
```

## Lock File Schema

```json
{
  "session_key": "claude-code-12345-abc",
  "agent": "claude-code",
  "model": "claude-sonnet",
  "persona": "basecamp",
  "bank_account": "claude-da-xiaojie",
  "locked_at": "2026-05-12T07:50:00Z",
  "expires_at": "2026-05-13T07:50:00Z"
}
```

## 不入 git

`*.json` 走 `.gitignore` (見 repo root `.gitignore` 末段「Awakening Init Protocol session lock files」)。
本 README.md 入 git 作為 dir marker + 設計文檔。
