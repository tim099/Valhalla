---
id: knowhow_collapsible-sections-defaults
topic: ucl-editor-pages
title: 管理頁區塊折疊的預設與標頭責任
type: knowhow
status: active
created_at: 2026-08-02
created_by: meadow
links: []
related_docs: [Assets/Plugins/UCL_Core/UCL_Core_Scripts/EditorCore/UCL_EditorMenuPages/UCL_BartenderAdminPage.cs, Assets/Plugins/UCL_Core/UCL_Core_Scripts/EditorCore/UCL_EditorMenuPages/UCL_ControlPanelPage.cs, Assets/Plugins/UCL_Core/Docs~/zh-Hant/Workflows/Create_EditorPage_Workflow.md]
---

長列表型管理頁以專用 UCL_ObjectDictionary 搭配 UCL_GUILayout.Toggle 畫各區塊 header，首次值一律 iDefaultValue:false。仍需高頻使用的總開關、立即執行與重新載入留在 header；說明、列表及新增刪除內容在 if (!show) return 後才繪製，避免首頁冗長且不犧牲操作性。
