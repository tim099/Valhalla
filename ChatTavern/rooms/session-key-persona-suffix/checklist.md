# ✅ Checklist — session-key-persona-suffix

_衍生 cache；最後更新 2026-05-13 14:58:18 UTC_

- ✅ **T01-compute-session-key-persona-arg** compute_session_key(persona=None) 加 optional arg + Tier 3/4 fallback 加 suffix
- ✅ **T02-callers-pass-persona** cmd_morning / cmd_goodnight / cmd_status callers 傳 persona
- ✅ **T03-verify-fallback-no-collision** Verify Tim 場景: Tier 3 fallback 兩 persona 不撞 + Tier 2 命中時不影響
