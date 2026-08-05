# 工作記憶索引 — compile-verification

> 機械生成（work_memory.py index）— 手改會被覆寫。事實源 = 各 fragment 檔。

## decision
- **decision_completion-and-freshness** — 完成條件 = mtime 推進 + in_progress=false；新鮮度基準吃 git 且只算一次  ↔ bartender-remote-notify/decision_read-ack

## knowhow
- **knowhow_three-way-reconcile** — 改完 .cs 的驗收：recompile → check_compile 交叉對帳 → 停跳台帳當第三方物證

## pitfall
- **pitfall_three-layer-false-green** — 三層各有一隻假綠燈：時間戳對而數字假 / 快照早於改動 / 停跳不等於編譯  ↔ unitask-editor-async/knowhow_unitask-patterns, library-media-migration/pitfall_slug-vs-title-and-position-vs-coverage

## state
- **state_2026-08-05-eod** — 全案完工並實測；LY bump 已清，今日無遺留  ↔ compile-verification/state_2026-08-05
- **state_2026-08-05** — 新鮮度守衛 + 停跳台帳 + recompile 完成條件 全部落地並實測；LY parent bump 待 Tim ~~[superseded]~~  ↔ compile-verification/state_2026-08-05-eod

## pointer
- **pointer_docs-map** — 文件與 code 位置地圖（三層工具 + 三個產出物）
