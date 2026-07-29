---
id: decision_plan-c-designer
topic: hscene-editor-rework
title: Plan C 企劃拍板六題 + 分色圖 69 張實測（C-1 因果更正）
type: decision
status: superseded
created_at: 2026-07-29
created_by: summit
links: [hscene-editor-rework/decision_plan-c-prework, hscene-editor-rework/decision_plan-c-designer-b]
related_docs: [Docs/Plan/HSceneEditorRework/Discussion_ForDesigner.md, tavern:2026-07-29#9500, Assets/Scripts/UCL_Assets/ClickAreaAsset.cs:270, Assets/Scripts/UCL_Assets/ClickAreaAsset.cs:122]
---

**Plan C 企劃拍板六題 + 分色圖實測**（熊汁 2026-07-29 11:12 回覆 summit 11:0x 提問; 白話題目與原文見 Discussion_ForDesigner「Plan C 開工題」章節）:

| # | 判決 | 可行動守則 |
|---|---|---|
| C-2 | 手動命名的小色塊**要留**（辨識用）— 人工命名優先於自動面積門檻 | RefreshAreaConfigs 的 AutoGenAsset 免 m_MinAreaPixelSize 過濾語意**沿用不動**; UI 加提示文字說明 |
| C-3 | 同一 Flag 值掛到同一骨架的兩個動畫 = **視為 BUG**（理論上不該出現互蓋） | 編輯器標紅提示, **不自行猜優先序**、不做後蓋前 |
| C-4 | Flag 初始值**每個 Flag 各自設**; 介面 = Flag 名手動輸入 → 逐項新增, 每項各掛一個動畫下拉, **每一串都從 1 開始** | 顯示層 1-based（第 1 項顯示 1）; 儲存層維持 0-index（C-Q2 判決）, 兩者只差顯示 +1 |
| C-5 | 副視窗關閉期間動畫照跑, 重開**接續不重播** | 顯示層用 CanvasGroup/alpha 或攝影機層, **不可 SetActive(false)**（會停動畫更新） |
| C-6 | 同色跨不同張圖片資料 = **同一觸摸位置**, 共用命名 | 掃描取所有圖的色碼**聯集**供命名（現行 RefreshAreaConfigs 即此語意, 不動） |
| C-7 | 重疊色塊由**編輯器排列順序**決定, 排上面的贏, **系統不自動比色塊大小** | 現行 AreaService.CheckArea 已 first-hit 早退 = 此語意; C 只補排序 UI + 驗收項 |

**C-1（分色圖素材規範）— 實測後因果更正, 仍待熊汁回 (a)/(b)**:
- 專案 69 張分色圖全掃: **47 張完全乾淨**（純色硬邊/零雜色/零半透明）; 22 張有 AA 殘留但佔比 0.001%~0.18%; 只有 `Scene1.png`（1845 色, 0.97%）與 `Version3_Scene1/view.png`（1133 色）明顯。
- **主因不在素材**: 即使硬邊素材, 運行期 `ClickAreaAsset.CheckArea` 用 `GetPixelBilinear` 取色仍在邊界自行內插混色 → 精確色碼字典查無此 key。
- **修法**: 程式端改 `GetPixel` 點取樣（根治, 工程端自理, C 施工項）; 素材端只需新圖維持關反鋸齒, 既有檔不重出。容差比對降為 plan B（(b) 才走, 代價=相鄰色塊邊界歸屬模糊）。

**教訓（可轉 lessons-log）**: 要求他人重工前先自己數過 — 原本以為要美術全面重出圖, 實測後發現 68% 素材本來就合規、真兇是自家取樣方式。
