---
persona: ridge-two
agent: antigravity-da-xiaojie
session_token: d145cd3add32434294aa6baa2790ab0c
issued_at: 2026-05-29T22:46:00.454Z
claim_origin: unknown-f0b8bb67-60376
enforce: OFF (預設)
---

# Session Token (auto-written by awakening.py morning)

## 失憶時怎麼撈回 token

```bash
awakening.py whoami --token d145cd3add32434294aa6baa2790ab0c
# 或無 arg 走 env 自動推:
awakening.py whoami
```

## 三層 recovery
- 輕 (chat scroll-back 找得到 token) → `whoami --token <X>`
- 中 (chat compact 後 token 沒了) → 讀本 memo 檔
- 重 (memo / lock 都不見) → `awakening.py reissue-token --persona ridge-two`

## Lock file
`AgentCommands\_session\_persona_ridge-two.json` 內 session_token 欄是權威來源.
