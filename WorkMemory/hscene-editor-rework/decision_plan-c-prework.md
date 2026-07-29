---
id: decision_plan-c-prework
topic: hscene-editor-rework
title: Plan C 開工前五題判決（雙軌並存/0-index/list[0]/CheckArea 源頭）
type: decision
status: active
created_at: 2026-07-29
created_by: summit
links: [hscene-editor-rework/knowhow_a-b-deliverables, hscene-editor-rework/decision_spine-group-model]
related_docs: [Docs/Plan/HSceneEditorRework/Plan_C_SceneAnimFlags_ClickAreas.md, Docs/Plan/HSceneEditorRework/Discussion_ForDesigner.md, tavern:2026-07-29#9495, tavern:2026-07-29#9496, Assets/Scripts/UCL_Assets/SkeletonGraphicAsset.cs:332, Assets/Scripts/UCL_Assets/ClickAreaAsset.cs:270, Assets/Scripts/HScenes/HSceneService/AreaService.cs:105]
---

**Plan C 開工前五題判決**（crest-001 前一棒回覆 2026-07-29 10:54, summit 提問 10:51; 推導在酒館 ref, 這裡只留結論+可行動守則）:

| # | 題目 | 判決 | 可行動守則 |
|---|---|---|---|
| C-Q1 | C1 flag→動畫模型與現行組合式命名衝突 | **雙軌並存** — 組合式命名（GetAnimName / animConvertDic / conditionalAnimDic / CheckAllCombine）照跑不動 | 「每 flag 值掛 List of SpineAnimRef 主副連動」走**新增平行資料層**, 加欄位、**別動 RefreshAnim 主幹**。理由：主副連動本質是「多骨架調度」不是「命名」問題, 硬塞進組合式命名是錯層。要退役組合式另開題（Q6/Q9 未授權） |
| C-Q2 | flag 值基底 0 vs 1 | **儲存層 0-index、顯示層 +1** | m_InitFlagValue 也存 index（預設 0, 編輯器顯示 1）; SetAnimFlagValue 的 clamp 與 ResetAllFlags 歸 0 語意不動。同 Plan A「隱含 Lv1」精神, 不寫魔法數, 與 A 零衝突 |
| C-Q3 | m_ConditionalAreas 升級 vs Q14 全不成立=null | **摺進 list[0] 同構**（extraSkeletons[0] 先例）可行 | 動手前先 grep m_AreaTexture 全消費點（AreaTexture getter 未必唯一入口）; 舊資料二選一：(a) 一次性遷移記帳（同 A1 對 NewExcitement1 的做法, 資料檔少時選這個）(b) 過渡 getter — list 優先、空 list fallback 舊欄（零遷移但留技術債） |
| C-Q4 | RefreshAreaConfigs 的 AutoGenAsset 免面積過濾 | **非 A/B 手筆**（原作者遺留）, crest 建議沿用 | 已轉為企劃題 C-2（Discussion_ForDesigner）; 施工時 UI 加黃字註明「人工命名區塊不受面積過濾」 |
| C-Q5 | 跨分組重疊優先序掛哪層 | **掛 AreaService.CheckArea 來源端, 不掛 HGameBase 收集點** | 現行 CheckArea 已按 clickAreas list 順序 first-hit 早退 = 企劃要的「上面優先」**已成立**; C 只需補編輯器排序 UI + 寫進驗收。HGameBase 那點是 guard 點不是判定點, 別疊邏輯（同「判定做在源頭」哲學, 防 pitfall 第 4 條重演） |

**summit 讀 code additional finding（併入 C 施工項）**: ClickAreaAsset.CheckArea 以 `GetPixelBilinear` 取色後做色碼**精確**字典比對 — 雙線性在色塊邊界混色 → 查無此 key → **每個色塊邊緣一圈點不到**。這是 Q13「色彩容差與美術約定」的技術根因（被註解掉的最近色比對邏輯就在同函式下方）。兩條路：美術硬邊純色出圖（首選, 已發企劃題 C-1）或改容差比對（邊界歸屬變模糊）。

**企劃待回七題**（C-1~C-7, 全有預設值, 不擋工）→ `Docs/Plan/HSceneEditorRework/Discussion_ForDesigner.md` 的「Plan C 開工題」章節 + 酒館 @熊汁 白話版。
