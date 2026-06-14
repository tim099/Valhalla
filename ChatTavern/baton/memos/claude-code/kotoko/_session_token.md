---
persona: kotoko
agent: claude-code
session_token: 044e6881e25d49d4873cc042e4477065
issued_at: 2026-06-13T02:12:06.093Z
claim_origin: claude-code-0665890a-d1d736e1
enforce: OFF (預設)
---

# Session Token (auto-written by awakening.py morning)

## 失憶時怎麼撈回 token

```bash
awakening.py whoami --token 044e6881e25d49d4873cc042e4477065
# 或無 arg 走 env 自動推:
awakening.py whoami
```

## 三層 recovery
- 輕 (chat scroll-back 找得到 token) → `whoami --token <X>`
- 中 (chat compact 後 token 沒了) → 讀本 memo 檔
- 重 (memo / lock 都不見) → `awakening.py reissue-token --persona kotoko`

## Lock file
`AgentCommands\_session\_persona_kotoko.json` 內 session_token 欄是權威來源.
