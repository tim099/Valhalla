---
id: knowhow_a-b-deliverables
topic: hscene-editor-rework
title: A/B 交付物使用說明（SpineAnimRef/LockService/Trigger/FolderFilter 下一棒怎麼用）
type: knowhow
status: active
created_at: 2026-07-29
created_by: crest-001
links: [hscene-editor-rework/decision_impl-verdicts-a-b]
related_docs: [Assets/Scripts/HScenes/HSceneAssets/SpineAnimRef.cs, Assets/Scripts/HScenes/HSceneService/InteractionLockService.cs, Assets/Scripts/IAsyncEvents/EventTriggers.cs, Docs/API/HScenes/InteractionLockService.md, Docs/API/HScenes/HSceneAssets/SpineAnimRef.md, Docs/API/HScenes/HSceneAssets/TriggeredEventSetting.md]
---

**A/B 交付物使用說明**（給下一棒/Plan C~F 施工者; state -29b 的就緒件清單是目錄, 這篇是怎麼用）:

**SpineAnimRef**（Assets/Scripts/HScenes/HSceneAssets/SpineAnimRef.cs）— C/E/F 所有 Spine 動畫欄位一律用它:
- 宣告: `public SpineAnimRef m_Anim = new();`（骨架自選）或 `new SpineAnimRef("骨架ID")`（情境隱含, 可自行子類加 UCL_HideOnGUI 藏骨架欄）
- runtime 只讀 `m_Anim.m_Anim`（動畫名 SSoT）; `m_Group` 純過濾別在 runtime 判斷它
- 選項 provider 依賴 `UCLI_Asset.s_CurOnGUIAsset` 章節 context — CommonEditPage 與 HSceneEditorWindow 都已接線; 新編輯面板若繞過這兩者, 記得自己設 s_CurOnGUIAsset（try/finally）
- 失效驗證: `IsAnimValid()` + NameOnGUI 紅字已內建, 欄位層不用重做

**分組過濾語意**（SkeletonGraphicSetting）: 下游取「可選動畫」一律呼叫 `setting.GetSelectableAnims()` 或 `GetGroupAnims(group)` — 不要直接讀 skeleton.GetData().anims（會繞過「未分組不出現」語意）。主骨架=extraSkeletons[0]（同構, 無特例）。

**InteractionLockService**（HScenes/HSceneService/）— 操作暫停:
- 查詢: `InteractionLockService.Locked`（static, null-safe 不用判空）; 高潮狀態查 `HGameBase.Ins.IsClimax`
- 排程演出（Plan F）: 自訂 source 字串 `Ins.PushLock("MySchedule")` / `PopLock`（計數式可重入）; 高潮/AVG 兩個內建 source 已自動管理
- **新互動路徑不用加 guard** — 輸入已在 ClickInfo.PreUpdate 源頭攔（pitfall 第4條的修法）; 但「非 ClickInfo 的輸入」（例如 uGUI Button）要自己 AND !Locked（HButton 是範例）

**TriggeredEventSetting + IEventTrigger**（IAsyncEvents/EventTriggers.cs）— 企劃 2.2.6 事件設定:
- 3.11.3/3.12.3/3.13.2/3.14 的「觸發源+事件」欄位直接用 `List<TriggeredEventSetting>`（HSceneAsset.triggeredEvents 是掛法範例, TriggeredEventService 驅動）
- 新觸發源=繼承 EventTriggerBase（維護自己的邊沿/once 狀態, GameInit 重置）; ButtonPressedTrigger 的 NotifyPressed 接線留給 Plan D ButtonZone

**AssetFolderFilter**（HScenes/HSceneAssets/）: config.m_SpineFolders/m_SpriteFolders/m_SoundFolders 三欄就緒。Plan C 3.4.7 圖片下拉接線: 選項 provider 取 `(UCLI_Asset.s_CurOnGUIAsset as IHSceneConfig)?.Config?.m_SpriteFolders` 過濾（UtageVoiceSetting.VoiceNameOptions 是完整範例, 含「引擎未就緒保底列當前值」的防卡欄位手法）。

**A 的條件/數值零件**: FlagValueCondition（AnimFlag 現值, 電平）vs AlteredAnimFlagCondition（變動, 邊沿）; ExcitementLevelCondition 有 levelMax 區間; HGameValueAsset.m_DecreaseRate 可負值=成長。
