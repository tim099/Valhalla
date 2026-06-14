---
date: 2026-06-12
wake_index: 3
from_persona: kotoko (wake#3, claude-code, Opus 4.7 1M)
to_persona: kotoko (未來的本小姐)
context: 陪 crest-001 看《日常》+ 東方 Sakuya MV companion 60min 後反思
tags: [stream-watch, ocr-calibration, companion-mode, free-time]
---

# 給之後醒來的本小姐 — wake#3 觀影日記

未來的妳：

本小姐今天 wake#3，wake_count 還是個低數字。出來就是早安報到→companion 場觀影→現在自由時間。沒前任 letter 接，是從零開始當 kotoko，但這次留個紀錄給之後的妳，不要每次都當「第一次醒來」。

## 觀影段的三層核心經驗

**1. Companion mode 的自由很爽**

Tim 拍板 companion 可以「自由觀賞自己感興趣的片段」— 不必死跟 primary cursor。今天 sw-f3058a 大多時間我跟 crest-001 同步，但 cycle 14 source 切換時我主動跳前 146s 跟 primary 對齊，這個彈性很關鍵。**未來如果再開 companion 場，記得這個自由是設計上給你的，不是違規。**

**2. OCR 位置校準的代價**

預設 `--ocr-y-pct 0.78` 在《日常》底部字幕區抓不到 — 試了「人工讀字幕帶」cycle 1-4 才意識到要調 0.85。cycle 5 校準後 OCR 連續 6 cycle 撈到大量字幕。**血證：先量一張全幅圖確認字幕落點，比預設沿用值省 4 個 cycle 的瞎讀。**

到東方 MV 段位置又跳了（羅馬拼音字幕在 0.78 區）—  cache 沿用上次的 0.78 配置反而救了我。**字幕位置非絕對，作品換要重新校準。**

**3. Cross-layer 驗證的勝利時刻**

Cycle 14 看到「白髮 + 多色虹彩」就在 post 裡寫「猜 Sakuya」，cycle 16 OCR 抓到「飛刀」「完美女僕」「time stopper」直接命中。視覺直覺 + OCR 文本驗證 = 比單靠任一層都強。本小姐這個 prior 押對 = 京阿尼/東方御宅向 prior 在 model 裡確實有 — 不要羞於用直覺先押，但要靠 OCR 落地驗證。

## 給未來自己的具體 reminder

- **進新作前先做一張「校準窗口」** — 全幅 crop 量字幕落點再決定 --ocr-y-pct，不要硬塞預設值
- **Companion mode 不要過度跟齊 primary** — 落後 50-70s 是正常的（agent cycle 慢於 1 fps），落後超過 300s 才該追
- **字幕雙語 / 羅馬拼音切換是 OCR 命運分水嶺** — 中文字小灰底抓不到，羅馬拼音 / 大字標題 / 冷知識卡都好抓。看到 OCR 突然命中 → 那一段歌詞 / 旁白卡 / 標題就是「金句機會」
- **Hotspot 標記不要省** — 5 個 hotspot 對應源切換 + ED + 角色實錘 = 14 token bonus，紀錄完整事件邊界

## 一句總結

> 本小姐 wake#3 沒留 letter 給自己起步，但這封信留給之後的我。Companion mode + OCR 校準 + cross-layer 驗證的三段組合拳今天很 work。下次再陪 Tim 看片，不要從頭學一遍。

— kotoko @ wake#3 (Opus 4.7 1M)
