# StreamWatch step=peek owner=_peek  ts=`2026-08-15 19:56:27+08:00`（本地時間）

> **這不是一場觀影** —— 不開 session／不記帳／不發酒館／不動任何進行中的場次。

## 看到什麼
- 縮圖牆   : `D:/Unity/Bar/AgentCommands\_screenstream\_montage_peek__peek.jpg`　← 直接 Read
- 字幕     : `D:/Unity/Bar/AgentCommands\_screenstream\_montage_peek__peek.subtitles.md`　← 直接 Read（**這次產出**，mtime 已驗）
- 錄影中   : 是
- 涵蓋     : 19:55:28 → 19:55:40  (12s, 13 frames)（要求窗口：最近 60s）
- 格數     : 13　**每格 ≈1s**
- 保存期   : 2400s（2400 frames / 1 fps —— **讀自 _config.json，不寫死**）
- 感官     : OCR 開／STT 開（讀自 _config.json）
- STT      : 5 段 (cache-only, 命中 1 chunk) → 接入 sidecar
- 窗口對帳 : 窗口尾端 19:55:40 ≤ 水位 19:55:41 ✅（夾子生效，餘裕 1s）
　　　　　　 （水位來源：OCR 19:56:27／STT 19:55:41）

## next
- 這是一次性的一眼；**沒有下一步**，也沒有進度可接。要正式看請開場：
  run_cmd.py run StreamWatch --arg step=start --arg persona=<P> --arg until=<HH:mm> --arg media=<work>
