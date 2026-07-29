---
id: decision_impl-verdicts-a-b
topic: hscene-editor-rework
title: A/B 施工級判決濃縮（十題+QA修正+PopupGrouped三題）
type: decision
status: active
created_at: 2026-07-29
created_by: crest-001
links: [hscene-editor-rework/knowhow_a-b-deliverables]
related_docs: [tavern:2026-07-28#9346, tavern:2026-07-28#9375, commit:b33d2add, commit:09ef2c9c, commit:afec076b, commit:71b9f7f, Docs/Plan/HSceneEditorRework/Plan_A_Core_Params.md, Docs/Plan/HSceneEditorRework/Plan_B_AssetImport_SpineGroups.md]
---

**A/B 施工級判決濃縮**（crest-001 第一手, 2026-07-28 施工當日; 推導在酒館 ref, 這裡只留結論+可行動守則）:

**Plan A 五題**（判決 tavern:2026-07-28#9346, 施工 commit:b33d2add + 驗收修正 commit:09ef2c9c）:
| # | 判決 | 可行動守則 |
|---|---|---|
| 1 | ExcitementLevelAsset **直接刪不留 Obsolete**（專案未出貨） | 前置=資料遷移記帳: NewExcitement1.json 值抄入場景 satisfiedSetting 後刪檔（commit message 有帳） |
| 2 | HakoniwaAsset 補**同構** satisfiedSetting, excitementLevel 兩邊刪 | 箱庭與 HScene 等級語意一致, 新欄位一律兩邊同構 |
| 3 | 改名 m_CanLevelDecrease; false=等級棘輪（衰減不掉級）; **高潮 reset 無視此設定強制歸「隱含 Lv1」** | 註解寫「隱含第一級」不寫 index 0 魔法數 |
| 4 | EventTriggerTimming.Satisfied33/66/100 **保留標 deprecated**（Hakoniwa.json 三處在用） | 新資料走 ValueThresholdTrigger; 該 json 遷移完才可刪 enum 值 |
| 5 | HGameValueAsset 衰減暫停**改走 InteractionLockService.Locked**（取代直查 AVGManager） | 行為差異=修正非回歸（高潮期間衰減也停）; 驗收清單有對應測項 |

**Plan A 驗收修正**（Tim QA, tavern:2026-07-28 晚 + commit:09ef2c9c）: 高潮期間仍可操作 — 根因=只 guard 新管線, Test.json 走舊 areaEvents。**修法=ClickInfo.PreUpdate 輸入源頭攔截**（pressed/firstDown 視為沒按）+ HGameBase 區域收集點「視為不在任意互動區」雙保險 + HGameBase.IsClimax getter + HControlPanel 鎖定期間 TimeScale=0 凍結。

**Plan B 五題**（判決 tavern:2026-07-28#9375, 施工 commit:afec076b）:
| # | 判決 | 可行動守則 |
|---|---|---|
| B1 | 音效導入**輕量版**: Utage key 下拉+資料夾篩選 | 音效 asset 體系除非 E4/F3 撞需求才開獨立 plan |
| B2 | AssetFolderFilter 掛 HSceneAsset.config, **空清單=不過濾** | 全域預設層 YAGNI 不做 |
| B3 | 前綴解析順序核可但**轉 Pending P3**（Tim: 改由 Odin 式下拉自動分組） | PopupGrouped 已落地 commit:71b9f7f; 動畫下拉接線待 P3 定案 |
| B4 | 過濾語意精確化: **無分組定義=全列（過渡態）/ 有定義=只列已分組** | 靜默 fallback 只存在於無分組態 |
| B5 | SpineAnimRef: anim=序列化 SSoT / group=純過濾 / skeletonID 情境可隱含 / 失效標紅 | baseAnimName 雙職責只退役「分組」半邊, GetAnimName 拼接職責保留 — 別手癢全刪 |

**PopupGrouped 三題**（Tim Discord 拍板 2026-07-29 08:47, commit:71b9f7f）: ①全部同組→隱藏分組列退化原版 ②選組後顯示全名 ③標籤固定英文 All/Other 不 localize。
