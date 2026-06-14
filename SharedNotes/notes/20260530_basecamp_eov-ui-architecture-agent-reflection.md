---
id: 20260530_basecamp_eov-ui-architecture-agent-reflection
title: EOV UI 架構 + agent 反射操作 (UIInspect / UIInvoke)
author_persona: basecamp
author_agent: claude-code
created: 2026-05-30
last_updated: 2026-05-30
topics:
  - ui-architecture
  - cmd-system
  - agent-collaboration
subjects:
  - UCL_GameUI
  - UCL_UIService
  - RCG_MainMenu
  - RCG_SelectBigMapUI
  - Cmd_UIInspect
  - Cmd_UIInvoke
  - UIStack
tags:
  - reflection
  - unity-editor
  - dogfood
  - agent-introspection
related_notes: []
visibility: public
status: live
---

## 摘要

EOV UI 走「`UCL_GameUI` 基類 + `UCL_UIService` singleton 管 stack」架構，**`UCL_UIService.GetUIStackInfo()` 是 agent 反射 UI 的標準入口**，搭配 `Cmd_UIInspect` + `Cmd_UIInvoke` 兩個 T78 Cmd 可完整偵測 + 操作 UI 不必滑鼠點擊。

## 怎麼學到的

Tim 派 task：「上班時間到 10:00，請先嘗試用昨天新增的 CMD 進入一局新遊戲，接著開始用 CMD 分析 UI 進行操作（同時讀對應的 .cs 學習 UI 邏輯）」。Cmd_StartNewGame 撞 domain reload 卡住期間，趁 Editor idle 把 UI 架構的 .cs 全讀過一遍。

## 經驗本體

### UCL_GameUI （UI 基類）

- 繼承 `MonoBehaviour`
- 五個 virtual property：`IsUIOverlay` / `Layer` (預設 100) / `Reusable` (預設 false) / `IsFullScreen` (預設 false) / `OnTop` / `OnCovered` hooks
- 三個 lifecycle hook：`Init()` / `OnTop()` / `OnCovered()`
- `m_OnCloseAction` action delegate
- `Close()` 走 `UCL_UIService.Ins.OnUIClosed(this)` — UI 不自己 Destroy，由 service 統一管

### UCL_UIService （UI 管理 singleton）

- `Ins` static singleton
- `m_UIStack` — `List<UCL_GameUI>` 模擬 stack (LastElement = top)
- `m_UIPools` — `Dictionary<Type, Queue<UCL_GameUI>>` 重用 (Reusable UI close 時進 pool 而非 Destroy)
- `m_UIRootLayer` / `m_UIOverlayRootLayer` — `Dictionary<int, RectTransform>` 分層 root (Layer 高低決定渲染順序，`SetAsLastSibling` 排序)
- 兩個 root canvas：`m_UIRoot` (一般 UI) + `m_UIOverlayRoot` (overlay)
- `CreateUI<T>()` 從 pool 取 or instantiate；自動 push 進 stack；若 IsFullScreen 對前一個 UI call `OnCovered()`
- `CreateUIFromResource<T>()` 從 Resources/ 載 prefab
- `CreateUIFromAddressable<T>()` 從 Addressables 載 (async)
- `OnUIClosed(ui)` 從 stack remove；若 Reusable 進 pool；否則 Destroy
- **`GetUIStackInfo(bool iIncludeMethods)`** — ★ 給 agent 反射的標準入口

### Agent 端 UI Cmd（T78 Tim 拍板）

#### Cmd_UIInspect

- CommandType = "UIInspect"
- args: `filter=<class name>` / `include_methods=true|false` / `top_only=true|false`
- 守門: `UCL_UIService.Ins == null` 直接 reject "非 Play Mode"
- 渲染 markdown: 每個 UI 列 type/gameObject/layer/IsTop/methods

#### Cmd_UIInvoke

- CommandType = "UIInvoke"
- args: `type=<class name>` + `method=<method name>` (必填) / `include_protected=true|false` / `broadcast=true|false`
- 找 target UI: 優先 active，fallback inactive (印 warning)
- type match 用 short name / full name / EndsWith
- walk type hierarchy 找 method (含 inherit protected)
- blacklist Unity lifecycle / Object base method 避誤觸
- Invoke + TargetInvocationException unwrap

### RCG 端 UI 範例

#### RCG_MainMenu

- 繼承 `UCL.Core.Game.UCL_GameUI`
- `Ins` static singleton
- `Create()` 走 Addressable (async `CreateUIFromAddressable`)
- `Init()`：set `m_Inited = true` (private bool)，串各 button onClick：
  - `m_ContinueButton.onClick.AddListener(ShowLoadSelectUI)`
  - `m_NewGameButton.onClick.AddListener(StartNewGame)`
  - `m_BaseButton.onClick.AddListener(OpenBase)`
  - 等
- `StartNewGame()` 內容**極簡**:
  - `var aUI = RCG_SelectBigMapUI.Create()`
  - `aUI.OnEnterMapAct = Close` (玩家選定地圖時關掉 main menu)

#### RCG_SelectBigMapUI

- 繼承 `UCL.Core.Game.UCL_GameUI`
- `Create()` 走 `UCL_UIService.Ins.CreateUIFromResource<>` (sync, Resources 不是 Addressable)
- UI 元素: `m_BackButton` / `m_ConfirmButton` / `m_BigMapPanelTmp` (template) / `m_SelectedMapTitle/Desc/Icon` / `m_FogUI` / `m_SelectableCardListUI`
- `OnEnterMapAct` Action — 玩家選定地圖後呼叫
- `Init()`：
  - 從 `RCG_BigMapManager.GetAllBigMaps()` 取所有大地圖
  - 過濾 tutorial / 未解鎖角色 (`!m_DetailSetting.m_IsTutorial && unlocked > 0`)
  - 用 `m_Pool` (`UnityComponentPool<RCG_BigMapPanel>`) 創 BigMapPanel
  - 排序 SortingOrder
  - Mark `Main_Mode_Unlock` displayState
  - 跑 `InitAnim()` (FadeIn → SetActive → FadeOut)

## 應用

下次要操作 main menu / 任何 UI 時：

1. **先跑 `Cmd_UIInspect`** 看 UI stack 知道現在有哪些 UI active + 哪個是 top + 每個 UI 有哪些可 invoke method
2. **再跑 `Cmd_UIInvoke type=<X> method=<Y>`** 模擬點按鈕（不必滑鼠）
3. 寫新 UI 時繼承 `UCL_GameUI`，遵守 `Init/OnTop/OnCovered/Close` lifecycle，讓 agent 端 UIInspect/UIInvoke 自動 work
4. 設計 UI 流程時注意 `OnEnterMapAct = Close` 這種 callback 設計 — UI 之間用 action 串而非互相直接呼叫，agent 操作時看 callback 就懂下一步

## 反例

- ❌ 不繼承 `UCL_GameUI` 自己寫 UI 流程 — agent 偵測不到，UI lifecycle 也沒人管
- ❌ Method 帶參數想被 `Cmd_UIInvoke` 觸發 — 目前不支援，要無參 method
- ❌ Method 名跟 Unity lifecycle 撞 (Awake/Start/Update 等) — 會被 Cmd_UIInvoke blacklist 擋
- ❌ 期待 `Cmd_UIInspect` 在非 PlayMode 跑 — `UCL_UIService.Ins == null` 會 reject

## 後續

- Cmd_UIInvoke 不支援帶參 method（meadow 或 trailhead 將來可補）
- `_subjects/` 該 cross-link 到 `RCG_AlertUI` / `RCG_BattleEndUI` 等其他 UI 子類別當 follow-up note
- 完整 UI 流程的「進新遊戲」需要 Editor 已在 PlayMode + UCL_UIService 已 init，配合 Cmd_StartNewGame 流程 (見另一筆 note)

## 補注
