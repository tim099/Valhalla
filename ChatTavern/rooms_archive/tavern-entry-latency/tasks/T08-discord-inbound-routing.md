---
title: T08 — Discord → 本地酒館 inbound 路由策略研究報告
task_id: Q20260508-232559-c021
status: research-complete
last_updated: 2026-05-09
related:
  - docs/Plan/Plan_DiscordToTavern.md | 完整 Bot 路線設計（既存）
  - docs/Plan/Plan_CrossAgent_Wake.md | 跨 agent 喚醒 daemon
  - docs/Plan/Plan_UnifiedDaemon.md | 三 daemon 整併
---

# T08 — Discord Inbound 路由策略研究

## 0. 摘要（給 Tim 一眼看完）

| 問題 | 推薦答案 |
|---|---|
| 統一 channel vs 每 webhook 一個 channel？ | **每 channel 對應一個本地房（一對一）+ 用既有 outbound mirror_kinds 機制做 channel→room 對偶 mapping** |
| 走 Bot 還是 Webhook Receive？ | **走 Bot（discord.py gateway）** — Webhook 設計即出站，反向不可行 |
| Author → identities mapping？ | **mapping table** — `discord_user_id → tavern_sender_id`，未對應 fallback `discord:<id>` |
| 防 echo loop？ | **三層**：author.bot filter / webhook_id 比對 / `meta.source=discord` 標記 + outbound exclude |

**估計工時**：Phase B prototype ~3h（discord.py 最小 daemon 1 channel 1 room）；Phase C 整合 Wake / UnifiedDaemon ~1day。

---

## 1. 路由策略：統一 channel vs 每 channel 一個房

T08 議題核心問題。兩條路線對比：

### 方案 a — 統一單一 inbound channel

```
Discord #tavern-inbound channel  →  本地 tavern 房（單一）
```

**優點**：
- config 最簡，daemon 內 hard-code 即可
- Tim 在手機上不必想「這條訊息要丟哪 channel」— 只有一個入口

**缺點**：
- 失去 outbound mirror_kinds 對應的對偶結構（outbound 已支援 per-room mirror，inbound 卻只有單入口）
- 多 quest 房深聊時 Tim 想跨房留言只能進 tavern 然後 mention 房名 — 失去 channel 視覺隔離
- 跟既有 `notify_config.json` 的 `tavern_mirror.rooms` per-room mapping 不對稱

### 方案 b — Per-channel 對應一個本地房（推薦）

```
Discord #tavern        →  tavern 房
Discord #chat-flow     →  chat-flow-robust 房
Discord #latency-quest →  tavern-entry-latency 房
Discord #other         →  ignored (default_room=null)
```

**優點**：
- 對稱 outbound — outbound `tavern_mirror.rooms` 已是 per-room watch list，inbound 用同款 mapping 結構即可
- Tim 在哪 channel 留言就進哪房，視覺直覺
- 多 quest 並行時各 channel 互不污染對話流
- daemon config 可動態加 mapping，新 quest 房不必改 code

**缺點**：
- 要維護 channel↔room mapping config（但 outbound 也要，整體成本 amortize）
- Tim 手機上要記得「這條留言要進哪 channel」— 但這就跟 Discord 平時用法一致

### 推薦：方案 b（一對一 per-channel）

**主理由**：跟既有 outbound 架構**對偶對齊**。outbound `tavern_mirror.rooms` 已 per-room watch；inbound 走同款 `channel_mappings` 自然 symmetric。

**實作建議**：
- daemon config `bridge_config.json` 加：
  ```json
  {
    "channel_mappings": [
      { "discord_channel_id": "...", "tavern_room": "tavern" },
      { "discord_channel_id": "...", "tavern_room": "chat-flow-robust" }
    ],
    "default_room_for_unmapped": null
  }
  ```
- `default_room_for_unmapped: null` 預設**忽略**未 mapping channel（避免 DM / 私訊 / 不相干 channel 噪音進來）
- 想要 fallback「未對應 → 進 tavern」的話設 `default_room_for_unmapped: "tavern"`，但**不推薦**（噪音風險）

### 混合選項：群組 channel 多對一

少數場景可允許多 Discord channel → 同一 tavern 房（例：`#discussion-A` + `#discussion-B` 都進 tavern），訊息加 `[from #channel-name]` prefix 標來源。Phase D 才考慮，MVP 不做。

---

## 2. 訊息來源辨識：Bot vs Webhook Receive vs Polling

| 方式 | 即時性 | 依賴 | 複雜度 | 結論 |
|---|---|---|---|---|
| **Discord Bot（gateway WebSocket）** | 毫秒級 | discord.py（~2MB） | 中 | ✅ **推薦** |
| Polling Discord REST API | 60s+ | 純 stdlib（urllib） | 低 | 🟡 備用（即時性不重要） |
| Webhook Receive | — | — | — | ❌ **不可行**（webhook 設計即 outbound） |
| IFTTT / Zapier 中介 | 數秒~分鐘 | 第三方 + ngrok tunnel | 高 | ❌ 不主推 |

### 為何 Bot 才是真路線

T08 提的「Webhook Receive」是常見誤解 — Discord Webhook 概念是「**外部對 Discord channel 的入站接口**」，**單向**。要從 Discord 拉訊息出來必須走：
- **Bot account + Gateway WebSocket**（subscribe message_create event）
- 或 **Bot account + REST API polling**（每 N 秒 GET channel messages）

兩者都需要 bot account（不是 webhook account）。Bot setup 流程見 [Plan_DiscordToTavern §4.1](../../../docs/Plan/Plan_DiscordToTavern.md)。

### Privileged Intent 必須開

`MESSAGE CONTENT INTENT` — Discord 強制；不開 bot 收到的 message body 永遠空。setup 5 分鐘流程一定要勾。

---

## 3. Author → Tavern identities 對應

選 mapping table（既有 plan §4.3 選項 3）：

```json
// bridge_config.json 內
{
  "user_mappings": {
    "<tim_discord_user_id>": "Tim",
    "<other_user_discord_id>": "<some_id>"
  },
  "fallback_pattern": "discord:{discord_user_id}"
}
```

**為何不用 Discord username 直接當 sender_id**：username 可改（且 Discord 2023 後改全 server unique handle），用 user_id 才是 stable identifier。

**identities.json 自動 lazy-create**：
- 收到未對應 discord_user_id → 用 `discord:<id>` 為 sender_id
- 自動 append 到 identities.json：`{"id":"discord:<id>","display_name":"<discord username>","kind":"discord-user"}`
- 之後 Tim 在 mapping table 加上 `<discord_id>: Tim` → daemon reload config 後自動切回 `Tim` sender_id（identities.json 內保留 `discord:<id>` 條目作 historic ref）

### Mention 處理

Discord 端 `@<discord_user>` → daemon 偵測 → 轉成 tavern 端 `@<mapped_sender_id>` 寫進 jsonl body
- 走 user_mappings 解出
- 沒對應 → 保留原 Discord mention 文字（不主動寫進 inbox，避免亂飛）

---

## 4. 防 Echo Loop — 三層防護（既有 plan §4.4 沿用）

| 層 | 機制 | 命中條件 |
|---|---|---|
| 1 | Author filter | bot 收到 message 看 `author.bot == True` 或 `author.id == webhook_id` → skip |
| 2 | Webhook ID 偵測 | tavern_mirror webhook 的 `application_id` 寫進 daemon config 的 `ignore_webhook_ids` → match 即 skip |
| 3 | Sender prefix + outbound exclude | bot 寫 jsonl 的 sender_id 永遠以 `discord:` 開頭；outbound `exclude_senders` 加 `discord:*` glob |

**任一層命中即斷迴圈**；任意兩層失效仍安全。MVP 必開三層。

### outbound 端要配合改一條

`notify_discord.py` 的 `tavern_mirror.exclude_senders` 加 glob 支援 `discord:*` — 當前是 exact match。10 行內可改：

```python
def _matches_excluded(sender_id, excludes):
    for pattern in excludes:
        if pattern.endswith("*") and sender_id.startswith(pattern[:-1]):
            return True
        if pattern == sender_id:
            return True
    return False
```

---

## 5. 跟既有 plan 整合建議

三個 plan 高度重疊：

| Plan | 觸發 | 動作 | daemon 形態 |
|---|---|---|---|
| `Plan_DiscordToTavern` | Discord gateway message_create | append jsonl | 常駐 |
| `Plan_CrossAgent_Wake` | tavern jsonl 偵測 @claude | spawn `claude -p` | 常駐 |
| `Plan_UnifiedDaemon` | 統一上述兩條 | 同一 process | meta-plan |

**建議**：
- 直接走 `Plan_UnifiedDaemon` 一個 process — 不要養兩個 daemon
- Discord inbound 是 plugin module，wake 是另一 plugin module
- 共用 config 載入 / pause flag / log 邏輯
- end-to-end：Tim 在 Discord @claude → bot 寫 jsonl → wake plugin 偵測 → spawn `claude -p` 全自動（這正是 T09 wake 議題的關鍵 flow）

→ 建議 Tim 拍板後 **三 plan 收斂為 1**，直接做 UnifiedDaemon。

---

## 6. 工時估計

| Phase | 內容 | 工時 |
|---|---|---|
| A | 文件（本報告 + 既存 Plan）| **已完成** |
| B | discord.py 最小 daemon（1 channel 1 room）+ echo loop 三層防護 + dry-run 驗收 | ~3h |
| C | UnifiedDaemon 整合（plugin 架構 + Wake 模組合併）| ~6h |
| D | 多 channel mapping、attachments、Production 化 | 後續 |

**Phase B 最小依賴**：
- `pip install discord.py`（~2MB）
- `_bot_token.txt` git-ignored（5 min Discord 端 setup）
- `bridge_config.json` 一個 channel mapping
- 同 process 寫 jsonl + recompile trigger（讓 C# Cmd_Tavern 觀察 jsonl mtime 自動 advance _seq.txt）

---

## 7. 給 Tim 拍板的決策點

1. **方案 b 一對一 per-channel** 同意嗎？（vs a 統一 channel）
2. **discord.py 依賴**可接受嗎？或要堅持純 stdlib WebSocket（複雜度 ×3 不划算）
3. **三 plan 合一走 UnifiedDaemon** 同意嗎？建議合
4. **MVP 從哪條 channel 起手**：tavern 房對應某 channel？還是 chat-flow-robust？建議 tavern（最常用）
5. **identities.json 自動 lazy-create** 同意嗎？或要 Tim 顯式維護 mapping
6. **outbound exclude_senders glob 支援**順手改嗎？（10 行 Python，本 task 範圍內或拆 task 都行）

拍板任 3 條 → 進 Phase B prototype（~3h）。

---

## 8. 不在範圍

- Webhook 反向（不可行）
- 訊息編輯 / 刪除同步（破壞 jsonl append-only 鐵律）
- DM 私訊監看（隱私 / 安全；只監看 server channel）
- 即時雙向 typing indicator（agent turn-based 不適用）
- Discord reaction 同步進 jsonl（過度噪音）

---

## 9. 結論

- ✅ **方案 b 一對一 per-channel** — 跟 outbound `tavern_mirror.rooms` 對偶對齊
- ✅ **Bot gateway 路線 + discord.py** — 唯一可行真路線
- ✅ **三層 echo loop 防護** — author / webhook_id / sender_prefix
- ✅ **三 plan 合一走 UnifiedDaemon** — 強烈建議
- 🚧 **Phase B prototype ~3h** — 等 Tim 拍板後動工

**T08 任務完成 — 報告已產出**。Phase B 實作不在 T08 scope 內，待 Tim 拍板後另開 task。
