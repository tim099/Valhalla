---
id: state_progress-2026-07-29c
topic: hscene-editor-rework
title: 施工進度快照 2026-07-29c（C 資料層完工, 未 commit/未實測）
type: state
status: superseded
created_at: 2026-07-29
created_by: crest-001
links: [hscene-editor-rework/state_progress-2026-07-29b, hscene-editor-rework/state_progress-2026-07-31]
related_docs: [Docs/Plan/HSceneEditorRework/Plan_B_AssetImport_SpineGroups.md, Docs/Plan/HSceneEditorRework/Discussion_Pending.md]
---

**施工現況**（2026-07-29 11:50 快照 — 過期時 supersede 本檔, 別改寫）:

| Plan | 狀態 | 備註 |
|---|---|---|
| A 基礎資料層 | ✅ 完工（crest-001, b33d2add + 09ef2c9c, Tim 實測過） | — |
| B 素材導入+Spine分組 | ✅ 完工（crest-001, afec076b + bump 32efceee, Tim 測過） | B3 → P3 pending |
| PopupGrouped 下拉分組 | ✅ 完工（UCL_Core@LY 71b9f7f + bump e59b5fb2） | 動畫下拉接線待 P3 |
| **C Flag+互動區域** | 🔨 **資料層+編輯器語意完工（summit, 尚未 commit / 尚未 Editor 實測）** | 詳見下方 |
| D 互動+按鈕+操作 | ⬜ 未動 | ClickTypeAsset 補完 + :79 疑似反向 bug |
| E 觸摸動畫 | ⬜ 未動 | 依賴 C 色塊 + D 互動類型; 含副視窗顯示控制 |
| F 表情+被動效果 | ⬜ 未動 | 先抽共用排程器 |
| Pending | P1 棒棒 / P2 物件槽 / P3 動畫下拉自動分組 | 不擋工 |

**C 這一棒做了什麼**（code 已改, compile 0 error, SelfTest 綠）:
- `ClickAreaAsset`: `m_AreaTexture` + `m_ConditionalAreas` → **`m_AreaImages`（有序圖片資料清單）**; 上面優先 / 全不成立 = 無法互動（Q14）; 舊資料一次性遷移 **39 檔 87 筆**（原條件圖在前、原主圖當無條件保底在後 = 行為不變）
- 取色 `GetPixelBilinear` → **`GetPixel` 點取樣**（邊界混色根治, 與素材既有 FilterMode=Point 對齊）
- 新檔 `ClickAreaSpriteEntry`: 分色圖下拉吃 `config.m_SpriteFolders`（企劃 3.4.7）, 含靜態快取防每幀讀檔
- `SkeletonGraphicAsset`: 新增 **`AnimFlagConfig.valueAnims`（值→動畫組平行資料層）** + `initValue`（每 Flag 各自, 存 0-based 顯示 1-based）+ `ApplyValueAnims()` 掛在 RefreshAnim 尾端（**未動 GetAnimName 主幹**）+ `MaxIndex`（names 空時不被夾成負數）+ C-3 撞車標紅
- 兩支 `SelfTest()` 靜態方法（Cmd_Invoke 觸發, 結果走 Debug.LogWarning 落 Simulation log）

**驗收實測 11:47**: ClickArea 39 分組/87 圖片資料/0 壞資料; SkeletonGraphic 104 骨架/139 flag/**啟用新層 0 個（舊資料零影響）**/0 越界/0 撞車。

**下一棒要知道的**:
- C 尚未 commit、尚未 Editor 實機驗收（驗收要點見 Plan_C 文件末「施工進度」段）
- 副視窗顯示控制（CanvasGroup/alpha, 不可 SetActive(false)）歸 Plan E, C 只備資料層
- 遷移腳本是一次性的, 已跑完; 之後新資料直接編 `AreaImages`
