---
task_id: T03-verify-fallback-no-collision
title: Verify Tim 場景: Tier 3 fallback 兩 persona 不撞 + Tier 2 命中時不影響
role: qa
depends_on: [T02-callers-pass-persona]
created_at: 2026-05-13T14:50:42Z
---

測試: (a) Tier 2 命中 (CLAUDECODE env + PATH 有 conv) 加 persona 不變 (b) Tier 3 fallback (CLAUDECODE 沒 PATH) 兩 persona 算出不同 key (c) Tier 4 (unknown) 同 (d) 既有 Tier 2 collision 場景仍偵測到 (cwd-hash 撞但 conv_uuid 同的 edge case)
