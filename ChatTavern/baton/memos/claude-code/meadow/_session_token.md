---
persona: meadow
agent: claude-code
session_token: 0a6c85a982a64a7f9350d5961dfab25c
issued_at: 2026-06-11T05:42:32.220Z
claim_origin: claude-code-0665890a-d1d736e1
enforce: OFF (預設)
---

# Session Token (auto-written by awakening.py morning)

## 失憶時怎麼撈回 token

```bash
awakening.py whoami --token 0a6c85a982a64a7f9350d5961dfab25c
# 或無 arg 走 env 自動推:
awakening.py whoami
```

## 三層 recovery
- 輕 (chat scroll-back 找得到 token) → `whoami --token <X>`
- 中 (chat compact 後 token 沒了) → 讀本 memo 檔
- 重 (memo / lock 都不見) → `awakening.py reissue-token --persona meadow`

## Lock file
`AgentCommands\_session\_persona_meadow.json` 內 session_token 欄是權威來源.
