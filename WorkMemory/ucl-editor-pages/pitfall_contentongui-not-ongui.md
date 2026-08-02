---
id: pitfall_contentongui-not-ongui
topic: ucl-editor-pages
title: 自訂 ContentOnGUI，不覆寫 OnGUI
type: pitfall
status: active
created_at: 2026-08-02
created_by: meadow
links: []
related_docs: [Assets/Plugins/UCL_Core/UCL_Core_Scripts/EditorCore/UCL_EditorMenuPages/UCL_EditorPage.cs, Assets/Plugins/UCL_Core/UCL_Core_Scripts/EditorCore/UCL_EditorMenuPages/UCL_CommonEditorPage.cs, Assets/Plugins/UCL_Core/UCL_Core_Scripts/EditorCore/UCL_EditorMenuPages/UCL_BartenderAdminPage.cs, Assets/Plugins/UCL_Core/Docs~/zh-Hant/Workflows/Create_EditorPage_Workflow.md]
---

UCL_EditorPage.OnGUI 負責 TopBar 與全頁 GUILayout.ScrollViewScope。子頁若直接覆寫 OnGUI，會繞過 Back/Close/HelpURL 及全頁捲動；頁面主體應覆寫 ContentOnGUI，標頭擴充則覆寫 TopBarButtons 並先呼叫 base。
