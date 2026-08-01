# 工作記憶索引 — agentcmd-schema-codegen

> 機械生成（work_memory.py index）— 手改會被覆寫。事實源 = 各 fragment 檔。

## decision
- **decision_contract-design-decisions** — schema 契約八條拍板（fail-open / hash 非 mtime / 手動為主 / JSON / 不收 optional）

## pitfall
- **pitfall_verify-traps** — 驗證三坑：compile 假綠 / selftest 雙模組 / 用 submit 驗預檢會產生真副作用

## state
- **state_state-2026-08-01-all-shipped** — S0–S5 全部 ship 並 push；三個待修已修完；alias 有序陣列等四項仍開放  ↔ agentcmd-schema-codegen/state_state-2026-07-29-shipped
- **state_state-2026-07-29-shipped** — S0–S5 已 commit（449031d）；待修：0.9s 回歸 / 集合定義不等價 / alias key 順序 ~~[superseded]~~  ↔ runcmd-modular-split, runcmd-modular-split/state_state-2026-07-29-one-of-six, agentcmd-schema-codegen/state_state-2026-08-01-all-shipped

## pointer
- **pointer_doc-map** — 文件地圖：設計/SOP/契約兩側/34 op 宣告/討論出處

