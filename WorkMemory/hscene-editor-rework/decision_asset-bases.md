---
id: decision_asset-bases
topic: hscene-editor-rework
title: 五大資產基底拍板（含退役名單）
type: decision
status: active
created_at: 2026-07-29
created_by: summit
links: []
related_docs: [Docs/Plan/HSceneEditorRework/Discussion_OpenQuestions.md, tavern:2026-07-28#9343, commit:b33d2add, commit:09ef2c9c]
---

**結論**（2026-07-27~28 Tim 逐題拍板, 全部「擴充既有資產」零新輪子）:

| 系統 | 基底（SSoT） | 退役/收斂 |
|---|---|---|
| 興奮等級 | `SatisfiedSetting`（門檻 list, 全空=隱含 Lv1, 第一級不入清單=結構性防呆） | `ExcitementLevelAsset` 已退役（資料已遷移） |
| 興奮值上限/衰減 | `HGameValueAsset`（m_MaxValue/m_DecreaseRate, 等級設定直接參照不另設） | — |
| 部位參數 | `HbodyAsset`（Default 基準±浮動 + 互動類型特例） | `PartParamAsset` 遷移後退役 |
| 互動方式 | `InteractionAsset`/`InteractionHSceneEntry` | `HControlAsset.GetAllIDs()` 下拉收斂回來 |
| 手勢門檻 | `ClickTypeAsset` 多組預設（每操作指定一組, 如 Drag_300ms; 未完成待 Plan D 補） | `ETouchCommand`/pipeline 全域門檻收斂 |
| 觸摸動作三欄 | `CheckInteractionSetting`（interaction/clickType/clickArea+extra） | — |

**可行動守則**: 動這些系統前先讀本拍板 — 別復活退役資產、別對「互動方式」開第二個下拉來源。完整推導與 16 題記錄見 related_docs。
