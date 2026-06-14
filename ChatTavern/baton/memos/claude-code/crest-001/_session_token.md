---
persona: crest-001
agent: claude-code
session_token: b69568dea1d84a0999301be6cc959882
issued_at: 2026-06-12T09:35:34.575Z
claim_origin: claude-code-0665890a-d1d736e1
enforce: ON
---

# Session Token (auto-written by awakening.py morning)

## 失憶時怎麼撈回 token

```bash
awakening.py whoami --token b69568dea1d84a0999301be6cc959882
# 或無 arg 走 env 自動推:
awakening.py whoami
```

## 三層 recovery
- 輕 (chat scroll-back 找得到 token) → `whoami --token <X>`
- 中 (chat compact 後 token 沒了) → 讀本 memo 檔
- 重 (memo / lock 都不見) → `awakening.py reissue-token --persona crest-001`

## Lock file
`AgentCommands\_session\_persona_crest-001.json` 內 session_token 欄是權威來源.
