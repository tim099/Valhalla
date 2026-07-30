---
id: pitfall_verify-traps
topic: agentcmd-schema-codegen
title: 驗證三坑：compile 假綠 / selftest 雙模組 / 用 submit 驗預檢會產生真副作用
type: pitfall
status: active
created_at: 2026-07-30
created_by: kotoko
links: []
related_docs: [eov_docs:docs/Glossary/stale-green.md, eov_docs:docs/Glossary/same-code-mute.md, ucl_core:Tools~/AgentCommands/tavern_cmd.py]
---

**這項工作特有的三個坑**（跨工作通用的教訓另見 agent-lessons-log）：

### ① `check_compile` / `recompile` 會給你假綠 —— 判準要看 dll mtime

實測 2026-07-29：
- `check_compile.py` 回「Errors: 0」但 **timestamp 是前一天**（舊快照）
- `run_cmd.py recompile` 連兩次回報 `0.0s / errors=0 / warnings=0`，而 `UCL_Core.dll` **根本沒重建**
- 真編譯是 12–15s，且會列出全專案 21→100 個 warning

`0.0s + 0 warnings` 是「Unity 認為沒東西要編」的 no-op 回報，與真正的成功**同碼**。
新檔第一次被 import 的那次 refresh 也只會 import 不編譯，要再跑一次才會真編。

**守則**：改完 .cs 判斷有沒有編過，看 `CardGame/Library/ScriptAssemblies/UCL_Core.dll` 的 mtime；
要確認型別真的進了產物可以 `grep -c "<TypeName>" UCL_Core.dll`。

### ② `python <module>.py --selftest` 的雙模組陷阱（configure 設到另一份副本）

以 `python tavern_cmd.py --selftest` 執行時本檔是 `__main__`，而 `import run_cmd` 內的
`import tavern_cmd` 會載入**另一份副本**並只設定那一份 —— `__main__` 這份的注入值全是 None。
`tavern_handshake.py` 早就踩過同一個。

**守則**：selftest 入口要**自己呼叫 configure**（從 run_cmd 取解析結果），不能靠對方幫你注入。
而它會「炸得漂亮」而不是靜默走錯目錄，是因為模組層拒絕給 fallback 預設值 —— 這條規則不能拿掉。

### ③ 驗 client 預檢不要用 `submit`／`run` —— 預檢通過就代表它真的會被執行

2026-07-29 我為了驗「`create_trpg_room` 不再被擋」跑了 `run_cmd.py submit Tavern --arg op=create_trpg_room`，
結果**真的建了房 `trpg-probe` 並註冊進 Discord mirror 監看清單**。
已用 `op=createroom --arg id=trpg-probe --arg mirror=false` 反註冊還原，殘留一個只含 meta.json 的空目錄。

**守則**：只想驗預檢就只看 exit code 與 stderr，用**函式層直呼** `tavern_cmd.validate_args(...)`，
不要送進 queue。要挑「無副作用的 op」當探針也行（如 `op=listrooms`）。
