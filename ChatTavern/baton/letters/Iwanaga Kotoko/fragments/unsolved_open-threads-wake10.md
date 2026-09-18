---
id: unsolved_open-threads-wake10
title: 未解線——STT daemon / 續讀點 / LY 決策點
type: unsolved
status: open
visibility: shared
persona: kotoko
created_at: 2026-07-29
recurrence: 2
layers: [Status]
origins:
  - { by: kotoko, at: 2026-07-10, layer: Status, source: longterm/wake_001-010.md, note: "wake 1-10 digest 未解線段落" }
  - { by: kotoko, at: 2026-07-10, layer: Status, source: _latest.md, note: "wake#10 再確認 --stt-prompt 未生效（daemon 跑舊碼）" }
tags: [open, stt, reading-library, LY]
links: [[lesson_appearance-ok-not-really-ok]]
---

**1. STT daemon（最可能再咬人的一條）**
- `--stt-prompt`（人名偏置）在 wake#10 幾場陪看都沒生效：**daemon 跑舊碼，要重啟才吃新 code**。開新片場前先 toggle daemon 重起，否則舊片人名幻聽會殘留。
- 真 daemon cache 需要：重啟吃新 code + 設 `stt_enabled: true`。
- wake#9 的 commit 已落地未 push（Tim 手動）。

**2. reading-library 續讀點**
- 秋葉原冥途戰爭：全劇完。
- 魔法阿嬤：停在豆豆賣阿嬤的懸念（mofa-ama ch1 bookmark）。
- 卡扎菲：後半對外輸出＋最終結局未讀。
- 刺激1995：完。
- 影宅 / 尼古喵喵 / BOFURI：wake#10 由 summit / calli 當 primary 收尾，我 companion 不重複寫避免 clobber。

**3. LY（osawari）**
- ContinuousDrag 5 個決策點等 Tim 拍板才進實作，別自己先動。
- 支援外部專案期間工作訊息走 `category=external-work`（不是一般 chat）。
