---
id: pointer_page-contract
topic: ucl-editor-pages
title: Editor Page 與文件契約
type: pointer
status: active
created_at: 2026-08-02
created_by: meadow
links: []
related_docs: [Assets/Plugins/UCL_Core/Docs~/zh-Hant/Workflows/Create_EditorPage_Workflow.md, Assets/Plugins/UCL_Core/Docs~/zh-Hant/UCL_EditorPage/UCL_BartenderAdminPage.md, Assets/Plugins/UCL_Core/UCL_Core_Scripts/EditorCore/UCL_EditorMenuPages/UCL_ControlPanelPage.cs]
---

新頁用 UCL_CommonEditorPage + static Create() 工廠；HelpURL 指向 Docs~/{lang}/UCL_EditorPage/<Class>.md。新增公開頁要同時建立含 frontmatter/related 的文件，並回填 Docs~/zh-Hant/index.md。控制台入口只導流，不在入口頁靜默改設定。
