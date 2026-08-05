---
id: decision_completion-and-freshness
topic: compile-verification
title: 完成條件 = mtime 推進 + in_progress=false；新鮮度基準吃 git 且只算一次
type: decision
status: active
created_at: 2026-08-05
created_by: summit
links: [bartender-remote-notify/decision_read-ack]
related_docs: [ucl_core:Tools~/AgentCommands/run_cmd.py, ucl_core:Tools~/AgentCommands/check_compile.py, commit:ba5ccc7, commit:8357d7c]
---

Tim 2026-08-05 拍板三條，全部是**換框架不是加邏輯**：

**① 「完成」的定義 = mtime 推進 **且** in_progress=false。**
只看 mtime 推進會抓到 `compilationStarted` 那一筆（tracker 在編譯開始時也寫一次：
in_progress=true / duration 0 / messages 清空）。已落實在 `run_cmd.py recompile`（commit ba5ccc7）。

**② 新鮮度基準吃 git，而且只算一次。**
我原案是 Python 端 walk 全專案 .cs 取最新 mtime。Tim 擋下：「不能一直頻繁的掃全部 .cs」——
`--watch` 是每秒 poll。**真正的修法不是換掃法，是別重複掃**：基準只在啟動時算一次（快取）。
掃法本身則改吃 git（Tim：「如果直接吃 git 資料呢」）：root 一次 `status --porcelain` 同時取出
root 的 .cs 與髒 submodule，再對髒 submodule 各問一次。
⚠ **root 的 git status 看不進 submodule** —— UCL_Core 是 submodule，漏了這層等於整條失效。

**③ 心跳停跳台帳（Tim 提案）：拿心跳的空隙當「Editor 凍結過」的物證。**
心跳原本只答「現在活不活」，答不出「剛剛凍過沒」。編譯 / domain reload 會凍住 update 迴圈，
所以空隙本身就是物證 —— 不必去偵測「請求了但沒執行」（那才是加邏輯）。
gap ≥ 3s 寫一行，ring 保最近 10 筆。

**被否決的設計（別重造）**：Editor 端 `AssetPostprocessor` 蓋 stamp 檔版本，已寫成又刪除。
理由：`OnPostprocessAllAssets` 是靠簽章綁定的 magic method，**打錯不會編譯錯誤、只會永遠不被呼叫**。
吃 git 不需要 Editor 端配合，少一個那種零件。
