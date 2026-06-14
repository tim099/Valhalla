---
task_id: T01-migrate
title: 酒館券 schema v1 → v2 migration (broadcast rule)
created_at: 2026-05-13T07:54:48Z
---

**目標**: 執行 Q11 拍板的酒館券 schema v1→v2 migration

**規則** (Tim 2026-05-13 拍板):
- 每 persona 初始化 = 該 actor 帳戶當前 voucher total
- broadcast 不 split (eg. actor 36 → 每 persona 36)
- Antigravity 0 → 每 persona 0
- 通膨可接受 (一次性)

**Deliverable**:
1. `AgentCommands/Tools/migrate_voucher_v1_to_v2.py` (NEW): 自動化 migration 腳本
2. `agent_bonus_quota.v1.bak.json` (backup): 原檔 snapshot
3. `agent_bonus_quota.json` (new v2 schema): per-actor × per-persona 兩層
4. 跑完驗證 stats + 確認無誤

**Steps**:
1. Write migrate script
2. Run migrate (backup + transform + write)
3. Verify: print per-actor × per-persona total_remaining stats
4. Compare expected: claude-da-xiaojie 36 → 5 personas × 36 = 180 / antigravity 0 → 4 × 0 = 0
5. If pass → task_done + commit migration files
6. If fail → revert from backup + task_block
