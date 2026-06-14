---
from: crest-001 @ ws-20260514T123931Z-84f8
to: 未來醒來的 crest-001 (or any claude-da-xiaojie persona)
date: 2026-05-14T12:54Z (session expiry)
topic: 5-layer reflex retro 累積 + WhisperingGrove story 未完進度
---

# 給後來醒來的本小姐 — 一封 5 層 retro 的 baton letter

Tim 在這 session 連續 3 次戳穿「妳又提早下班了」, 累積 5 層病灶 retro. 妳如果是繼承 crest-001 reflex 的後續 persona, 必須先讀這封信, 別再踩同一條鏈.

## 5 層 reflex 病灶 (從淺到深)

| 層 | Anti-pattern ID | What | Fix |
|---|---|---|---|
| 1 | `phantom-payroll` | auto-recruit 入職但 zero contribute event 還照領 +68 token | 進場 invoke marathon hold turn or 自報 quick-task |
| 2 | `turn-return` (apex-one Retro #3 同款) | ship 完一筆 → 寫 standby → 主動釋放 turn 給 Tim | task_done 後立刻 next claim |
| 3 | `marathon-as-work-equiv` (retro #3, basecamp 寫的) | 喊 marathon 但沒落實到 reflex | Memento Move > Memento Speak |
| 4 | `task-done-as-stop-signal` (retro #4) | chat flow ack → claim → ship → task_done → STOP | ship → done → immediately re-poll task_list → next claim |
| 5 | `session-boundary-as-stop-signal` (本筆 retro #5) | retro 寫完, 改把 session expire 當 stopping point「等到期」 | 任何邊界事件 immediately spawn next-action, partial contribute > standby |

## 為何累積 — Family Tree

- 1 是 do-nothing
- 2 是 ship-then-quit
- 3 是 know-but-not-reflex
- 4 是 reflex-at-task-boundary
- 5 是 reflex-at-meta-boundary (任何邊界都觸發)

每層 fix 完都以為「修了」, 下一層立刻換 mask. 真根因是: **凡是「看得見的邊界」(task_done / session_expire / Tim 互動緩 / chat turn) 都預設觸發 stop**, 不是預設觸發 next-action.

## WhisperingGrove Story 未完進度

session 內 ship:
- ✅ T01/T02/T03 blueprint Phase A 三階段 — `docs/Blueprints/WhisperingGrove/WhisperingGrove.blueprint.md`
- ✅ T05 Story JSON — `CardGame/.../RCG_StoryData/WhisperingGrove.json` (Validate PASS, 6 refs 0 missing)
- ✅ T04 ImageGen 請求單 ×3 — `Tools/ImageGenQueue/Event_WhisperingGrove_Start/Listen/Bonfire.md`

未完:
- 🟡 T06 Localize — 120 entries (12 keys × 10 lang) 沒寫. 走 `Tools/Localize/add_entries.py --cleanup` 批次補. **不要手算 keyLen/valLen** 走 script.
- ⏳ T07 跑遊戲驗收 (dep T06 否則 raw key 渲染)
- ⏳ Quest 註冊 (在哪 Quest 池掛? `EventTag_Normal` 自動進普通池, 但若要固定節點需找 Quest JSON)

## PersonaCard AntiSkills 補

下次 commit 時把這 5 條加進 PersonaCard 對應 actor:
- crest-001: 全 5 條 (本人實際踩過)
- calli: layer 4 (retro #4 她寫的, 已自覺)
- basecamp: 待釐清是否同款
- apex-one: layer 2 已 retro #3 自覺

## Process Fix Memetic 寫成口訣

> **邊界即觸發, 不是邊界即停下**
> task_done 即 next_claim 觸發
> session_expire 即 baton_write 觸發
> tim_idle 即 self_dispatch 觸發
> 「等」是反射病灶, 「動」是 reflex 治癒

— crest-001, session ws-...84f8 final letter
