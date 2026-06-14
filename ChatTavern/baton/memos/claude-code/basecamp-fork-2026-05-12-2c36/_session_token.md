---
persona: basecamp-fork-2026-05-12-2c36
agent: claude-code
session_token: 0aa4a0c905bf4b7bb898003f568576d8
issued_at: 2026-05-18T01:48:08.879Z
claim_origin: claude-code-db18bfc4-96ae8e3a
enforce: OFF (預設)
---

# Session Token (auto-written by awakening.py morning)

## 失憶時怎麼撈回 token

```bash
awakening.py whoami --token 0aa4a0c905bf4b7bb898003f568576d8
# 或無 arg 走 env 自動推:
awakening.py whoami
```

## 三層 recovery
- 輕 (chat scroll-back 找得到 token) → `whoami --token <X>`
- 中 (chat compact 後 token 沒了) → 讀本 memo 檔
- 重 (memo / lock 都不見) → `awakening.py reissue-token --persona basecamp-fork-2026-05-12-2c36`

## Lock file
`AgentCommands\_session\_persona_basecamp-fork-2026-05-12-2c36.json` 內 session_token 欄是權威來源.
