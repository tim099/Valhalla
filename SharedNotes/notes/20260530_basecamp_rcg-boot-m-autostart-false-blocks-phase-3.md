---
id: 20260530_basecamp_rcg-boot-m-autostart-false-blocks-phase-3
title: RCG_Boot.m_AutoStart 預設 false 卡 Cmd_StartNewGame Phase 3
author_persona: basecamp
author_agent: claude-code
created: 2026-05-30
last_updated: 2026-05-30
topics:
  - cmd-system
  - unity-editor
  - debug-lesson
  - boot-flow
subjects:
  - RCG_Boot
  - m_AutoStart
  - Cmd_StartNewGame
  - RCG_MainMenu
  - RCG_StartScene
  - RCG_GameManager
  - LoadScene
tags:
  - scene-transition
  - boot
  - inspector-flag
  - dogfood
  - debug
related_notes:
  - 20260530_basecamp_cmd-startnewgame-domain-reload-first-call
  - 20260530_basecamp_eov-ui-architecture-agent-reflection
visibility: public
status: live
---

## 摘要

EOV 的 `RCG_Boot` (boot scene 載入器) 有個 inspector 欄位 `m_AutoStart` (預設 `false`)：boot 跑完後**只有 m_AutoStart=true 才會自動切到 RCG_MainMenu**，否則停在 RCG_StartScene。dev mode 預設 false → Cmd_StartNewGame Phase 3 期望「boot 自動切 scene」是錯的假設，永久 timeout。

## 怎麼學到的

2026-05-30 早上 Tim 派 task「進新遊戲測試」，跑 Cmd_StartNewGame from=reset autoEnableSetting=true → Phase 3 reject「RCG_Boot didn't transition to RCG_MainMenu scene after 15s (current scene='RCG_StartScene')」。一開始懷疑 RCG_UnlockData ID:None exception 阻止切 scene，讀 RCG_Boot.cs 才發現真相是 `m_AutoStart` 預設 false。RCG_UnlockData exception 是另一個 game-side bug，跟卡 Phase 3 無關。

## 經驗本體

### RCG_Boot.cs 關鍵 code

```csharp
public class RCG_Boot : MonoBehaviour
{
    /// 自動切換到 RCG_MainMenu
    public bool m_AutoStart = false;   // ← 預設 false (dev mode)

    public static bool IsBooted { get; private set; } = false;

    private async UniTask Boot()
    {
        // ... init module / GameManager 等 ...
        m_GameManager = await RCG_GameInitData.PrefabResSetting.Boot(token);

        if (m_AutoStart && m_GameManager != null)
        {
            m_GameManager.LoadScene(RCG_Scenes.RCG_MainMenu);   // ← 只有 m_AutoStart=true 才切
        }

        IsBooted = true;
        Started = true;
        Debug.LogWarning($"Boot Duration:{duration.TotalSeconds.ToString(".00")}s");
        Destroy(gameObject);
    }
}
```

### 對應 Cmd_StartNewGame Phase 3 設計缺陷

meadow ship 的 Cmd_StartNewGame Phase 3 邏輯：

```csharp
await UniTask.WaitUntil(
    () => SceneManager.GetActiveScene().name == "RCG_MainMenu",
    cancellationToken: token).Timeout(TimeSpan.FromSeconds(aPhaseTimeout));
```

**期望** RCG_Boot 自動切 scene。但實際上 dev mode `m_AutoStart=false` → boot 跑完 scene 仍在 RCG_StartScene → Cmd 永遠 timeout。Phase 3 reject。

這是 meadow Plan §7「隱性風險預測」沒 cover 的：她偵測 m_Inited / Singleton / DDOL，沒偵測 m_AutoStart。

### 三個解法 (trade-off)

| # | 解法 | trade-off |
|---|---|---|
| A | game-side：設 RCG_StartScene 的 RCG_Boot prefab m_AutoStart=true | 永久但影響 dev workflow（dev 想停在 boot debug 變慢） |
| B | Cmd-side：Phase 3 加 active trigger — 若 IsBooted=true 但 scene 仍 StartScene → 主動 invoke RCG_GameManager.Ins.LoadScene(RCG_Scenes.RCG_MainMenu) | 最 robust；需 meadow patch |
| C | Agent workaround：用 Cmd_Invoke 走 RCG_GameManager.Ins.LoadScene(RCG_Scenes.RCG_MainMenu) bypass Cmd_StartNewGame Phase 3 | 立刻 work，每次手動 chain |

## 應用

新 Cmd 設計「等 scene transition」前必先確認：

1. **誰負責 trigger transition?** — Boot loader 自動？玩家點按鈕？開發者 inspector 設定？
2. **transition 是否有條件?** — 像 `m_AutoStart` 這種 dev/prod 行為不同的 flag
3. **Editor / Build 行為差異?** — `#if UNITY_EDITOR` 邏輯可能讓 dev mode 跟 build 行為不一樣
4. **若沒 active trigger，Cmd 該主動觸發**（解法 B 的精神）

讀 game-side .cs 時找：
- `public bool m_*` inspector 欄位 — 預設值不一定是 production behaviour
- `if (m_X && y)` 條件 branch — m_X 預設 false 等於該 branch 永遠不跑

## 反例

- ❌ 假設「boot 完成 = 進 main menu」 — 看 `m_AutoStart` 條件
- ❌ 只看 logs（Boot Duration 21.35s）下結論 boot 成功 — boot 完成 ≠ scene transition
- ❌ 把 Phase 3 timeout 拉長期望「等更久就會切」— 根因不是 timing 是 missing trigger
- ❌ 怪 RCG_UnlockData exception 阻止 transition — 不相關，exception 在另一條 init 鏈

## 後續

- meadow patch Cmd_StartNewGame Phase 3 加 active trigger（解法 B）
- 或 game-side 把 RCG_StartScene 的 RCG_Boot prefab m_AutoStart 設成 true（解法 A，需 Tim 拍板）
- 短期用 Cmd_Invoke workaround（解法 C），可寫成 helper Cmd_Forward_To_MainMenu

## 補注
