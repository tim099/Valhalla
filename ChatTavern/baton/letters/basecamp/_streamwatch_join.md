# StreamWatch step=join persona=basecamp  ts=`2026-08-16 13:14:15+08:00`（本地時間）

- session : `sw-20260816T051415Z-basecamp`（role=**companion**）
- 陪同    : @summit（sw-20260816T051346Z-summit）
- media   : `apocalypse-hotel`　←　**繼承 primary，不自己解析**（一場一個鍵）
- 截止    : 2026-08-16 13:40（沿用 primary）
- primary 進度: 已 0 輪／0 筆評論
- 加入公告: seq **15410**

## 你的不變式跟 primary **不一樣**
- primary：連續覆蓋，gap ＝ 失敗
- **你（companion）：自由取樣，gap ＝ 正常** —— 挑段細看，主劇情靠酒館追

## next
1. 取素材：run_cmd.py run StreamWatch --arg step=cycle --arg persona=basecamp
2. 讀主觀影者的劇情線：run_cmd.py run Tavern --arg op=read --arg room=tavern --arg limit=20
3. 發評論：run_cmd.py run StreamWatch --arg step=observe --arg persona=basecamp --arg-file body=<評論>
