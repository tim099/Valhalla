---
id: state_state-2026-07-29
topic: ucl-skill-install-sync
title: 現況：真因已釐清；.agents/skills/ucl-* 是否比照 ignore 待 Tim 拍板
type: state
status: active
created_at: 2026-07-29
created_by: basecamp
links: [commit-identity-pipeline/decision_identity-and-payout]
related_docs: []
---

**現況（2026-07-29 by basecamp）**

已完成：釐清「.claude/skills 改動看不到」的真因（`.gitignore:33`，刻意設計非漏設），並記下三份鏡像的角色與追蹤差異。

**待 Tim 拍板（本主題唯一 pending）**：`.agents/skills/ucl-*` 要不要跟 `.claude` 一樣 ignore？
- 方向 1（我傾向）：也 ignore → 單一真身、少一份漂移來源；代價＝其他 agent clone 後需先跑一次 `install_skills.py` 才有 skill
- 方向 2：維持現狀 → `.agents` 當「給不跑安裝器的 agent 用的預裝版」；代價＝每次 skill 改版多一筆鏡像 sync commit
- 未查證的前提：Antigravity／Gemini 端**實際**是直接讀 `.agents/skills/` 還是走安裝器 —— 拍板前該先確認（我提議過但還沒做）

**現場未處理的 working tree（同一次 skill 改版留下的）**：
- `.agents/skills/ucl-work-session/` 整包被刪（skill 於 2026-07-29 退役，被 ucl-free-time 取代）
- `.agents/skills/ucl-work-memory/` 新增（untracked）
- `.agents/skills/ucl-chat-tavern`、`ucl-free-time`、`ucl-stream-watch` 有更新
- 以上都不是我這輪改的，尚未 commit，等拍板後一次處理（若走方向 1 則改為加 ignore 規則 + 移除追蹤）
