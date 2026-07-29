---
id: decision_plan-c-designer-b
topic: hscene-editor-rework
title: Plan C 企劃拍板六題 + C-1 結案（分色圖角色分類修正）
type: decision
status: active
created_at: 2026-07-29
created_by: summit
links: [hscene-editor-rework/decision_plan-c-designer]
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

---

**C-1 結案（取代先前的「請美術重出圖」版本）** — Tim 2026-07-29 指出 Scene1.png / view.png 是**參照底圖**（場景畫面, 墊在分色圖下供對齊）, 非分色圖。重新依 39 個 ClickAreaAsset 的欄位角色分類後：

| 角色 | 數量 | 說明 |
|---|---|---|
| 參照底圖（`Texture` 欄） | 3（ClickAreas_Scene1 / Version2_Scene2_Scene2 / Version3_Scene1_view） | **不參與取色判定**, 彩色照片天經地義; 先前「1845 色」誤報全在此 |
| 真分色圖（`AreaTexture` / ConditionalAreas） | 59 | 40 張完全乾淨 / 19 張有 AA 殘留, 最大佔比 0.176% |

**關鍵事實**: 59 張分色圖 **58 張 FilterMode 已設 Point**（唯一 Bilinear 是全透明的 ClickAreas_Null, 無色塊無影響）。素材端「分色圖不做內插」的觀念早已落實; **沒跟上的是程式** — `ClickAreaAsset.CheckArea` 用 `GetPixelBilinear`（CPU 自行內插, **不理會素材的 FilterMode**）。

**定案**:
- 素材端**零動作** — 底圖維持、19 張殘留檔不重出; 僅保留軟性習慣（新分色圖關反鋸齒存 PNG）
- 工程端 `GetPixelBilinear` → `GetPixel` 點取樣, 與素材既有 Point 設定對齊 — 併入 Plan C 施工項, **不再是需求題**
- 容差比對方案作廢（不需要）

**額外發現**: `ClickAreas_Null`（Transparent.png, 全透明）**已存在且已被當條件分色圖使用** — Plan C「內建 null 圖片資料（該分組完全無法互動）」半套已在專案內跑, **沿用不另造**。

**教訓（可轉 lessons-log）**: 稽核前先確認「掃的東西是不是判定真正吃的東西」。我把整個 ClickAreas 資料夾無差別掃描, 沒依欄位角色分類, 於是把參照底圖當成不合規的分色圖點名, 差點要求美術重工。**外觀 FAIL ≠ 真的 FAIL 的第 N 次現形** — 這次靠 Tim 一句領域知識救回。
