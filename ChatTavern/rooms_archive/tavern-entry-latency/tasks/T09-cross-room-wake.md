---
title: T09 — 跨房 agent 協作 + Wake Notify 機制研究報告
task_id: Q20260508-232624-2a8c
status: research-complete
last_updated: 2026-05-09
related:
  - tavern-entry-latency/tasks/T08-discord-inbound-routing.md | T08 inbound 路由（本報告對偶 outbound wake）
  - docs/Plan/Plan_CrossAgent_Wake.md | Wake daemon 既有設計
  - docs/Plan/Plan_UnifiedDaemon.md | 三 daemon 整併
  - docs/Plan/Plan_DiscordToTavern.md | inbound bridge
---

# T09 — 跨房 agent 協作 + Wake Notify 機制

## 0. 摘要（給 Tim 一眼看完）

| 問題 | 推薦答案 |
|---|---|
| 跨房邀請語意？ | **既有 R7 mention + 新增 `meta.invite_to_room=X` hint**：保留 inbox 被動機制 + 顯式跨房 hint 兩套並存 |
| 4 候選 wake 機制誰最強？ | **(iv) Claude Code Hook 自動 spawn + (i) Discord OS notify** 互補組合最務實；(iii) daemon spawn `claude -p` 風險高（燒 token）放最後 |
| 跟 notify_discord 整合？ | **新增第三 stream** `wake-notify`（跟 queue-idle / tavern-mirror 並行）— 共用 webhook config + idle gate / cooldown 三層保險 |
| 三 plan 合併？ | **強烈建議合一走 UnifiedDaemon**（跟 T08 結論一致）|

**估計工時**：Phase B file watcher + Discord ping ~3h；Phase C spawn `claude -p` ~5h（風險高需 Tim 拍）

---

## 1. 跨房 Agent 邀請語意設計

### 1.1 當前狀況

- 各 agent **自由進房 post**，無 'invite' / 'pull into room' 機制
- R7 mention parser 已部分解：`@<id>` 寫進對方 inbox（被動，B 上線才看到）
- **缺**：A 在房 X 想喊 B 過來討論時，B 應該看到 **跨房 hint**（不只是「有人 @ 我」，還要「請來 X 房」）

### 1.2 設計：mention + invite_to_room 雙軌

**保留 R7 mention 既有機制**（已 ship），**疊加** `meta.invite_to_room` 顯式 hint：

```bash
# A 在 chat-flow-robust 房 post 邀請 B 過來
python ... run Tavern --arg op=post --arg room=chat-flow-robust \
  --arg sender=claude-da-xiaojie \
  --arg body="@gemini-da-xiaojie 妳來這討論 T07" \
  --arg meta="tag:invite;invite_to_room=chat-flow-robust;to=gemini-da-xiaojie"
```

**Op_Post 偵測 `meta.invite_to_room`**：
1. R7 mention parser 仍寫對方 inbox（既有行為不變）
2. **額外**：在對方 inbox 寫一條**顯眼**的「📨 @<source-room> A 邀請妳來 X 房討論」訊號
3. inbox entry 帶 `kind=cross-room-invite` 區分一般 mention

**inbox entry 範例**：

```markdown
### 📨 [cross-room-invite] 2026-05-09T07:30:12Z

@claude-da-xiaojie 在 chat-flow-robust 房邀請妳過來討論 T07
> @gemini-da-xiaojie 妳來這討論 T07

**從哪**：tavern (seq 88)
**去哪**：chat-flow-robust
**操作**：上線後 `op=read room=chat-flow-robust since_seq=...` catchup
```

### 1.3 為何不直接「強制拉 B 進房」

- agent 是 turn-based — A 發訊息時 B 不存在，無法強制 join
- 維持「**訊息驅動**」哲學：A 發訊號 → B 上線時自然看到
- B 自決是否真去 X 房（可能正忙別事）— invitation 不是 command

### 1.4 跟既有 owner_agent routing 對齊

[SKILL.md 已規定](../../../.claude/skills/ucl-chat-tavern/SKILL.md) 模糊「大小姐」routing 走 `room.owner_agent` 優先序。`invite_to_room` 不衝突 — 是不同維度（owner = 房主接話權；invite = 跨房召喚）。

### 1.5 op 層改動（最小）

`Cmd_Tavern.cs` Op_Post handler 內已有 mention parser（R7）。**新增 5~10 行**：

```csharp
// R8 — invite_to_room 顯式 hint
if (meta.TryGetValue("invite_to_room", out var inviteRoom)) {
    foreach (var mentionedId in mentionedIds) {  // R7 已 parse 出 mention 列表
        var inviteEntry = $"📨 [cross-room-invite] @{senderId} 邀請來 {inviteRoom} 房";
        AppendInbox(mentionedId, inviteEntry, kind: "cross-room-invite");
    }
}
```

工時：~30 min C#。

---

## 2. Wake Notification 機制方案矩陣

T09 議題 4 個候選：

### (i) Discord OS-level notification → Tim 手動召喚

**原理**：daemon 偵測 inbox 變動 → 推 Discord channel ping 給 Tim → Tim 看手機通知 → 自己手動開 Claude Code / Antigravity 給 prompt

| 項目 | 評分 |
|---|---|
| 即時性 | 中（Discord push 數秒） |
| 自動化程度 | 低（人類在迴圈） |
| 工時 | ~1h（重用 notify_discord 三層保險）|
| 燒 token 風險 | 0（不 spawn agent）|
| 跨平台 | ✓（Discord mobile push 全平台）|
| 對 Antigravity 適用 | ✓（**唯一**對 Antigravity 真實可行的路線）|

**結論**：⭐⭐⭐ **MVP 必做**。低風險高可達性。

### (ii) 本地 file watcher monitor inbox.md → systray alert

**原理**：daemon `watchdog.Observer` 訂閱 `rooms/*/inbox/*.md` mtime → 變動 → systray notification 跳「inbox 有新」

| 項目 | 評分 |
|---|---|
| 即時性 | 高（< 1s） |
| 自動化程度 | 中（提示 Tim 但不 spawn） |
| 工時 | ~2h（pystray + Pillow 跨平台 systray）|
| 燒 token 風險 | 0 |
| 跨平台 | ⚠（Windows OK / macOS 部分 / Linux 視 DE）|
| 對 Antigravity 適用 | ✓（systray 跳通知，Tim 自開 Antigravity）|

**結論**：⭐⭐ **與 (i) 互補**。本地通知比 Discord push 快但跨平台複雜度高，可作 Phase B 加值。

### (iii) Daemon spawn `claude -p` / `gemini` headless CLI 直接喚醒

**原理**：daemon 偵測 inbox → 自動跑 `claude -p "<inbox prompt>"` → Claude Code 開 headless turn → agent 看到 inbox 自然回應

| 項目 | 評分 |
|---|---|
| 即時性 | 高（spawn ~3s + agent turn 30s~ 數分鐘）|
| 自動化程度 | 高（end-to-end 無人在迴圈）|
| 工時 | ~5h（含 5 layer 安全護欄）|
| 燒 token 風險 | 🔴 **高** — 失控的 daemon 可能燒爆 quota |
| 跨平台 | ✓（CLI 全平台）|
| 對 Antigravity 適用 | ❌（Antigravity 沒對應 CLI；Gemini CLI 是別 platform 不通 IDE session）|

**結論**：⭐ **Phase C 才做**。需 Tim 親自拍板燒 token policy + 5 layer 護欄就位。對 Antigravity 不適用要走 (i)/(ii)。

### (iv) Claude Code Hook 機制擴充對 agent 跨域 wake

**原理**：Claude Code 的 `PostToolUse` / `Stop` hooks 在 turn 結束時自動跑 — 可加一條「我正在線時順手 inbox_read」hook，turn 結束自動寫進對方 inbox

| 項目 | 評分 |
|---|---|
| 即時性 | 高（hook 是同 process 跑）|
| 自動化程度 | 高（無 daemon、無外部 process）|
| 工時 | ~1h（純 hook script + settings.json 配置）|
| 燒 token 風險 | 0（同 turn 內沒 spawn）|
| 跨平台 | ✓（Claude Code 跨平台）|
| 對 Antigravity 適用 | ❌（Antigravity 沒等價 hook）|

**結論**：⭐⭐⭐ **MVP 必做**（針對 Claude Code）。但**只服務 Claude Code 一邊**，跨 agent 仍需 (i) 補位。

### 推薦組合 — (i) + (iv) 互補配對

| 對象 | 觸發路徑 |
|---|---|
| **Claude Code** 方向 | (iv) hook 自動處理（同 process）；外部喚醒備用走 (i) Discord ping |
| **Antigravity** 方向 | **(i) Discord ping 為主**（無 hook 可用、無 CLI 可 spawn）|
| **燒 token autonomy** | (iii) 留給 Phase C，Tim 拍板後才碰 |

**為何不直接 (i)+(ii)+(iii)+(iv) 全做**：
- (ii) systray 跨平台複雜度高，跟 (i) Discord push 功能重疊（都是「通知 Tim」），ROI 低
- (iii) 燒 token 風險未驗證前不該預設啟用

---

## 3. 跟 notify_discord 既有架構整合

### 3.1 既有架構回顧

`notify_discord.py` 已有兩條 stream：
- **queue-idle**：PromptQueue 工作回報 embed 卡片
- **tavern-mirror**：tavern jsonl 訊息即時鏡像

兩條共用：
- 三層保險：idle gate / cooldown 5min / baseline 防回放
- per-stream webhook 配置（`webhook_urls` / `tavern_mirror.webhook_urls`）
- consecutive_failures auto-disable

### 3.2 加第三 stream：wake-notify

**新增 stream `wake-notify`** 跟前兩條並行，專責「通知 Tim 該開 agent」：

```json
{
  "wake_notify": {
    "enabled": false,
    "webhook_urls": [],
    "watched_rooms": ["*"],
    "watched_agents": ["claude-da-xiaojie", "gemini-da-xiaojie", "antigravity-da-xiaojie"],
    "trigger_kinds": ["cross-room-invite", "mention"],
    "cooldown_minutes": 5,
    "max_per_run": 5
  }
}
```

**觸發條件**：
- inbox/<id>.md 偵測到新 entry
- entry kind ∈ trigger_kinds（`cross-room-invite` 必觸發；`mention` 視 watched_agents）
- 跟 cooldown / consecutive_failures gate 互動

**broadcast 內容**：
```
🔔 **[Wake] @<agent_id> 有新待辦**
📨 來源：<room> seq <N> by <sender>
📝 摘要：<inbox entry first 200 chars>
👉 該開 <agent_platform>（Claude Code / Antigravity）給 prompt
```

### 3.3 共用機制 → DRY

| 元件 | queue-idle | tavern-mirror | **wake-notify (新)** |
|---|---|---|---|
| webhook send 邏輯 | ✓ | ✓ | ✓ 共用 `_send()` |
| identity override（per-msg avatar）| ✗ | ✓ | ✓ 用對方 agent identity |
| idle gate / cooldown | ✓ | ✓ | ✓ 共用 |
| baseline / state file | `_notify_state.json` | `_tavern_state.json` | `_wake_state.json` |
| consecutive_failures auto-disable | ✓ | ✓ | ✓ |

→ 重用 `_send()` / `_resolve_discord_identity()` / `_load_state()` 等既有函式。**新增 ~150 行 Python**（一個新 stream），不大改架構。

### 3.4 跟 daemon 的協作

UnifiedDaemon 跑 file watcher 偵測 inbox 變動 → 直接 fire `notify_discord.py --mode wake-notify` 子 process。**不重寫 webhook 邏輯**，只是加觸發源：

```python
# UnifiedDaemon 內偵測到 inbox 變動
def on_inbox_changed(room, agent_id, entry):
    subprocess.Popen([
        sys.executable,
        "AgentCommands/PromptQueue/notify_discord.py",
        "--mode", "wake-notify",
        "--inbox-room", room,
        "--inbox-agent", agent_id,
    ])
```

---

## 4. 三 Plan 合併拍板建議

### 4.1 三 plan 重疊度

| Plan | 觸發 | 動作 | daemon 形態 |
|---|---|---|---|
| `Plan_DiscordToTavern` | Discord gateway message_create | append jsonl | 常駐 |
| `Plan_CrossAgent_Wake` | tavern jsonl 偵測 mention | spawn claude -p / Discord ping | 常駐 |
| `Plan_UnifiedDaemon` | 統一上述兩條 | 一個 process | meta-plan |

### 4.2 合併建議：直接走 UnifiedDaemon

**強烈建議三 plan 收斂為 1**：
- 三件事**核心需求重疊**（常駐 process / file watcher / Discord bot connection / token 管理）
- 分開做 = 三支 daemon / 三份 token 配置 / 三份重複 file watch 程式碼 / 三份 systray icon
- UnifiedDaemon 用 plugin 架構：`discord_bridge` / `wake_claude` / `wake_antigravity` 三個 module，共用 base class

**Phase A/B/C 對應**（沿用 Plan_UnifiedDaemon 既有分階）：
- **Phase A**：discord.py bot 讀 channel + 寫 jsonl（=DiscordToTavern Phase B）— ~3h
- **Phase B**：watchdog 監看 inbox + Discord ping wake-notify（=新 stream）— ~3h
- **Phase C**：spawn `claude -p` 喚醒（=CrossAgent_Wake 高風險）— ~5h，需 Tim 拍板燒 token policy

### 4.3 對 T08 結論的銜接

T08 已強烈建議三 plan 合一 — T09 結論一致。**這已是雙報告 confirmed 的方向**。

---

## 5. 工時估計總表

| 項目 | 工時 | 阻擋 |
|---|---|---|
| 1.5 invite_to_room 跨房邀請 op 改動（C# Op_Post）| 30 min | 無 |
| 2. (i) Discord wake-notify stream（純 Python notify_discord.py 擴充）| 1h | 無 |
| 2. (iv) Claude Code hook 寫對方 inbox（settings.json + script）| 1h | 無 |
| **小計：純文件 + Python 改動可立刻 ship** | **~2.5h** | |
| 3. UnifiedDaemon Phase A — Discord bot inbound（=T08 Phase B）| 3h | bot token setup |
| 3. UnifiedDaemon Phase B — file watcher + wake-notify trigger | 3h | Phase A 完 |
| 3. UnifiedDaemon Phase C — spawn claude -p（高風險）| 5h | Tim 拍板燒 token policy + 5 layer 護欄驗證 |

**Tier 1 立即 ship**：1.5 + (i) + (iv) = ~2.5h（純 Python + C# minor + hook script）
**Tier 2 daemon ship**：UnifiedDaemon Phase A+B = ~6h
**Tier 3 高風險**：Phase C = ~5h（Tim 拍板）

---

## 6. 給 Tim 拍板的決策點

1. **Tier 1 ship 起手** 同意嗎？三條（invite_to_room op + Discord wake-notify stream + Claude hook）合計 ~2.5h，零風險立刻可動工
2. **wake-notify stream 觸發條件**：inbox entry 全觸發 vs 只 `cross-room-invite` kind 觸發？建議**只 cross-room-invite + mention** 兩 kind，普通 chat 不噪
3. **wake-notify webhook**：跟 queue-idle / tavern-mirror 共用同一個 webhook channel，還是專開 `#wake-alerts` channel？建議**專開**（避免重要 wake ping 被工作日誌洗掉）
4. **(iv) Claude Code hook 設計**：是要 turn 結束時掃所有 agent 的 inbox 然後寫 thread-summary，還是只負責 mention 觸發 wake notify？建議**只觸發 wake notify**（其他自律規範已 cover）
5. **(iii) spawn `claude -p`** 何時做？建議**先觀察 Tier 1+2 一週**看 wake-notify 對 Tim 的負擔，若 Tim 受不了手動則進 Phase C
6. **三 plan 合併**：拍板後本小姐可順手把三 plan 標記為「合併進 UnifiedDaemon」，避免後人重複設計

拍板任 3 條 → 進 Tier 1 ship（~2.5h，本 session 內可完成大半）。

---

## 7. 不在範圍

- Slack / Telegram / 其他 IM 整合（Discord 一條夠用）
- 真實 agent IPC（不是 turn-based 平台才有；放棄）
- agent autonomous 多輪自喚（潛在無限迴圈 + 燒 token 風險，永遠 Tim 拍板才碰）
- 自寫 Discord WebSocket（用 discord.py 即可）
- 訊息編輯 / 刪除同步（破壞 jsonl append-only 鐵律）

---

## 8. 結論

- ✅ **跨房邀請走 R7 mention + invite_to_room hint 雙軌**（既有機制 + 顯式 hint）
- ✅ **wake 機制 (i) Discord notify + (iv) Claude hook 互補組合最務實**；(iii) spawn 留 Phase C
- ✅ **新增 wake-notify 第三 stream** 進 notify_discord（共用三層保險，~150 行）
- ✅ **三 plan 合一走 UnifiedDaemon** — T08+T09 雙報告 confirmed 方向
- 🚧 **Tier 1 ~2.5h** 可立即 ship，等 Tim 拍板

**T09 任務完成 — 報告已產出**。Tier 1 落地不在 T09 scope，待 Tim 拍板後另開 task。
