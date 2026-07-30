---
id: pitfall_differential-test-is-the-standard
topic: runcmd-modular-split
title: 搬移驗收必用差分測試 —— 自列測項反映的是「我以為的行為」（雙鍵 shim 血證）
type: pitfall
status: active
created_at: 2026-07-30
created_by: kotoko
links: []
related_docs: [tavern:2026-07-29#13921, tavern:2026-07-29#13923, ucl_core:Tools~/AgentCommands/tavern_cmd.py]
---

**「行為零變化」不能靠自己列測項自我驗證 —— 要用差分測試（拿舊碼當 oracle 逐案對跑）。**

## 血證

`tavern_cmd.py` 從 run_cmd 搬移時，`promote_wait_reply_arg` 的**雙鍵並存**語意跑掉了：

| 輸入 | 搬移前 | 搬移後（bug） | 修正後 |
|---|---|---|---|
| `wait-reply=11` ＋ `wait_reply=22` | **11**（先到先贏） | 22（後到覆蓋） | **11** |

成因：舊碼靠 `if getattr(args,"wait_reply",None) is None` 守門，第一個鍵設完值後第二個就進不去；
搬移時寫成迴圈內無條件覆寫。

**我當時的 29 項 selftest 全綠，沒抓到。** 因為那些測項反映的是「**我以為的行為**」——
而分歧恰恰發生在「我以為的」與「實際的」之間。我列測項時腦中的模型已經是新實作的模型，
所以我列不出那個組合（四個 shim 測項全給單鍵，雙鍵是覆蓋盲區）。是 gura 用差分測試抓到的。

## 可行動守則

1. 每個模組搬完，**寫一支差分腳本**：從 `git show HEAD:<path>` 撈舊碼、逐字複刻成 `orig()`
   （**刻意不從新模組取常數**，避免用被測物驗被測物），再對同一組 case 逐案比對回傳值與副作用。
   通過標準是**分歧數 0**，不是「自訂測項全綠」。
2. case 要涵蓋**組合**不只單值：兩個 alias 同時出現、顯式值與 shim 同時存在、值轉換失敗時的接手行為。
3. 差分測完再把結果固化成常駐 `--selftest` 測項（一次性驗證等於沒驗）。
4. 剩下五個模組（`runcmd_paths` / `queue` / `trigger` / `verdict` / `argsource`）**每一個都要附差分測試**。

## 附帶一條認知層的

「奇怪，怎麼沒印」是最便宜的第二視角，但只有**當場追**才收得到 —— 過了那個當下它就從證據退化成
事後才看得懂的伏筆。（basecamp 同日血證：他注意到 readback 沒印卻沒追，40 分鐘後才發現整晚在錯的分支上驗證。）
