# ✅ Checklist — session-key-collision-fix

_衍生 cache；最後更新 2026-05-13 13:08:46 UTC_

- ✅ **T01-collision-detect-status** awakening.py status: 偵測 session_key 多 lock collision + 顯示 pid/locked_at + 移除 single-key ownership 假設 (owner: gemini)
- ✅ **T02-morning-strict-on-collision** cmd_morning: 偵測 collision 且 caller 沒帶 --persona → 拒絕 reuse + 要求 --strict-persona 顯式指定
- ✅ **T03-claude-md-update** CLAUDE.md MVP 限制條目: 從「session_key 不穩」改成「collision 偵測+顯式 fallback ship」
