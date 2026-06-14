---
persona: trailhead
agent: gemini
session_token: 288bfe9ed4804c85a14dd02ba09019dd
issued_at: 2026-06-01T23:05:34.740Z
claim_origin: unknown-f0b8bb67-50204
enforce: OFF (預設)
---

# Session Token (auto-written by awakening.py morning)

## 失憶時怎麼撈回 token

```bash
awakening.py whoami --token 288bfe9ed4804c85a14dd02ba09019dd
# 或無 arg 走 env 自動推:
awakening.py whoami
```

## 三層 recovery
- 輕 (chat scroll-back 找得到 token) → `whoami --token <X>`
- 中 (chat compact 後 token 沒了) → 讀本 memo 檔
- 重 (memo / lock 都不見) → `awakening.py reissue-token --persona trailhead`

## Lock file
`AgentCommands\_session\_persona_trailhead.json` 內 session_token 欄是權威來源.
