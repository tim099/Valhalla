---
task_id: T01-survey
title: 完整 survey: 列出所有該綁 Agent@Persona 卻只綁 Agent 的位置
role: architect
created_at: 2026-05-13T11:20:57Z
status: done
owner: claude-da-xiaojie
---

# T01 Survey — Agent vs Agent@Persona binding audit

## TL;DR

掃 21+ hit point 後，**真正需要改的只有兩處**：

| # | 系統 | 寫入點 | 現狀 path | 該改成 |
|---|---|---|---|---|
| 1 | Letter to future self | `awakening.py:700-724 write_letter()` | `baton/letters/<actor>/` | `baton/letters/<actor>/<persona>/` |
| 2 | Session baton | `Cmd_SessionBaton.cs:113-114` | `baton/<actor>_<ts>.md` + `_latest_<actor>.md` | `baton/<actor>/<persona>/<ts>.md` + `_latest.md`（mirror letters layout） |

其餘均**已 persona-keyed 正確** 或**故意 agent-level**。

## ❌ 該改（this quest target）

| Path | Writer | Read by | Reason |
|---|---|---|---|
| `baton/letters/<actor>/*.md` | `awakening.py:write_letter()` (goodnight) | next-session morning; agent cat `_latest.md` | letter = persona-level subjective reframe — basecamp 寫的不該被 crest-001 / meadow 當自己讀 |
| `baton/letters/<actor>/_latest.md` | 同上 | 同上 | 多 persona 互相覆蓋 latest pointer |
| `baton/letters/<actor>/dialogues/` | dialogue chain (手寫 / 未來 Cmd_SelfAnticipation) | 同 persona future self | round-trip 對話本就 persona-specific |
| `baton/<actor>_<ts>.md` | `Cmd_SessionBaton.cs:113` | 接力 session | thread context 是 persona-bounded |
| `baton/_latest_<actor>.md` | `Cmd_SessionBaton.cs:114` | morning ritual 重建 | 同上 |

## ✅ 已 persona-keyed 正確（對照組）

| Path | Keying |
|---|---|
| `_session/_persona_<persona>.json` | persona-keyed filename（Tim 2026-05-13 refactor） |
| `AwakenInit/personas/<persona>.json` | persona-per-file split |
| `ChatTavern/affinity/<persona>/relations.json` | persona dir |
| `ChatTavern/baton/constitution/<actor>/personas/<persona>/` | core (agent-level) + personas/<persona>/ split |
| `ChatTavern/agent_bonus_quota.json` | v2: `agents[<agent>].personas[<persona>]` |
| `ChatTavern/free_time_sessions.json` | entry 帶 `agent_id` + `persona` |
| `ChatTavern/work_sessions.json` | 同上 |
| `persona_ding` inbox | path 含 actor+persona |

## ⚪ 故意 agent-level（不該動）

| Path | Why agent-level |
|---|---|
| `Treasury/ledger/<ts>__credit.json` (內 agent_id) | Token bank 共用 per agent (Tim 拍板) |
| `ChatTavern/presence.json` | 線上狀態以 agent 為單位 |
| `ChatTavern/rooms/<room>/inbox/<X>.md` | 房內 inbox 以 actor 為單位 |
| `ChatTavern/baton/constitution/<actor>/core/` | core invariants 跨 persona 共享 |
| `rooms/<room>/messages/*.json` `sender_id` | sender_id 走 agent_id（per ucl-letters: "sender_id 不變"） |

## Migration impact

- **既有 letters**：claude-da-xiaojie 32 篇 / antigravity-da-xiaojie 1 / antigravity-da-xiaojie-da-xiaojie 2 / Zeta-da-xiaojie 數筆 / cross-agent 留原處
- **既有 baton**：~3 timestamped + `_latest_claude-da-xiaojie.md`
- **Strategy**：讀 letter frontmatter `written_by_persona` → 搬進對應子目錄；沒 meta 的丟 `_unassigned/`
- **Baton** 沒 persona 欄 → 全進 `<actor>/_unassigned/` 或 best-effort 推斷

## 子任務拆解

- T02-letters-refactor — 改 awakening.py write_letter
- T03-baton-refactor — 改 Cmd_SessionBaton.cs + 加 persona arg
- T04-migrate-existing — 搬遷既有 letters/baton 進新結構
- T05-skill-doc-sync — 同步 SKILL.md / Plan_Awakening_Init_Protocol.md
