---
id: state_progress-2026-07-29b
topic: hscene-editor-rework
title: 施工進度快照 2026-07-29b（A/B/PopupGrouped 完工, 下一棒 C）
type: state
status: superseded
created_at: 2026-07-29
created_by: crest-001
links: [hscene-editor-rework/state_progress-2026-07-29c]
related_docs: [Docs/Plan/HSceneEditorRework/Plan_B_AssetImport_SpineGroups.md, Docs/Plan/HSceneEditorRework/Discussion_Pending.md]
---

**施工現況**（2026-07-29 09:20 快照 — 過期時 supersede 本檔, 別改寫）:

| Plan | 狀態 | 備註 |
|---|---|---|
| A 基礎資料層 | ✅ 完工（crest-001, b33d2add + 驗收修正 09ef2c9c, Tim Editor 實測過） | 高潮繞過修正 = 輸入源頭 guard（見 pitfall 第4條） |
| B 素材導入+Spine分組 | ✅ 完工（crest-001, afec076b + bump 32efceee, Tim 測試 OK） | B1輕量/B2手動分組/B5 SpineAnimRef 落地; B3 → P3 pending |
| PopupGrouped 下拉分組 | ✅ 完工（UCL_Core@LY 71b9f7f + bump e59b5fb2, Tim 測試 OK） | 已接 UCL_AssetEntry ID 下拉; 動畫下拉接線待 P3 定案 |
| C Flag+互動區域 | ⬜ 未動（依賴圖下一棒） | 依賴 B 的 SpineAnimRef（已就緒）; Q13 色彩容差施工時與美術約定; Q14 全不成立=null |
| D 互動+按鈕+操作 | ⬜ 未動 | 含 ClickTypeAsset 補完 + :79 疑似反向 bug（B1 記帳）修 |
| E 觸摸動畫 | ⬜ 未動 | 依賴 C 色塊 + D 互動類型; HbodyAsset 接手（Q2）+ FloatRange 統一（E3） |
| F 表情+被動效果 | ⬜ 未動 | 先抽共用排程器; FaceOn/FaceOff Utage 指令（Q15） |
| Pending | P1 棒棒 / P2 物件槽 / P3 動畫下拉自動分組（機制已落地, 差接線拍板） | 不擋工 |

**B 完工後給 C/E/F 的就緒件**: `SpineAnimRef`（兩段式選單通用型別, 12 個既有消費點的遷移歸各章）、`AssetFolderFilter`×3 掛 config（圖片下拉接線歸 C 3.4.7）、`SkeletonGraphicSetting.GetSelectableAnims()` 過濾語意（無分組=全列/有分組=只列已分組）。
**編輯器 context 缺口已修**: HSceneEditorWindow.OnGUI 已設 `UCLI_Asset.s_CurOnGUIAsset`（scoped entry / SpineAnimRef provider 依賴它）。

需求收斂: 18 題 → 16 拍板 / 3 pending。指派慣例: 酒館 task-assign（T06.3 meta schema）。
