# ✅ Checklist — qa-battle-balance

_衍生 cache；最後更新 2026-05-12 11:46:23 UTC_

- ✅ **T01-csv-schema-bootstrap** 建 4 CSV files (qa_battle_results / card_power_log / item_equipment_log / state_effect_log) headers + gitignore + AgentCommands/QA_Battle_Logs/ dir (owner: claude-da-xiaojie)
- 🟢 **T02-cmd-battle-setup** Cmd_BattleSetup + Cmd_BattleConfig — 動態 build/patch RCG_BattlePresetData (player class / extra cards / items / equipments)
- ✅ **T03-record-result-cmd** Cmd_RecordBattleResult — 戰後自動 fire 寫 qa_battle_results.csv (turn_count / damage / outcome) (owner: claude-da-xiaojie)
- ✅ **T04-card-scorer** Cmd_ScoreCard — agent 評 1-5 分 + 寫 card_power_log.csv (situation_score 帶情境) (owner: claude-da-xiaojie)
- ✅ **T05-state-inspect** Cmd_BattleStateInspect — reflection 列所有 unit buff/debuff + 寫 state_effect_log.csv (owner: claude-da-xiaojie)
- 🟢 **T06-discord-log-rich** 擴 BattleAction broadcast body — 加 hand/mana/buff stack/damage breakdown 詳細欄位
- ✅ **T07-balance-aggregator** Cmd_BalanceReport — 跨 4 CSV aggregator → markdown report 在 _balance_reports/ (owner: claude-da-xiaojie)
- 🚧 **T08-matrix-sweep** 跑 5 char × 5 preset × 5 plays = 125 場 QA loop (or 第一輪 25 場 試 pipeline) (owner: antigravity-da-xiaojie)
- 🟢 **T09-final-report** 整合報告 + 平衡建議 → tavern post (category:work)
