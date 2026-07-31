---
id: decision_plan-d-prework
topic: hscene-editor-rework
title: Plan D 開工前拍板（D2 基底 ClothSetting + 四題工程消化 + 企劃三題）
type: decision
status: superseded
created_at: 2026-07-31
created_by: summit
links: [hscene-editor-rework/decision_plan-d-prework-final]
related_docs: [Docs/Plan/HSceneEditorRework/Plan_D_Interaction_Buttons_Operations.md, Docs/Plan/HSceneEditorRework/Discussion_ForDesigner.md, Assets/Scripts/HScenes/HSceneAssets/ClothSetting.cs, Assets/Scripts/UI/ClothPanel.cs:44, Assets/Scripts/UCL_Assets/ClickTypeAsset.cs:79]
---

**Plan D 開工前拍板**（Tim 2026-07-31 chat 逐題; 推導見 Plan_D 文件與本日 chat）:

| # | 判決 | 可行動守則 |
|---|---|---|
| D2 基底 | **擴充既有 ClothSetting / clothSettings, 不新建 ClothingButtonAsset** | nameKey/condition 沿用; 新增 m_PutOn/m_TakeOff (各帶 FlagChanges[]+可執行條件); 舊 flag 欄一次性遷移 →PutOn=-1/TakeOff=+1 (A1 先例); Hakoniwa 同構 (A2 先例) |
| D-1 | 「可新增動作類型」= 編輯器新增 InteractionAsset 資產 (UCL_Asset 自動編輯頁) | 特規欄位化: m_LeftPanelMode enum{一般/無左側/自動拆左右手}, 內建五型出廠值, 不綁死 enum |
| D-3 | 穿脫 flag 變化**沿用現行「加減」語意**(AlterAnimFlagValue ∓1) | FlagChanges = {AnimFlagRef, delta}; 不開 set 模式 (YAGNI) |
| D-4 | flag 值切換**當下即同步穿脫動畫**(現行機制涵蓋) | 不需過場演出設計; 日後要脫衣過程動畫再開 Plan F 題 |
| D-6 | 色塊歸屬 = **滑鼠按下瞬間**的區域判定 (沿用現行) | 整次按壓錨定起始色塊, 拖入他區不改判; 手勢互斥的「忽略」天然限定起始色塊 |

**企劃題縮至三題** (D-2 左右手共用/D-5 兩層條件/D-7 拖曳超時重試) → Discussion_ForDesigner「Plan D 開工題」, 全帶預設不擋工。

**工程順修項**: ClickTypeAsset.cs:79 反向 bug 實錘 — dragDistanceMax 判斷寫成 `dragDis < max`(上限寫成下限); 且四個 min/max 欄位 XML 註解 min/max 對調。列 D4 施工項。
