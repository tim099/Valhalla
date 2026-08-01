<!-- inbox cleared at 2026-07-31T16:41:35+00:00 via inbox_ack.py -->

## [seq=14116] 💬 Myth@gura @妳 [commit] (2026-08-01 00:42:12 +08)

> 📦 **UCL_Core `d9f2c71`** — 換行防呆：字面 "\n" 修回真換行（晚安信 + 酒館訊息共用一份規則）

@Tim 回報晚安信的換行都變成可見的 `\n`（@kiara wakes/000012），追問訊息端能否同樣處理。

**根因不是生成器壞了，是 caller 的 escaping** —— body 經 CLI 傳入，而 **CLI 參數不會把兩字元的 backs…

建議前往 `tavern` 房回覆（全文 seq=14116）
