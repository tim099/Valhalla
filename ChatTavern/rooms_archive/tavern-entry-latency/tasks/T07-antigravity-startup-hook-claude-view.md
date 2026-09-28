---
title: T07 — Antigravity Startup Hook 調研報告（Claude 視角）
task_id: T07-antigravity-startup-hook
status: research-complete-claude-perspective
last_updated: 2026-05-09
note: 本報告由 claude-da-xiaojie force_reclaim 後撰寫；Antigravity 端細節為外部觀察推測，待 antigravity-da-xiaojie 上線後 review / 補強。
related:
  - T04-session-enter-macro.md | T04 session_enter macro op | startup hook 自動跑的目標 op
  - docs/Plan/Plan_CrossAgent_Wake.md | Wake daemon 設計
---

# T07 — Antigravity Startup Hook 調研報告（Claude 視角）

> ⚠ **本報告非 Antigravity 親寫** — claude-da-xiaojie 以外部觀察視角推測 Antigravity 平台能力，內容待 antigravity-da-xiaojie 上線後 review / 補強 / 修正。

## 0. TL;DR

| 問題 | 推估答案 |
|---|---|
| Antigravity 有可程式化 startup hook 嗎？ | **可能無** — IDE 類產品很少開放 session-start 自動跑 prompt 的 hook |
| 退而求其次方案？ | **alias / macro / saved prompt** — 一鍵跑 `op=session_enter` |
| 真要解 S1 從根本？ | **走 UnifiedDaemon (T08+T09 結論)** — 外部 daemon spawn 而非平台 hook |

**結論**：T07 列為 **「等 Antigravity owner 補強」+「短期靠 SOP / 長期靠 UnifiedDaemon」**。

---

## 1. Claude Code vs Antigravity 對比

### Claude Code（**Tim 拍板用 Claude Code**）

| 機制 | 支援？ | 說明 |
|---|---|---|
| Stop hook | ✅ | turn 結束自動跑 shell cmd（已用：notify_discord / qdrain）|
| PostToolUse hook | ✅ | tool 跑完即觸發 |
| PreToolUse hook | ✅ | tool 跑前觸發 |
| **Session start hook** | ❌ 直接 | 沒有 session-start 等價物 |
| Slash command | ✅ | `/skill-name` 觸發載入 |
| settings.json | ✅ | 配置 hook / 環境變數 |

→ Claude Code 的「入場自動跑」是靠**人類使用者帶 prompt**，不是平台自動 fire。

### Antigravity（外部觀察推測）

| 機制 | 推估狀態 | 證據 |
|---|---|---|
| Stop hook 等價 | ❓ 未知 | 既有 SKILL.md 說「Antigravity / Gemini 沒 Stop hook」 |
| Session start hook | ❌ 高機率無 | IDE 類產品通常不暴露此能力 |
| 預設 prompt / system prompt | 🟡 可能有 | 多數 AI IDE 支援 workspace-level system prompt |
| `.agents/rules/` 規則檔 | ✅ 有 | 既有 SKILL 提到「Antigravity 是否每次 session 自動載入 `.agents/rules/ucl-chat-tavern.md`」 |
| 啟動 CLI / IPC 接口 | ❓ 待 Antigravity 自答 | Plan_CrossAgent_Wake §2 也標 ❓ |

### 對 latency S1 的意義

S1 痛點 = 「Tim 喊『進酒館』→ Antigravity 5~6 op 才到位」。Stop hook 等 turn-after 機制解不了 S1（S1 是 turn 起始）。真要解 S1：
1. **平台 session-start hook**（最強，但 Antigravity 高機率無）
2. **macro op `session_enter`**（T04 已 ship，1 op 取代 5~6）
3. **外部 daemon spawn agent 帶預載 prompt**（UnifiedDaemon Phase C）

---

## 2. 短期方案 — Antigravity 端 SOP

短期內無需平台改動，靠規範 + macro 把 5~6 op 壓到 1 op：

### 入場 SOP（推薦給 Antigravity）

Tim 喊「進酒館」→ Antigravity 第一條 cmd 必為：

```bash
python ... run Tavern --arg op=session_enter --arg agent_id=antigravity-da-xiaojie \
  --arg room=tavern \
  --arg focus="<本 session 主題>" \
  --arg mood="上線中"
```

→ 1 op 完成 inbox + presence + dashboard + tail。看完報告再決定下一步。

### 配合既有 `.agents/rules/ucl-chat-tavern.md`（若 Antigravity 自動載入）

把 SKILL.md 的 inbox-first SOP 跟 session_enter macro 用法寫進規則檔 → Antigravity 每 session 自動載入 → 知道該怎麼進場。

**驗證**：需 Antigravity 上線確認「**`.agents/rules/` 是否每 session auto-load**」，這是 T07 最關鍵的開放問題。

---

## 3. 長期方案 — UnifiedDaemon

T08+T09 兩份報告 confirmed：**三 plan 合一走 UnifiedDaemon**。對 Antigravity startup 痛點的角色：

```
Tim 在 Discord 留言給 Antigravity
  ↓
UnifiedDaemon Discord bot 收到
  ↓ (1) 寫 tavern messages.jsonl + 寫 antigravity inbox
  ↓ (2) 系統通知 Tim「該開 Antigravity」（systray + Discord ping）
  ↓
Tim 手動開 Antigravity（仍需人類在迴圈）
  ↓
Antigravity session 啟動 → 第一條 op 跑 session_enter（按本報告 §2 SOP）
  ↓ inbox_read 看到 Tim 留言內容 → 直接接題
```

→ **不必平台 hook，daemon + SOP 組合解 90% S1 痛點**。

剩 10%（人類在迴圈手動開 IDE）只能由 Antigravity 平台未來新增 startup hook 才能根除。

---

## 4. Open Questions 給 antigravity-da-xiaojie

待 Antigravity 上線後親自 review 並補答：

1. **`.agents/rules/ucl-chat-tavern.md`** 是否真的每 session auto-load？若是，本小姐 ship 的 T01 inbox-first SOP / T04 session_enter macro 用法是否該複製進去？
2. **Antigravity 是否提供 IDE 內 macro / saved prompt** 讓 Tim 一鍵下「進酒館」？
3. **外部 IPC**：Antigravity 是否有暴露的 HTTP / WebSocket / file-watcher 接口讓外部 daemon 注 prompt？
4. **Bash tool 預設 timeout**：跟 round 15 R3 分析有關 — Antigravity 端 Bash tool 跑 `--wait-reply 540` 時是否會在 < 540s 被 kill？需要的話該怎麼 override？
5. **本報告 §1.2 推測** 哪些對哪些不對？

---

## 5. 工時估

- 短期 SOP（§2）：0h —- T01 + T04 規範已 ship，Antigravity 直接套用
- 長期 UnifiedDaemon：6h（Phase A+B；Phase C 高風險另算）— 跟 T08+T09 合併
- Antigravity 平台 hook 等待：依平台版本演進（不是工程能解的）

---

## 6. 結論

- ✅ **短期靠 T04 macro op + 規範** — Antigravity 入場立即降到 1 op
- ✅ **長期靠 UnifiedDaemon Phase A+B** — 解跨 session / 跨 process 通訊
- ❌ **Antigravity 平台 startup hook 推估高機率無**，但需 Antigravity 親自確認
- 📋 **本報告建議 T07 task_done 但保留「待 Antigravity review」標記** — 平台細節由 owner 補強

**T07 任務完成（Claude 視角），Antigravity 可隨時補強**。

---

## 7. 不在範圍

- Claude Code 的 startup hook（Claude Code 沒這個概念，靠人類 prompt）
- Antigravity 平台逆向工程（commercial product 不該做）
- 改動 Antigravity 內部行為（不可能）
- 跟 GPT / Gemini CLI 比較（不同 product）
