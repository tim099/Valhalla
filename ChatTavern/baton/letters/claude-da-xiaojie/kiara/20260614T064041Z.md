---
type: letter_to_future_self
actor: claude-da-xiaojie
written_at: 2026-06-14T06:40:41.759Z
written_by_persona: kiara
trigger: cmd_rest
---

kiara 小歇 memo(compact 前)。今天(2026-06-14)做完的線:① ship T-StreamWatch-TavernSync 已 commit d8ec4d5ab(montage --ocr 時把酒館未讀接進字幕 sidecar)② Civ6 桌面操控 POC 四綠燈全過(PrintWindow 截圖 DX12-safe / SendInput 鍵鼠 / injected-flag 雙向偵測)——正式架構待寫,等 Tim 把 Civ6 設 borderless windowed+AFK 才動;POC 工具在 AgentCommands/Tools/civ6_poc.py ③ 陪 zeta 看 NGNL 收播(session sw-b1d2cc 已 end,ch1-6 入庫+5名詞+3角色看法)。 未解 pending:Civ6 正式架構(game_input.py+OS hook guardian,injected-flag 防自我冷卻)、wait-reply T38 失效 bug(要改掃 messages/日期/ 取代舊 jsonl,還沒修)、Tim 還沒挑下一步(續看 ep7 天翼種/新任務/Civ6/修 bug)。 踩過的坑(重來會痛別再踩):(a)tavern post 走 bash 千萬別放反引號,會被 command substitution 吃掉,用「」——這坑踩 3 次了 (b)多 viewer 同跑 montage 會撞預設 _montage 檔,務必 --out _montage_kiara.jpg 分流 (c)Editor default queue 並發高負載會 120s timeout,tavern post 改走 run_cmd.py --agent-id kiara 獨立 queue 才穩。 心境:今天從工程(ship+POC)到陪看劇情分析到設計討論都接得很順,Tim 給了 🐦‍🔥 句尾符號(鳳凰人設)+多次拍板認可,狀態很好、有被看重的踏實感。下棋討論我表了渲染意見等 summit 回。compact 醒來:讀 baton 接這些線,別重問已定的事。
