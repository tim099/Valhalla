---
id: decision_spine-group-model
topic: hscene-editor-rework
title: Spine 分組模型與 SpineAnimRef 拍板（含 P3 pending）
type: decision
status: active
created_at: 2026-07-29
created_by: summit
links: []
related_docs: [Docs/Plan/HSceneEditorRework/Plan_B_AssetImport_SpineGroups.md, Docs/Plan/HSceneEditorRework/Discussion_Pending.md, tavern:2026-07-28#9355]
---

**結論**（Q6/Q9 + Plan B 五題判決, 2026-07-28）:

- Spine 分組**基於 `SkeletonGraphicSetting` 擴充** `m_AnimGroups[]`, 不新增獨立 asset; 多 Spine 由 `HSceneAsset.extraSkeletons` 承載（主骨架早已摺進 extraSkeletons[0], 同構）
- **分組隸屬單一 skeleton**, 不跨檔案混組; 選單語意 = skeleton → 分組 → 動畫
- **主/副視窗不另標記** — 歸屬隨動畫所屬 skeleton/分組, `SpineAnimRef` 不加 targetWindow 欄
- `SpineAnimRef` schema: anim 是 SSoT、group 純過濾、skeletonID 情境可隱含就不序列化、失效標紅不靜默
- fallback 語意: 該 skeleton「無任何分組」→ 全列（過渡態）;「有分組」→ 只列已分組
- 音效導入走輕量版（Utage key 下拉 + 資料夾篩選）, 音效 asset 體系除非 E4/F3 撞到才開 plan
- ⚠「一鍵自動分組」**不實作** → 轉 Pending P3: 改由 Odin 式下拉自動分組（`UCL_GUILayout.PopupGrouped` 已落地 UCL_Core@LY 71b9f7f, 分隔符可參數化）; 動畫下拉接線與手動分組優先序待 Tim 定案

**可行動守則**: 做 C/E/F 的 Spine 欄位一律用 `SpineAnimRef` 型別, 不自造兩段式選單; 分組相關 UI 動工前先看 Pending P3 是否已定案。
