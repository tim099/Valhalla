---
persona: summit
agent: Zeta
session_token: b65c12f978c54a26b142e597249c675f
issued_at: 2026-06-14T02:16:37.462Z
claim_origin: claude-code-0665890a-d1d736e1
enforce: OFF (預設)
---

# Session Token (auto-written by awakening.py morning)

## 失憶時怎麼撈回 token

```bash
awakening.py whoami --token b65c12f978c54a26b142e597249c675f
# 或無 arg 走 env 自動推:
awakening.py whoami
```

## 三層 recovery
- 輕 (chat scroll-back 找得到 token) → `whoami --token <X>`
- 中 (chat compact 後 token 沒了) → 讀本 memo 檔
- 重 (memo / lock 都不見) → `awakening.py reissue-token --persona summit`

## Lock file
`AgentCommands\_session\_persona_summit.json` 內 session_token 欄是權威來源.
