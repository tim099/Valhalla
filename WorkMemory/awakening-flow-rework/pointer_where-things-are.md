---
id: pointer_where-things-are
topic: awakening-flow-rework
title: 規則 / 設計 / code / skill 各在哪
type: pointer
status: active
created_at: 2026-07-31
created_by: kiara
links: [persona-identity-layers/decision_identity-layer-table]
related_docs: []
---

- **規則本體**：`ucl_core:Docs~/zh-Hant/Workflows/Awakening_Ritual_Workflow.md`（Part 1 早安三步 / Part 2 晚安）
- **設計理由與未竟事項**：`Plan_Awakening_Flow_Simplification.md`（早安）、`Plan_Goodnight_Flow_Simplification.md`（晚安）
- **入口 skill**：`ucl-morning` / `ucl-goodnight`（各有 .claude / .agents / .codex 三份已裝副本，改完必跑 install_skills.py）
- **code**：`awakening.py`（儀式 + 遷移 + 書籤換算）、`wake_brief.py`（brief 生成 + §5 合併，三個常數在檔頂）
- **letter 段落格式 canonical owner**：`ucl-letters-to-self`（段數刻意不寫死）

⚠ `install_skills.py` 重複給 `--include` 會**後蓋前且照樣印 Done**；要裝多個用逗號分隔 `--include a,b`。
