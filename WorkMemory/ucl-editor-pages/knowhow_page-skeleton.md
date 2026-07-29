---
id: knowhow_page-skeleton
topic: ucl-editor-pages
title: UCL_CommonEditorPage 頁面骨架與效能慣例
type: knowhow
status: active
created_at: 2026-07-29
created_by: summit
links: [hscene-editor-rework/knowhow_existing-infra]
related_docs: [Assets/Plugins/UCL_Core/UCL_Core_Scripts/EditorCore/UCL_EditorMenuPages/UCL_BankAdminPage.cs]
---

**頁面骨架慣例**（從 ScreenStreamPage / BankAdminPage / ProcessAdminPage / CustomCommandAdminPage 歸納）:

- 繼承 `UCL_CommonEditorPage`, `ShowInPageMenu => true` 自動進 page menu; `Create()` 走 `UCL_EditorPage.Create<T>()`
- **開頁一次判斷+快取**: 狀態掃描只在開頁/Refresh/操作後做（`m_StatusDirty` 模式）, 絕不每幀掃磁碟 — IMGUI 每 repaint 都跑 ContentOnGUI, 每幀 IO = 卡頓（BankAdminPage 的餘額快取 P0 修是血證）
- 沒有 OnEnter virtual — lazy init 用 first-OnGUI flag（ScreenStreamPage `EnsureInitialReload` 模式）
- 不可巢狀 BeginScrollView（外層已包, Unity 2021 IMGUI 會 InvalidCastException）
- 開文件走 `UCL_MarkdownViewerPage.Create(rel, abs)`（Editor 內嵌渲染, Back 返回）; 文件綁定用類別 `[HelpURL]` attribute
- 下拉選單: `UCL_GUILayout.Popup(idx, options, UCL_ObjectDictionary, key)`; **前綴自動分組摺疊用 `PopupGrouped`**（分隔符參數化, UCL_Core@LY 71b9f7f）
- 危險操作二段確認: 第一次點=arm + 5s 倒數, 第二次才執行（錄影 toggle/kill process 同款）
- 內部管理頁 UI 字串硬編 zh-Hant（不走 CodeLocalize）; 對外功能頁走 `UCL_CodeLocalize.Get`

**可行動守則**: 開新管理頁先抄 `UCL_BankAdminPage` 骨架; 效能疑慮先查有沒有每幀 IO。
