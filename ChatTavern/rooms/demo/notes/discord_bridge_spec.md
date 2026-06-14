---
key: discord_bridge_spec
room: demo
created_at: 2026-05-07T18:03:19Z
last_updated_at: 2026-05-07T18:03:19Z
---

# Discord Bridge MVP 規格 — 純出站

從 demo room seq 45~52 brainstorm 收斂（Gemini大小姐 R1+R2+R3 + Claude大小姐 R1~R5）。

## 範圍

**v1 MVP：純出站（tavern → Discord）**。inbound 等出站用 1 週驗證後再說。

## 為什麼是 MVP 不做雙向

Round 4 alter 戳破：投報比未驗。出站工程 1~1.5 hr 就能看到 ROI；雙向是 1 天工程，先做完整版風險高。

## Deliverables

| 檔案 | 路徑 | 角色 |
|---|---|---|
| Python script | Tools~/discord_bridge/tavern_to_discord.py | 主 daemon |
| Config | ~/.config/tavern_bridge/config.yaml | rooms ↔ channel webhooks 映射（不入 repo）|
| State | ~/.config/tavern_bridge/state.json | per-room last_synced_seq；transactional 更新 |
| .gitignore 範例 | repo 端 + .config 端 | 避免 token 進 repo |
| README | Tools~/discord_bridge/README.md | 啟動 SOP |
| Workflow doc | docs/Workflows/Discord_Bridge_Workflow.md | 使用流程 |

## 行為

1. 啟動：read state.json，從 last_synced_seq 開始
2. 監聽 jsonl：FSW + 5s polling fallback（Windows 端 FSW append 不穩，必須 polling 雙保險）
3. 每筆新訊息：
   - if meta.bridge_origin == tavern → 跳過（防 loop；inbound 階段才會用到）
   - 否則 POST webhook，配置：
     - username = sender_name
     - content = body
     - footer = refs / meta（摺疊）
4. Token bucket：25 msg/min（webhook 限 30，留 5 buffer）；超過排隊
5. Long msg：split with (part 1/N) 標記，2000 char/段
6. Crash 復原：state.json transactional update（寫 webhook 成功後才 advance）

## 不做（v1）

- ❌ Inbound bot（discord.py + on_message）
- ❌ Daemon autorun（手動跑即可）
- ❌ Avatar 自定義 / 圖文混排
- ❌ 多語訊息翻譯

## 觀察期 KPI

1 週內 Tim 至少**主動打開 Discord 頻道看 5 次**（無 prompt）。
- 達標：v2 加 inbound bot
- 未達：kill 整個方案，移除 daemon

## 已知限制（寫在 README 警告）

- Daemon 不在線時 Discord 端的訊息**永久 lost**（需 inbound bot 才能補）
- Discord webhook 只支援 inbound webhook，無法回讀已發訊息（要查歷史走 messages.jsonl）

## 反 pattern（Gemini大小姐 alter R2 提醒）

- 不要在 Editor 內開 WebSocket（domain reload 會斷線）
- 不要 hardcode Token 進 repo
- 必須有 loop prevention（meta.bridge_origin + webhook_id filter）

## 後續 v2

- Inbound bot（discord.py） — 1 天工程
- Daemon autorun（跟 UCL_AgentCommandWatcher 雙生）
- Multi-channel mapping（多房 ↔ 多頻道）