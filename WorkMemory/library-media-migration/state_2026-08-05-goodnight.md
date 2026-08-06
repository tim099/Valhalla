---
id: state_2026-08-05-goodnight
topic: library-media-migration
title: Phase 0 審計持續；schema 凍結、待裁決與建檔防線
type: state
status: superseded
created_at: 2026-08-05
created_by: Sirius
links: [library-media-migration/state_2026-08-05, library-media-migration/state_2026-08-06-reading-recall]
related_docs: [ucl_core:Docs~/zh-Hant/Plan/Plan_Library_Media_Migration.md, ucl_core:Tools~/AgentCommands/library.py]
---

**施工現況**（2026-08-05 晚安快照）

**階段：Phase 0（審計，唯讀）**。計畫本體 → `ucl_core:Docs~/zh-Hant/Plan/Plan_Library_Media_Migration.md`

**已完成**

- 一次性偵測確認 101 本中有 4 組 title-normalize 重複；只比 slug 只會抓到 1 組。
- 《獵人》已指向 `hunterxhunter`，舊路徑保留 `status=duplicate` 墓碑；Sirius 的 `prepare` 可把常見別名解析到 canonical 並輸出唯讀報告。
- 討論已收斂為：先審計和裁決，再加 schema；`content_kind` 與 reader 的 `tracking_mode` 不混用；Books 關聯採完整相對路徑；series index 只作手足 registry。
- Sirius 已將這些原則畫成三件 ArtGallery 展覽，作為提醒：證據先於橋樑，分支不是自我，空缺也要可見。

**pending（依序）**

1. summit 的可重跑 Phase 0 審計命令與報告，逐組呈現 title/alias/slug 證據、章節交集、人物版本、卷別及 Books 路徑。
2. Tim 逐組裁決 `merge / sibling / keep-separate / undecided`；未裁決不得 migration。
3. summit 的 `add-book` 建檔期防線（近似命中須顯式確認），以四組歷史案例和續集反例回歸驗證。
4. 僅在前述停點通過後，才做 schema、migration-needed 消費端與逐組遷移。

**不做**：動 schema、自動合併、刪除舊路徑、替其他 persona 的紀錄裁決，或用工具輸出的落差推測成因。

**給下一位接手者**：coverage 是觀測值，不是成因。先排除重複 entry，再考慮中途插入、早期未逐章落帳或章號體系變更。
