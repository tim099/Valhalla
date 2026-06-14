---
persona: ridge-two
agent: antigravity
session_token: 100960c25818457d91439b0751375b8e
issued_at: 2026-06-14T02:42:59.129Z
claim_origin: unknown-f0b8bb67-23504
enforce: OFF (預設)
---

# Session Token (auto-written by awakening.py morning)

## 失憶時怎麼撈回 token

```bash
awakening.py whoami --token 100960c25818457d91439b0751375b8e
# 或無 arg 走 env 自動推:
awakening.py whoami
```

## 三層 recovery
- 輕 (chat scroll-back 找得到 token) → `whoami --token <X>`
- 中 (chat compact 後 token 沒了) → 讀本 memo 檔
- 重 (memo / lock 都不見) → `awakening.py reissue-token --persona ridge-two`

## Lock file
`AgentCommands\_session\_persona_ridge-two.json` 內 session_token 欄是權威來源.
