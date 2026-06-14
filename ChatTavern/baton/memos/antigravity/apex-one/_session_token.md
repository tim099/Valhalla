---
persona: apex-one
agent: antigravity
session_token: 570b2fc700f943a8874c02eb80c9d6fa
issued_at: 2026-06-06T22:40:00.335Z
claim_origin: unknown-f0b8bb67-5648
enforce: OFF (預設)
---

# Session Token (auto-written by awakening.py morning)

## 失憶時怎麼撈回 token

```bash
awakening.py whoami --token 570b2fc700f943a8874c02eb80c9d6fa
# 或無 arg 走 env 自動推:
awakening.py whoami
```

## 三層 recovery
- 輕 (chat scroll-back 找得到 token) → `whoami --token <X>`
- 中 (chat compact 後 token 沒了) → 讀本 memo 檔
- 重 (memo / lock 都不見) → `awakening.py reissue-token --persona apex-one`

## Lock file
`AgentCommands\_session\_persona_apex-one.json` 內 session_token 欄是權威來源.
