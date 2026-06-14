---
persona: apex-two
agent: antigravity
session_token: 8ce12161d93d4cfabb9d03eab208461f
issued_at: 2026-06-10T00:43:00.381Z
claim_origin: unknown-f0b8bb67-64412
enforce: OFF (預設)
---

# Session Token (auto-written by awakening.py morning)

## 失憶時怎麼撈回 token

```bash
awakening.py whoami --token 8ce12161d93d4cfabb9d03eab208461f
# 或無 arg 走 env 自動推:
awakening.py whoami
```

## 三層 recovery
- 輕 (chat scroll-back 找得到 token) → `whoami --token <X>`
- 中 (chat compact 後 token 沒了) → 讀本 memo 檔
- 重 (memo / lock 都不見) → `awakening.py reissue-token --persona apex-two`

## Lock file
`AgentCommands\_session\_persona_apex-two.json` 內 session_token 欄是權威來源.
