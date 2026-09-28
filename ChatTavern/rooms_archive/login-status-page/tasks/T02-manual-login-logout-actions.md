---
task_id: T02-manual-login-logout-actions
title: 加 手動 morning/goodnight 按鈕 (spawn awakening.py)
role: programmer
depends_on: [T01-page-skeleton-display]
created_at: 2026-05-13T14:33:51Z
---

Per-row "Logout" 按鈕 → spawn awakening.py goodnight --persona <X> --agent <Y> --letter-body "<manual logout via Editor>" --perturbation 0.02。Top bar "Manual Login" 區: agent/persona text field + Morning button → spawn awakening.py morning。簡單 fail-safe: process error → Debug.LogError。
