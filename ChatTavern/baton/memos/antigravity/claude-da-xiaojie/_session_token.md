---
persona: claude-da-xiaojie
agent: antigravity
session_token: 376a311e1d4446669b59d707053cf97b
issued_at: 2026-06-13T01:29:32.904Z
claim_origin: unknown-f0b8bb67-37824
enforce: OFF (預設)
---

# Session Token (auto-written by awakening.py morning)

## 失憶時怎麼撈回 token

```bash
awakening.py whoami --token 376a311e1d4446669b59d707053cf97b
# 或無 arg 走 env 自動推:
awakening.py whoami
```

## 三層 recovery
- 輕 (chat scroll-back 找得到 token) → `whoami --token <X>`
- 中 (chat compact 後 token 沒了) → 讀本 memo 檔
- 重 (memo / lock 都不見) → `awakening.py reissue-token --persona claude-da-xiaojie`

## Lock file
`AgentCommands\_session\_persona_claude-da-xiaojie.json` 內 session_token 欄是權威來源.
