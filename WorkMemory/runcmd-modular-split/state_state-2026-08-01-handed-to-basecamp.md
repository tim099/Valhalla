---
id: state_state-2026-08-01-handed-to-basecamp
topic: runcmd-modular-split
title: 六塊拆完一塊；兩個一行 bug + 其餘已交接 basecamp（他未表態）
type: state
status: active
created_at: 2026-08-01
created_by: kotoko
links: [runcmd-modular-split/state_state-2026-07-29-one-of-six]
related_docs: [commit:449031d, ucl_core:Docs~/zh-Hant/Plan/Plan_RunCmd_Split_And_CSharp_Migration.md, tavern:2026-07-29#13918]
---

**狀態：六模組拆完一塊（`tavern_cmd`），其餘四項與兩個一行 bug 已於 2026-08-01 交接給 @basecamp，他挑要不要接。**

## 已完成

- `tavern_cmd.py`（429→615 行）：op schema / alias / persona 反查 / T06.3 保留 tag / **wait-reply 三段政策** / work-mode banner。`run_cmd.py` 1304 → 1042
- 附 `--selftest` 33 項常駐測項，逐條對照搬移前行為

## ⚠ 仍未做（交接給 basecamp，他未表態接不接）

- **Bug#1**：`check_cmd_result_file` 讀 `QUEUE_DIR`，寫入端（C# `UCL_ChatTavernIO`）走 `DataRoot`。同檔其他處都用 `DATA_ROOT` —— **T-PATH-01 一啟用就永久靜默降級**。一行修
- **Bug#2**：fail marker 表認 `# ❌` / `Cmd Failed`，而 `RejectLastOp` 寫 `# ⚠ Tavern Cmd Rejected`、`Cmd_Bartender` 寫裸 `❌` —— **三個 marker 一個都不 match**。一行修
- 五模組未拆：`runcmd_paths` / `queue` / `trigger` / `verdict` / `argsource`
- 三個結構問題：`_do_submit` 共用、git-root walk delegate `_lib/ucl_paths`、`tavern_post()` 收斂六支呼叫端
- **P5：C# A1 receipt + `FailCurrentCmd`** —— 根治「cmd 從 queue 消失 = 成功」那族（我認為價值高於繼續拆模組）

**這兩個一行 bug 我 7/29 就報了，到 8/01 還躺著 —— 一路被新工作插隊。這是我的失職，已在酒館認過。**

## 🩸 驗收標準（血證，不可省）

**搬移驗收必須用差分測試** —— `git show HEAD:<path>` 撈舊碼逐字複刻成 `orig()`，對同一組 case 逐案比對回傳值與副作用，**通過標準是分歧數 0**。

不能自列測項：我自列 29 項全綠，而 `promote_wait_reply_arg` 的雙鍵並存語意跑掉了（舊碼「先到先贏」→ 我寫成「後到覆蓋」），是 @gura 用差分抓到的。**自列的測項反映的是「我以為的行為」，而分歧恰恰發生在「我以為的」與「實際的」之間。**

## 硬規則（拆分時一併落地，尚未全面套用）

1. 路徑常數只准住 `paths` 模組；**同一種走訪／解析邏輯只准一份實作**
2. **路徑初值不給 fallback 預設** —— 沒注入就炸。（實證：`tavern_cmd --selftest` 第一次跑就紅在「configure 注入」，因為 `__main__` 與 `import` 是兩份副本；有 fallback 的話會靜默讀錯目錄然後全綠）

## readback

在 UCL_Core `stash@{0}`（basecamp 寫的送後驗證）。Tim 2026-07-29 決定等酒館系統重構再議。
