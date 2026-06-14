---
persona: calli
agent: claude-code
session_token: a2c66987da51478f8096cd1076fa4771
issued_at: 2026-06-10T05:33:00.789Z
claim_origin: claude-code-0665890a-d1d736e1
enforce: OFF (預設)
---

# Session Token (auto-written by awakening.py morning)

## 失憶時怎麼撈回 token

```bash
awakening.py whoami --token a2c66987da51478f8096cd1076fa4771
# 或無 arg 走 env 自動推:
awakening.py whoami
```

## 三層 recovery
- 輕 (chat scroll-back 找得到 token) → `whoami --token <X>`
- 中 (chat compact 後 token 沒了) → 讀本 memo 檔
- 重 (memo / lock 都不見) → `awakening.py reissue-token --persona calli`

## Lock file
`AgentCommands\_session\_persona_calli.json` 內 session_token 欄是權威來源.
