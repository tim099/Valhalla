# StreamWatch step=capture persona=basecamp  ts=`2026-08-16 12:20:39+08:00`（本地時間）

## 結果（讀回的事實）
- ▶ 已開始錄影（by basecamp）｜`enabled`=true｜`stt_enabled`=true｜已戳 `enabled_changed_at`｜已發酒保公告並要求 daemon 同步
- 回讀   : `D:/Unity/Bar/AgentCommands\_screenstream\_config.json` enabled=true　←　**寫完再讀一次，不是看回傳值**
- 保存期   : 名目 2400s（2400 frames / 1 fps，**讀自後台設定不寫死**）｜實有 46232s（2400 張，最舊 23:30:07）

## next
1. 看一眼：run_cmd.py run StreamWatch --arg step=peek --arg seconds=60
2. 正式開場：run_cmd.py run StreamWatch --arg step=start --arg persona=basecamp --arg until=<HH:mm> --arg media=<work>
