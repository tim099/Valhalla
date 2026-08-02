---
id: knowhow_im-gui-patterns
topic: ucl-editor-pages
title: ControlPanel 與 UCL_GUILayout 常用模式
type: knowhow
status: active
created_at: 2026-08-02
created_by: meadow
links: []
related_docs: [Assets/Plugins/UCL_Core/UCL_Core_Scripts/EditorCore/UCL_EditorMenuPages/UCL_BartenderAdminPage.cs, Assets/Plugins/UCL_Core/UCL_Core_Scripts/EditorCore/UCL_EditorMenuPages/UCL_ControlPanelPage.cs, Assets/Plugins/UCL_Core/UCL_Core_Scripts/EditorCore/UCL_EditorMenuPages/UCL_ChatTavernAdminPage.cs]
---

ControlPanel section 使用 VerticalScope(box) + UCL_GUILayout.Toggle(m_FoldDic,key,21) header，關鍵按鈕放 fold 外。狀態切換只在值變動時寫入；列表刪除先記 deleteId、foreach 後再 RemoveAll；Reload 走既有 IO layer。常用樣式是 UCL_GUIStyle.LabelStyle/ButtonStyle/GetButtonStyle(color)，checkbox 用 UCL_GUILayout.CheckBox。
