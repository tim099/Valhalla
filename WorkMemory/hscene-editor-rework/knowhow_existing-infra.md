---
id: knowhow_existing-infra
topic: hscene-editor-rework
title: 既有基建直接用清單（條件/事件/階段停播/分組下拉）
type: knowhow
status: active
created_at: 2026-07-29
created_by: summit
links: [ucl-editor-pages/knowhow_page-skeleton]
related_docs: [Assets/Scripts/Conditions/ConditionGroup.cs, Assets/Scripts/IAsyncEvents/Settings/HAnimSetting.cs, Assets/Scripts/IAsyncEvents/Settings/HAnimSetting.cs:476]
---

**既有基建盤點**（探勘 2026-07-27, 施工前必知 — 這些都「直接用」不重造）:

- **條件**: `Assets/Scripts/Conditions/` — `ConditionGroup` 內建 AND/OR 切換 + inverse(NOT) + 巢狀 group, 表達力完整。企劃所有「條件設定/顯示條件/可執行條件」欄位直接掛它
- **事件**: `Assets/Scripts/IAsyncEvents/` — IAsyncEvent 20+ 具體事件（PlayAVG/SetAnimFlag/SetGameValue/WaitForSeconds/EventGroup…）+ AreaEvent/TimmingEvent/OnUpdateEvent 容器
- **觸摸階段停播已實作**: `HAnimSetting.ParameterSetting.m_ClickPlayTime`（=「操作後視為觸摸中的時間」, 預設 0.1f）+ `m_StopClickPlayEvent`（Spine event=換圖點, 非自動模式播到即停）→ 企劃「動畫階段數」以 event 邊界為基底補, 不另造階段系統
- **下拉分組 UI**: `UCL_GUILayout.PopupGrouped`（UCL_Core, 按 string 前綴自動摺疊, 分隔符參數化）已接 UCL_AssetEntry ID 下拉
- **兩段式 drawer 前例**: `UCL_AddressableData` 的 path→key（第二段選項吃第一段值）

**可行動守則**: 寫新欄位前先對照本清單 — 撞到「我需要條件/事件/階段/分組下拉」時, 答案都已存在。
