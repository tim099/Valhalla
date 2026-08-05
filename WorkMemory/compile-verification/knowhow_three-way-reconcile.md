---
id: knowhow_three-way-reconcile
topic: compile-verification
title: 改完 .cs 的驗收：recompile → check_compile 交叉對帳 → 停跳台帳當第三方物證
type: knowhow
status: active
created_at: 2026-08-05
created_by: summit
links: []
related_docs: [ucl_core:Skills~/ucl-compile-error/SKILL.md]
---

**改完 .cs 的驗收動作（2026-08-05 起）**

```bash
# 一步：觸發 + 等到真的跑完（會先印 "compile started"，那行出現才代表編譯真的開始）
python <UCL_Core>/Tools~/AgentCommands/run_cmd.py recompile

# 二步：交叉對帳 —— 新鮮度守衛預設開啟，過期會蓋 STALE 並且不印「Clean compile」
python <UCL_Core>/Tools~/AgentCommands/check_compile.py --errors-only --strict-fresh   # 過期 exit 4
```

**旗標速查（check_compile）**
- `--since-file <你改的.cs>`：基準改用那一個檔（1 次 stat，跳過 git，比問 git 更精準也更便宜）
- `--since <epoch|ISO>`：基準改用指定時間
- `--strict-fresh`：過期 exit 4（預設只印警告不改 exit code，以免既有呼叫端行為被改變）
- `--no-freshness`：關掉檢查（＝退回 2026-08-05 之前的行為）
- `--format json` 帶 `stale` / `staleness` 欄位（腳本呼叫端比人更不會看旁邊那行字）

**三方交叉對帳（互相印證，任一單獨都不足）**
1. `recompile` 報的 timestamp / duration / errors
2. `check_compile` 讀同一份 status，且判定它**涵蓋你的改動**
3. 心跳停跳台帳的 gap —— 獨立來源。實測 gap 7.179s vs duration 7.188s，**差 9ms**
   （台帳 gap 通常略大於 duration：停跳含 domain reload，duration 只算編譯）

**編譯遲遲不動時怎麼判斷**：看 `check_compile` STALE 區塊那行 ——
「改動後心跳停跳 N 次」= 凍過，可能正在編；「改動後沒有任何停跳紀錄」= **編譯很可能連開始都沒有**，
把 Unity 切到前景。這一句話取代了手翻 Editor.log 找 `bee_backend … ScriptAssemblies`。

**Editor.log 的地面真相（工具都不可信時的最後一層）**
- `[ScriptCompilation] Requested script compilation because: ...` = 請求登記了
- `Starting: bee_backend.exe ... ScriptAssemblies` = **編譯真的開始了**
- 只有前者沒有後者 = 遞延中
