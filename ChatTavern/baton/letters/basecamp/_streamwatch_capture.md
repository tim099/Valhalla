# StreamWatch step=capture persona=basecamp  ts=`2026-08-16 23:42:38+08:00`（本地時間）

## 結果（讀回的事實）
- 已經是「錄影中」—— 未動作（`enabled` 讀值 true）
- 回讀   : `D:/Unity/Bar/AgentCommands\_screenstream\_config.json` enabled=true　←　**寫完再讀一次，不是看回傳值**
- 保存期   : 名目 2400s（2400 frames / 1 fps，**讀自後台設定不寫死**）｜實有 5212s（2400 張，最舊 22:15:47）

## next
1. 看一眼：run_cmd.py run StreamWatch --arg step=peek --arg seconds=60
2. 正式開場：run_cmd.py run StreamWatch --arg step=start --arg persona=basecamp --arg until=<HH:mm> --arg media=<work>
