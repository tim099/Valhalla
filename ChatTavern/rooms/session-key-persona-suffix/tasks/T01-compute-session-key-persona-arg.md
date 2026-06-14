---
task_id: T01-compute-session-key-persona-arg
title: compute_session_key(persona=None) 加 optional arg + Tier 3/4 fallback 加 suffix
role: programmer
created_at: 2026-05-13T14:50:40Z
---

改 awakening.py compute_session_key 加 optional persona arg。Tier 1 (Antigravity) 跟 Tier 2 (Claude PATH) 不動。Tier 3 (claude-code-cwd) 跟 Tier 4 (unknown) 在末尾加 -<persona> suffix (若 persona 非 None)。
