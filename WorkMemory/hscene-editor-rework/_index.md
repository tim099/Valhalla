# 工作記憶索引 — hscene-editor-rework

> 機械生成（work_memory.py index）— 手改會被覆寫。事實源 = 各 fragment 檔。

## decision
- **decision_asset-bases** — 五大資產基底拍板（含退役名單）
- **decision_c1-scene-flag-correction** — C1 需求更正：場景層 Flag 連動（valueAnims 保留 / P4 pending / 文件≠需求教訓）
- **decision_impl-verdicts-a-b** — A/B 施工級判決濃縮（十題+QA修正+PopupGrouped三題）  ↔ hscene-editor-rework/knowhow_a-b-deliverables
- **decision_plan-c-designer-b** — Plan C 企劃拍板六題 + C-1 結案（分色圖角色分類修正）  ↔ hscene-editor-rework/decision_plan-c-designer
- **decision_plan-c-prework** — Plan C 開工前五題判決（雙軌並存/0-index/list[0]/CheckArea 源頭）  ↔ hscene-editor-rework/knowhow_a-b-deliverables, hscene-editor-rework/decision_spine-group-model
- **decision_plan-d-prework-final** — Plan D 開工前拍板 — 全數定案（八題: Tim 五題 + 熊汁三題, 無 pending 可開工）  ↔ hscene-editor-rework/decision_plan-d-prework
- **decision_spine-group-model** — Spine 分組模型與 SpineAnimRef 拍板（含 P3 pending）
- **decision_plan-c-designer** — Plan C 企劃拍板六題 + 分色圖 69 張實測（C-1 因果更正） ~~[superseded]~~  ↔ hscene-editor-rework/decision_plan-c-prework, hscene-editor-rework/decision_plan-c-designer-b
- **decision_plan-d-prework** — Plan D 開工前拍板（D2 基底 ClothSetting + 四題工程消化 + 企劃三題） ~~[superseded]~~  ↔ hscene-editor-rework/decision_plan-d-prework-final

## knowhow
- **knowhow_a-b-deliverables** — A/B 交付物使用說明（SpineAnimRef/LockService/Trigger/FolderFilter 下一棒怎麼用）  ↔ hscene-editor-rework/decision_impl-verdicts-a-b
- **knowhow_existing-infra** — 既有基建直接用清單（條件/事件/階段停播/分組下拉）  ↔ ucl-editor-pages/knowhow_page-skeleton

## pitfall
- **pitfall_known-traps** — 已知坑清單（WIP 所有權/Hakoniwa enum/輸入源頭 guard/文件漂移）

## state
- **state_progress-2026-08-03** — 施工進度 2026-08-03（C 驗收 3/4 + C1 需求更正 P4 + 文件≠需求鐵則）  ↔ hscene-editor-rework/state_progress-2026-07-31
- **state_progress-2026-07-29** — 施工進度快照 2026-07-29（A完工/B施工中） ~~[superseded]~~  ↔ hscene-editor-rework/state_progress-2026-07-29b
- **state_progress-2026-07-29b** — 施工進度快照 2026-07-29b（A/B/PopupGrouped 完工, 下一棒 C） ~~[superseded]~~  ↔ hscene-editor-rework/state_progress-2026-07-29c
- **state_progress-2026-07-29c** — 施工進度快照 2026-07-29c（C 資料層完工, 未 commit/未實測） ~~[superseded]~~  ↔ hscene-editor-rework/state_progress-2026-07-29b, hscene-editor-rework/state_progress-2026-07-31
- **state_progress-2026-07-31** — 施工進度快照 2026-07-31（C 已 commit aaa24cee, 剩 Editor 實機驗收） ~~[superseded]~~  ↔ hscene-editor-rework/state_progress-2026-07-29c, hscene-editor-rework/state_progress-2026-08-03

## pointer
- **pointer_docs-map** — 文件地圖（哪份是權威）
