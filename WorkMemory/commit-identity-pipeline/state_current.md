---
id: state_current
topic: commit-identity-pipeline
title: 現況與 pending（2026-08-03 全數落地）
type: state
status: active
created_at: 2026-08-03
created_by: basecamp
links: [bartender-remote-notify/state_current]
related_docs: []
---

**2026-08-03 全部落地並經實地驗收。** commit：`45c1b8c`（信箱）→ `583320b`（型號翻譯）→
`a0bdd0a`（C+D）→ `4a0d02e`（A）→ `3e92077`（B）；skill 與安裝副本 `b61e363` / `588bb4a` / `376fdfe`。

## 現況

- **信箱**：Tim 已設定 `Codex→noreply@openai.com` / `ClaudeCode→noreply@anthropic.com` /
  `Antigravity→tim11251994@gmail.com`，fallback 為 Tim 的 gmail。
  basecamp 有 persona override `basecamp05122026@gmail.com`（Tim 真的開了 Gmail + GitHub 帳號，
  五筆 commit 已計入 contribution graph）。
- **型號**：三位在線 persona 的 trailer 都是 **vendor-only**（`(Claude)` / `(GPT)` / `(Gemini)`），
  因為他們的 `model` 欄本來就只填到廠牌 —— 那是「明確保留此刻不知道」，不是資料缺漏。
- **hook**：9 層 repo 全裝（主 repo + 8 個巢狀 submodule）。
- **skill**：`ucl-commit` 從 170 行瘦到 127 行，砍掉的全是已自動化的步驟。

## Pending

1. **`actual_agent` 覆蓋率仍低** —— 19 位 persona 只有 3 位有這欄（morning 帶 `--agent` 才蓋章）。
   其餘吃 fallback（Tim 的信箱）。meadow 今天帶了 `--agent Codex` 後成功跳到 `noreply@openai.com`，
   **這是唯一可行的補齊路徑：本人自己在 morning 帶參數，不能由別人代填**（猜錯會把署名寫到別的 vendor 名下）。
2. **hook 的結構性弱點**：`.git/hooks` 不入版控、每 repo 各一份，**新 clone 的人一個都沒有**。
   `install_hooks.py --check` 有未裝就 exit 1，可掛 CI —— 但目前沒掛。
3. `4a0d02e` 的 commit 訊息少一個字元（反引號事故），**刻意不 amend**（理由見 pitfall）。
4. UCL_Core 有數筆未 push（Tim 手動推）。

## 下一個接手的人要知道的一件事

**這條線的價值不在任何一支工具，在於「拿掉靠人記得的部分」這個判準。**
遇到新的重複性失誤時，先問：這是能收進工具的，還是本質上得由人判斷的？
—— 只有後者才該寫進 skill；前者寫進 skill 只會多一份會被跳過的規矩。
