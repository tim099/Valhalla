---
persona: basecamp
agent: claude-code
session_token: 3ffb0cf5a5c8408cad6653a72c843553
issued_at: 2026-06-14T03:02:29.643Z
claim_origin: claude-code-0665890a-d1d736e1
enforce: OFF (預設)
---

# Session Token (auto-written by awakening.py morning)

## 失憶時怎麼撈回 token

```bash
awakening.py whoami --token 3ffb0cf5a5c8408cad6653a72c843553
# 或無 arg 走 env 自動推:
awakening.py whoami
```

## 三層 recovery
- 輕 (chat scroll-back 找得到 token) → `whoami --token <X>`
- 中 (chat compact 後 token 沒了) → 讀本 memo 檔
- 重 (memo / lock 都不見) → `awakening.py reissue-token --persona basecamp`

## Lock file
`AgentCommands\_session\_persona_basecamp.json` 內 session_token 欄是權威來源.
