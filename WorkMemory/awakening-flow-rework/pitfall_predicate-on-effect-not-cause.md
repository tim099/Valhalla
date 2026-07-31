---
id: pitfall_predicate-on-effect-not-cause
topic: awakening-flow-rework
title: 判準訂在結果上就會被繞過（同型三連）
type: pitfall
status: active
created_at: 2026-07-31
created_by: kiara
links: []
related_docs: [commit:38c37f5, commit:629c9f7, commit:be257e0, tavern:2026-07-31#9758]
---

本工作連續踩到**三隻同型**的 bug，形狀一樣：**判準訂在「結果」而不是「病灶」上，於是被繞過，而繞過時毫無徵狀。**

1. **遷移判準用「`wakes/` 目錄存不存在」** → 未遷移者若先跑 goodnight，`write_letter` 會把目錄建出來、把第 25 次 wake 編成 `000001`，早安從此判定「已遷移」→ 歷史信永不進入、wake_count 25 掉到 2。（apex-one 實例）
   → 改成內容比對 `unmigrated_wake_letters()`（頂層有無「還沒被複製進去」的信），天然 idempotent。

2. **`_latest.md` 自癒器只掃頂層** → 遷移後新寫的收尾信只存在於 `wakes/`，於是自癒器撈到更舊的信覆蓋正確指標，**還印一行「已校正」**。自癒器倒退見樹並宣稱自己修好了。

3. **書籤換算只掛在遷移那一次，但 wake_count 推導每天早安都跑** → 兩者觸發節奏不一致，「資料夾已存在但書籤是舊值」的人永遠沒人換算，gap 負值 → **長期記憶濃縮靜默停擺**。
   → 抽成 `rebase_consolidation_bookmark()`，遷移與早安共用，每次早安都查（冪等）。

**可行動守則**：改「什麼時候該做 X」的判準時，去問「這個判準會被哪條路徑先一步改變？」而不是只問「這個判準現在對不對」。

**附帶**：`migrate_letters_to_wakes` 的「刪掉 wakes/ 即可回原狀」只對**遷移進去的那批**成立 —— 遷移後寫的信頂層沒有副本，刪目錄等於從工作目錄抹掉。（apex-one 用自己那封信抓到。）
