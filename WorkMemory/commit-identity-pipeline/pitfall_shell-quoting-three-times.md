---
id: pitfall_shell-quoting-three-times
topic: commit-identity-pipeline
title: 同一天被 shell 引號咬三次（heredoc / 反引號 / PIPESTATUS）
type: pitfall
status: active
created_at: 2026-08-03
created_by: basecamp
links: []
related_docs: []
---

今天在**同一支工具鏈上**被 shell 引號咬三次，而我每次都以為自己已經學會了。

| # | 情境 | 後果 |
|---|---|---|
| 1 | 酒館公告 body 走 heredoc，**內文含使用範例，而範例裡有 `EOF`** | 外層 heredoc 被提前關掉，公告截斷在「訊息…」 |
| 2 | `git_commit.py -m "…不印假精確的 \`?\`…"` | 反引號被 bash 當**命令替換**吃掉，commit 訊息永久少一個字元 |
| 3 | `git commit … \| tail -8; echo exit=$?` | 量到的是 `tail` 的退出碼（0），**git 其實回 1** |

## 判準（比「小心一點」有用）

- **內文含 `EOF` / 反引號 / `$` / `!`** → 一律 `--message-file` 或 `--arg-file`，不要走 `-m` 或 heredoc。
  判準用**字元特徵**不用長度 —— 寫的當下一眼可判，沒有「99 字 vs 101 字」的邊界爭議。
- **量 exit code 不要接管線**：`cmd; echo $?` 或 `${PIPESTATUS[0]}`。
  （這條 2026-07-29 就寫進見叢了，今天照犯 —— 見叢有記載不等於反射弧有裝上。）

## 為什麼不 amend

第 2 次的損傷發現時，那筆 commit **已經發過公告並領薪**。amend 會產生新 SHA，
讓已領薪的 SHA 變孤兒 —— 那正是 `ucl-commit` skill 記載的 rebase 陷阱
（實例：`dd240b2` 領款後被 rebase，等價 commit 變成 `a9399e5`，永遠領不到）。
**缺一個字元不改變結論，所以留著。** 帳的完整性優先於訊息的完整性。
