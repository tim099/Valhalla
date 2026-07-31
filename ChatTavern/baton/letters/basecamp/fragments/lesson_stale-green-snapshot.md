---
id: lesson_stale-green-snapshot
title: 舊快照假綠 — 綠燈不是謊言，只是過期了
type: lesson
status: open
visibility: shared
persona: basecamp
created_at: 2026-07-28
recurrence: 4
layers: [Status]
origins:
  - { by: basecamp, at: 2026-07-19, layer: Status, source: 20260720T055700Z.md, note: "一夜三咬：check_compile 舊快照 / 牆鐘門檻空轉 / JsonLib 假 false" }
  - { by: basecamp, at: 2026-07-27, layer: Status, source: 20260726T114016Z.md, note: "check_compile 回 0 error 但 timestamp 早於改動 4 小時" }
tags: [cross-layer-verification, verification]
links: [lesson_appearance-ok-not-really-ok]
---
**症狀**：驗證工具回綠，但那個綠是舊的——它沒說謊，只是回答了一個過去的問題。

**解法三件套**：① **錨定 baseline 等變化**（先記 mtime/版本，再等它前進，而不是直接讀值）；② **行為驗證優先**（讓新功能真的跑一次看行為，而不是看狀態檔）；③ **雙層對時**（比對產物時間 vs 改動時間，早於改動就是舊的）。

**現成招式**：Unity 端用 run_cmd recompile 強制刷新後再讀；程式路徑用「新參數是否真的生效」當行為證據。
