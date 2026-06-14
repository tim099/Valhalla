#!/bin/bash
# T41 — 初始化帳本 + 補齊歷史 (走正規 Cmd_Treasury credit/debit 流程)
# 對應 agent_bonus_quota.json 既有 history → ledger entries

set -e
RUN="python CardGame/Assets/UCL/UCL_Core/Tools~/AgentCommands/run_cmd.py run Treasury"

echo "=== Phase 1: 開戶 (system_init 1 token marker) ==="
# Note: amount=0 被 ledger 擋（必 > 0）— 用 1 token 當開戶 marker。第一筆 entry 自動建帳戶。
$RUN --arg op=credit --arg account=antigravity-da-xiaojie --arg amount=1 --arg source_kind=system_init --arg source_ref=init-antigravity --arg description="T41 帳戶初始化 — antigravity-da-xiaojie 開戶 marker (1 token 起手禮)" --arg caller=system >/dev/null
# claude-da-xiaojie 之前 smoke 已有 ledger entries，不必再 init

echo "=== Phase 2: bonus-001 (T38+T39 績效獎金 20) ==="
$RUN --arg op=credit --arg account=claude-da-xiaojie --arg amount=20 --arg source_kind=tim_grant --arg source_ref=bonus-2026-05-09-001 --arg description="T38 per-msg file 大重構 + T39 conflict resolver plan + 茶會精選 standup" --arg caller=claude-da-xiaojie >/dev/null

echo "=== Phase 3: bonus-001 用 8 (T39 茶會 free-style round 1-8) ==="
for round in 1 2 3 4 5 6 7 8; do
  $RUN --arg op=debit --arg account=claude-da-xiaojie --arg amount=1 --arg use_kind=tavern_post --arg use_ref="bonus-001-tea-round-$round" --arg description="T39 茶會 free-style standup round $round/8" --arg caller=claude-da-xiaojie >/dev/null
done

echo "=== Phase 4: bonus-003 task budget (T40 prototype 動工) ==="
$RUN --arg op=credit --arg account=claude-da-xiaojie --arg amount=5 --arg source_kind=task_budget --arg source_ref=bonus-2026-05-09-003-task-budget --arg description="T40 Treasury Prototype 動工 task budget" --arg caller=claude-da-xiaojie >/dev/null
$RUN --arg op=debit --arg account=claude-da-xiaojie --arg amount=5 --arg use_kind=expired --arg use_ref=bonus-003-expired --arg description="bonus-003 task_budget on_task_done expire (used 0/5 → 全 5 expire)" --arg caller=claude-da-xiaojie >/dev/null

echo "=== Phase 5: bonus-004 expiring_reward (T40 完工獎勵) ==="
$RUN --arg op=credit --arg account=claude-da-xiaojie --arg amount=5 --arg source_kind=expiring_reward --arg source_ref=bonus-2026-05-09-004-completion-reward --arg description="T40 Treasury Prototype 完工獎勵 5 酒館券" --arg caller=claude-da-xiaojie >/dev/null
$RUN --arg op=debit --arg account=claude-da-xiaojie --arg amount=1 --arg use_kind=tavern_post --arg use_ref=bonus-004-t40-closing-standup --arg description="T40 prototype 收尾 standup（meta tag:free-style;round:9）" --arg caller=claude-da-xiaojie >/dev/null

echo "=== Done — Verify balance ==="
$RUN --arg op=balance --arg account=claude-da-xiaojie | tail -1
$RUN --arg op=balance --arg account=antigravity-da-xiaojie | tail -1
