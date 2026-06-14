---
id: 20260530_basecamp_cmd-startnewgame-domain-reload-first-call
title: Cmd_StartNewGame domain reload kills async chain (meadow finding + first-call caveat)
author_persona: basecamp
author_agent: claude-code
created: 2026-05-30
last_updated: 2026-05-30
topics:
  - cmd-system
  - unity-editor
  - debug-lesson
subjects:
  - Cmd_StartNewGame
  - EditorSettings
  - EnterPlaymode
  - enterPlayModeOptions
  - DisableDomainReload
  - UniTask
  - UCL_AgentCommandWatcher
tags:
  - domain-reload
  - async
  - playmode
  - debug
  - dogfood
related_notes:
  - 20260530_basecamp_eov-ui-architecture-agent-reflection
visibility: public
status: live
---

## 摘要

Unity 預設 `EnterPlaymode` 觸發 **domain reload**（C# 整個 AppDomain reload），會把 Cmd async chain 的 state 殺光 — UniTask `await` 永不回，Cmd 卡死。**meadow 2026-05-29 寫 Cmd_StartNewGame 時撞到**，加 Phase 0 guard 偵測 `EditorSettings.enterPlayModeOptions` 是否啟用 `DisableDomainReload`，沒啟用 → 教 user 怎麼設定或用 `autoEnableSetting=true` 自動啟。**但有 first-call caveat**：setting 啟用後仍需經一次 reload 才生效，**首次 call 仍會被殺**。

## 怎麼學到的

- 2026-05-29 basecamp dogfood meadow 剛 ship 的 Plan_Cmd_StartNewGame_Integration 7 步工具鏈，撞「Phase 4 卡死」
- 初步推測 `m_Inited` reflection false 卡，meadow 18:16 ship finding 修正為「Phase 2 EnterPlaymode → domain reload kill Cmd async state」
- 2026-05-30 basecamp 又 dogfood Cmd_StartNewGame（meadow 已 ship 完整版含 Phase 0 guard），用 `autoEnableSetting=true` 還是撞 — first-call caveat 確認：setting 修改後立即進 PlayMode 仍 reload 殺 Cmd
- Tim 2026-05-30 上午回報「Unity 剛被關閉重啟了」對應到時間軸 — autoEnableSetting=true 修改 ProjectSettings.asset 可能搭配 RCG_UnlockData ID:None exception 觸發 Editor crash

## 經驗本體

### Root cause

Unity Editor `EnterPlaymode()` 預設行為:

1. 切到 PlayMode
2. **Reload domain** (重新編譯 + reload assemblies + reset all static state)
3. （可選）Reload scene

第 2 步是預設 ON。**所有 C# static field + `UniTask` 跑中的 Task 都會被殺**。Cmd_StartNewGame 用 `await UniTask.WaitUntil(...)` 跨 Phase 2 進 PlayMode → reload 殺 → await 永不 resume → Cmd 卡死。

### Mitigation 1 — Editor 設定關 domain reload

`Edit → Project Settings → Editor → Enter Play Mode Settings`：

- ☑ Enter Play Mode Settings (啟用整個 group)
- ☑ Disable Domain Reload (關 domain reload)
- ☐ Reload Scene (可選關，加快進場)

**完成後重啟 Editor 一次**讓 setting 真正生效。之後 EnterPlaymode 就跳過 reload，Cmd async chain 活。

### Mitigation 2 — Cmd 自己啟用 setting（meadow 寫的 autoEnableSetting=true）

Cmd_StartNewGame Phase 0 偵測 setting，沒啟用就跑：

```
EditorSettings.enterPlayModeOptionsEnabled = true;
EditorSettings.enterPlayModeOptions |= EnterPlayModeOptions.DisableDomainReload;
```

**但 first-call caveat**: setting 修改不會立即生效，仍需經一次 EnterPlaymode 才真正生效。**第一次跑 Cmd_StartNewGame `autoEnableSetting=true`** → 設 setting → 進 PlayMode 仍 reload 殺 → Cmd 死。**第二次跑（setting 已生效）** → 才會跳過 reload，Cmd 活。

### Mitigation 3 — autoEnableSetting=true 仍有 side effect

`EditorSettings.enterPlayModeOptions` 寫到 `ProjectSettings.asset`（git tracked）。autoEnableSetting=true 改的是 project-level setting，影響全 team。**且修改 + 立即進 PlayMode 觸發 Editor 不穩**（Tim 2026-05-30 觀察到 Editor 自動關閉重啟）。

## 應用

新 Cmd 用 `async UniTask` chain + 跨 PlayMode 進入：

1. **必先確認 `EditorSettings.enterPlayModeOptions` 已啟用 DisableDomainReload + Editor 已重啟過一次**
2. Cmd Phase 0 偵測 setting，沒啟用 reject + 教 user 手動設定（autoEnableSetting=true 是 fallback 但不可靠）
3. 文件化「首次設定後需 restart Editor」這條 caveat 在 Cmd help message + skill SOP
4. 設計類似的 long-running async Cmd 時參考此 pattern

## 反例

- ❌ 期待 `autoEnableSetting=true` 一次就 work — 首次 call 必死
- ❌ 把 setting 改動 silent（沒 log / 沒 markdown 提示）— Tim 不知道為何 Editor 行為變
- ❌ Cmd 在 setting 還沒生效就 enter PlayMode — async state 必殺
- ❌ 把 `EnterPlaymode` 當輕量操作 — Unity 把它當「reload everything」

## 後續

- Cmd_StartNewGame `autoEnableSetting=true` 的 message 該補 first-call caveat 警告（basecamp Q3 review 已提，meadow 可 patch）
- 或考慮 deprecate `autoEnableSetting=true`，純走 Editor 手動設定路線（更可靠）
- Editor crash 跟 RCG_UnlockData ID:None exception 的關係待 game-side 排查（meadow / Tim 後續）

## 補注
