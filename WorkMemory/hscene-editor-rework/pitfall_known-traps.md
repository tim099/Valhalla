---
id: pitfall_known-traps
topic: hscene-editor-rework
title: 已知坑清單（WIP 所有權/Hakoniwa enum/輸入源頭 guard/文件漂移）
type: pitfall
status: active
created_at: 2026-07-29
created_by: summit
links: []
related_docs: [tavern:2026-07-28#9355, commit:09ef2c9c]
---

**本工作特有的坑**（都是實際撞過的）:

1. **WIP 所有權**: `SatisfiedSetting.cs`/`HbodyAsset.cs` 拍板時是他人 untracked WIP — 已由 Plan A 接手定稿, 但同型情況再現時（企劃點名的 asset 是零引用 WIP）先跟原作者確認再動
2. **`Hakoniwa.json` 用著 `Satisfied33/66/100`** — EventTriggerTimming 這三個 enum 值標 deprecated 但**不可刪**（刪了箱庭資料炸）, 遷移完才能刪
3. **runtime 檔引 UnityEditor namespace** — SatisfiedSetting 曾有 `using UnityEditor.ShaderGraph.Internal;`（player build 炸）, Plan A 已修; 同族錯誤 review 時盯 using 區
4. **高潮暫停要在輸入源頭關** — Plan A 驗收被 Tim QA 抓過: 只 guard 新觸摸 pipeline, 舊路徑（Test.json AreaEvent）繞過照樣能摸。修法 = 滑鼠輸入源頭一個開關管所有路, 別在每條路各設閘門
5. **企劃文件會漂**: 3.5.2「速度倍率固定值分檔」已被拍板推翻（slider 平滑 + Min/MaxSpeed）; 3.9.2 詳細說明漏「操作後視為觸摸中的時間」欄。**以 Discussion_OpenQuestions 拍板記錄為準**, 文件下版才修

**可行動守則**: C~F 各 plan 動工前把本清單過一遍; 發現新坑追加 fragment 別改本檔正文。
