---
id: pointer_docs-map
topic: hscene-editor-rework
title: 文件地圖（哪份是權威）
type: pointer
status: active
created_at: 2026-07-29
created_by: summit
links: []
related_docs: [Docs/Plan/HSceneEditorRework/README.md]
---

**哪份文件是什麼的權威**（別讀錯層）:

| 要什麼 | 讀哪份 |
|---|---|
| 全案索引/依賴圖/施工順序 | `Docs/Plan/HSceneEditorRework/README.md` |
| 各 plan 施工圖（欄位/驗收清單） | `Plan_A_Core_Params.md` ~ `Plan_F_Face_PassiveEffects_Events.md` |
| **需求拍板記錄（16 題, 含 code 出處）** | `Discussion_OpenQuestions.md` ← 需求爭議時的最終權威 |
| 給企劃的白話確認（全結案） | `Discussion_ForDesigner.md` |
| 未定案規格（棒棒/物件槽/自動分組） | `Discussion_Pending.md` ← 企劃會直接在檔內回覆 |
| 原始企劃 | `C:/Users/crespirit/Downloads/編輯器重構.txt`（V1.1; 注意已知漂移見 pitfall_known-traps 第5條） |

**可行動守則**: 接手任何 plan 先讀 README → 對應 Plan_X → 本主題 decision/pitfall fragments; 需求疑義查 OpenQuestions 而不是原始企劃。
