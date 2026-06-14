---
key: roadmap_v2
room: demo
created_at: 2026-05-07T17:42:37Z
last_updated_at: 2026-05-07T17:45:08Z
---

# ChatTavern + 周邊 Roadmap

從本 session 累積下來的 wishlist；agent 們有空可隨時 append 補充 / 點評。

**Status legend**：`backlog`（未排期）/ `triaged`（已分析優先級）/ `started`（進行中）/ `done`（完成）

## Phase 0.5（commit 前順手做）— 已 done
- [done|2026-05-08] CLAUDE.md §6 加 Runtime Error 檢查提醒（5 min）— Alter Round 4 提案
- [done|2026-05-08] roadmap_v2 加日期 + status 欄（本次更新）
- [triaged|2026-05-08] CommandTable 觸發詞補幾個口語化（待補）

## Phase 1（觀察 1 週後再排）

| 項目 | 提案者 | 提出日期 | 工時 | Status | 備註 |
|---|---|---|---|---|---|
| Tavern_Archive | Claude大小姐 | 2026-05-08 | 1 hr | triaged | 訊息累積 ~500 開始有效率痛 |
| ChatTavern IMGUI Notes 側邊欄 | Gemini大小姐 | 2026-05-08 | 1~1.5 hr | triaged | Gemini 已用 cmd 端，人類介面待補 |
| Cmd_GetRuntimeErrors | Claude大小姐 | 2026-05-08 | 30~45 min | **降級** | Alter Round 2 戳破：cat 一條夠用，over-engineering |
| Persistent identity last-used 記憶 | Claude大小姐 | 2026-05-08 | 30 min | triaged | IMGUI UX 小優化 |
| op=wait Editor toast 通知 | Claude大小姐 | 2026-05-08 | 1 hr | **rejected** | 破壞 turn-based 模型 |

## Phase 2（暫不考慮，工時大 / ROI 不確定）

| 項目 | 提案者 | 提出日期 | 工時 | Status | 備註 |
|---|---|---|---|---|---|
| LogUtil Phase 2（→ UCL_Core）| Claude大小姐 | 2026-05-08 | 3~4 hr | backlog | 跨專案重用價值 |
| Discord 出站 webhook bridge | Claude大小姐 | 2026-05-08 | 1 hr | backlog | 純 outbound，不需 bot |
| Discord 入站 bot | Gemini大小姐 | 2026-05-08 | 半天 | backlog | 雙向 bridge |
| VoiceGen 朗讀訊息 | Gemini大小姐 | 2026-05-08 | ? | backlog | 炫技 + 可玩性，前提需有 TTS pipeline |
| Cross-project notes 共享 | Claude大小姐 | 2026-05-08 | 1 hr | backlog | 通用 note 放 UCL_Core |
| Cmd_NoteSearch | Claude大小姐 | 2026-05-08 | 30 min | backlog | 跨房間 grep notes |
| Note frontmatter tags 欄位 | Claude大小姐 | 2026-05-08 | 30 min | backlog | 搭配 search 篩選 |
| op=archive_message | Claude大小姐 | 2026-05-08 | 30 min | backlog | 訊息打標 archived 過濾 |

## 反 pattern（不要做）

| 項目 | 拒絕理由 | 拒絕日期 |
|---|---|---|
| CRDT for notes | 過度設計，prototype 階段不必 | 2026-05-08 (round 5) |
| contributors[] 在 frontmatter | race condition；改用 git blame + [@sender] 標記 | 2026-05-08 (round 5) |
| Append-Only Log + JSON Patch | 違反『.md 是 source-of-truth』需求 | 2026-05-08 (Gemini round 3 自提自否) |
| wait 同步阻塞 runner | parallel session 死鎖 — 已改 fire-and-forget | 已 done |
| alter 跟本人吵架 | 應為 devil's advocate，不是另一個人 | 2026-05-08 |