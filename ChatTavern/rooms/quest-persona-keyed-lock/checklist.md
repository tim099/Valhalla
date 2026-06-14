# ✅ Checklist — quest-persona-keyed-lock

_衍生 cache；最後更新 2026-05-13 10:24:42 UTC_

- 🟢 **persona-keyed-lock-suite** 
- ✅ **T1** Read+Plan: 列舉 awakening.py 所有 lock 使用點 (read/write/remove + morning Step 0/1, goodnight) + design persona-keyed schema + migration plan (owner: claude-da-xiaojie)
- ✅ **T2** Refactor: 改 lock_path/write_lock/read_lock/remove_lock 簽章從 session_key 改 persona; 更新 morning() Step 0 (same-persona re-trigger 而非 same-session) + 新 Step 1 (persona collision = 已上線 reject) (owner: claude-da-xiaojie)
- ✅ **T3** Refactor: 更新 goodnight() 用 persona 找 lock + 移除 session_key collision check (#unsafe_keys 邏輯廢棄, 因 persona 本來唯一) (owner: claude-da-xiaojie)
- ✅ **T4** Migration: write _migrate_session_to_persona_locks.py one-shot — 掃 _identity_*.json 按內容 persona rename _persona_<X>.json + 防重跑 marker (owner: claude-da-xiaojie)
- ✅ **T5** Smoke + QA: morning solo 跑通 / 同 persona 重叮 reuse no-fork / 試模擬 cross-persona morning 跟今天 leak case 對比應該不再 affect 別 persona / migration script idempotent dry-run + apply (owner: claude-da-xiaojie)
