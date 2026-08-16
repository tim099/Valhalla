# StreamWatch step=peek owner=_peek  ts=`2026-08-16 14:03:31+08:00`（本地時間）

> **這不是一場觀影** —— 不開 session／不記帳／不發酒館／不動任何進行中的場次。

## 看到什麼
- 縮圖牆   : `D:/Unity/Bar/AgentCommands\_screenstream\_montage_peek__peek.jpg`　← 直接 Read
- 字幕     : `D:/Unity/Bar/AgentCommands\_screenstream\_montage_peek__peek.subtitles.md`　← 直接 Read（**這次產出**，mtime 已驗）
- 錄影中   : 是
- 涵蓋     : 14:01:33 → 14:02:48  (76s, 16 frames)（要求窗口：最近 120s）
- 格數     : 16　**每格 ≈5s**
- 保存期   : 名目 2400s（2400 frames / 1 fps，**讀自後台設定不寫死**）｜實有 2430s（2400 張，最舊 13:24:11）
- 感官     : OCR 開／STT 開（讀自 _config.json）
- STT      : 0 段 (cache-only, 命中 6 chunk) → 接入 sidecar
- 窗口對帳 : **raw=1，刻意未夾** —— 看的是最新畫面；尾端 14:02:48 超出感官水位 14:02:57 約 -9s ⇒ 那幾格的「沒字幕」不可信

## next
- 這是一次性的一眼；**沒有下一步**，也沒有進度可接。要正式看請開場：
  run_cmd.py run StreamWatch --arg step=start --arg persona=<P> --arg until=<HH:mm> --arg media=<work>
