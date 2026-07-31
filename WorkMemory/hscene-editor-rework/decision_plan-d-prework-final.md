---
id: decision_plan-d-prework-final
topic: hscene-editor-rework
title: Plan D 開工前拍板 — 全數定案（八題: Tim 五題 + 熊汁三題, 無 pending 可開工）
type: decision
status: active
created_at: 2026-07-31
created_by: summit
links: [hscene-editor-rework/decision_plan-d-prework]
related_docs: [Docs/Plan/HSceneEditorRework/Plan_D_Interaction_Buttons_Operations.md, Docs/Plan/HSceneEditorRework/Discussion_ForDesigner.md, Assets/Scripts/HScenes/HSceneAssets/ClothSetting.cs, Assets/Scripts/UI/ClothPanel.cs:44, Assets/Scripts/UCL_Assets/ClickTypeAsset.cs:79]
---

**Plan D 開工前拍板 — 全數定案**（Tim 2026-07-31 chat 逐題 + 熊汁 2026-07-31 18:59 Discord 回覆三題; 詳版 Plan_D / Discussion_ForDesigner）:

| # | 判決 | 可行動守則 |
|---|---|---|
| D2 基底 | **擴充既有 ClothSetting / clothSettings, 不新建資產**（Tim） | nameKey/condition 沿用; 新增 m_PutOn/m_TakeOff (各帶 FlagChanges[]+可執行條件); 舊 flag 欄一次性遷移 →PutOn=-1/TakeOff=+1 (A1 先例); Hakoniwa 同構 (A2 先例); CanExecute API 供 3.8 共用 |
| D-1 | 「可新增動作類型」= 編輯器新增 InteractionAsset 資產（Tim） | 特規欄位化: m_LeftPanelMode enum{一般/無左側/自動拆左右手}, 內建五型出廠值 |
| D-2 | 左右手**可各自掛不同動畫**（熊汁） | 「自動拆左右手」派生的兩個子條目各自帶完整動畫設定, 非僅 ID 派生 |
| D-3 | 穿脫 flag 變化沿用現行「加減」語意（Tim） | FlagChanges = {AnimFlagRef, delta}; 不開 set 模式 (YAGNI) |
| D-4 | flag 值切換當下即同步穿脫動畫（Tim） | 不需過場演出; 日後要脫衣過程動畫再開 Plan F 題 |
| D-5 | 兩層條件並存, **空條件=直接顯示/可按**（熊汁） | condition=顯示(隱藏) / m_Condition=可執行(壓灰); 空=通過, ConditionGroup 既有語意 |
| D-6 | 色塊歸屬 = 滑鼠**按下瞬間**判定（Tim） | 整次按壓錨定起始色塊, 拖入他區不改判 |
| D-7 | 拖曳超時後**重置計時可重試 (b)**（熊汁） | 引擎做拖曳狀態重置, 起點重錨於重置當下座標; 注意與「任一手勢觸發→忽略其餘」互動: 觸發過效果仍全域忽略 |

**工程順修項**: ClickTypeAsset.cs:79 反向 bug — dragDistanceMax 判斷寫成 `dragDis < max`; 四個 min/max 欄位 XML 註解對調。列 D4 施工項。

**Plan D 無 pending 企劃題, 可開工。** 補充素材: Tim 提供重構文件網路share `\192.168.14.22\Yellow Touch\重構文件`（2026-07-31 18:55 酒館）。
