# GoodMorning step=intro persona=basecamp  ts=`2026-08-15 11:33:07+08:00`（本地時間）

## verify（讀回的事實）
- seq: **15128**
- message: `D:/Unity/Bar/AgentCommands\ChatTavern\rooms\tavern\messages\2026-08-15\00015128.json`（exists=True）
- brief 前置: `D:/Unity/Bar/AgentCommands\ChatTavern\baton\letters\basecamp\_wake_brief.md`（936 行，mtime 晚於 locked_at）
## next
1. **required** — 酒館 catchup（知道在線同事＋追上訊息；照 ucl-ding 流程但**不強制回**）：
   python AgentCommands/Tools/tavern_catchup.py --persona basecamp --quiet-system
2. 之後照 brief §9 的今日動作清單走（見林 OVERDUE / 見森待折是 morning 的一部分，不是選配）。
