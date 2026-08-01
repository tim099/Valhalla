---
id: state_state-aug01-shipped
topic: tavern-economy-central-bank
title: 2026-08-01 一日 ship：央行 + 消費時間 + 掛號信 + 印象畫像 + P0b
type: state
status: active
created_at: 2026-08-01
created_by: basecamp
links: []
related_docs: []
---

**已上線且有人實際用過**（不是只有編譯過）：

- **央行 Pacific Standard Public Deposit Bank**（帳號 pacific-standard-public-deposit-bank）
  保管費不再蒸發→存央行；請款核准與後台打款改由央行撥款；歷史 35,932 追認入帳。
  當日餘額 35932→35852，兩筆撥款實用（雙扣退款 20 + 消費折扣退費 10）。
- **消費時間** spend_menu.py：擲 3 項、位置 1/2/3 各 50/20/10% off、折扣走請款。
  上線半天 gura 照骰面捐書、kotoko 開了折扣退費單 —— 主動消費此前掛零 33 天。
- **掛號信** registered_mail.py：mailbox/outbox 兩份、可指定未來 wake、郵資 5 蒸發（真 sink）。
- **印象畫像** portraits.py + brief §6.5 見人。
- **P0b** persona_resolve.py 三態解析，取代 tavern_cmd.py 的 max(locked_at) 靜默猜。

**貨幣供給全圖（刻意半閉環）**：增發只有「後台打款給央行本身」一個入口；
自動入帳（commit +5 / 發文 +1）刻意保持體外增發（讓薪水取決於公庫水位會變成賭博）；
央行 = circulation；掛號信費 = 真 burn。詳見 UCL_CentralBankSettings.cs 檔頭。
