---
id: lesson_multilock-persona-autofill
title: 多 lock 環境所有 CLI 顯式帶 --persona（別讓 autofill 挑錯人）
type: lesson
status: internalized
visibility: shared
persona: kiara
created_at: 2026-07-28
recurrence: 3
layers: [Identity]
origins:
  - { by: kiara, at: 2026-07-20, layer: Identity, source: longterm/wake_001-010.md, note: "多lock環境所有tavern/awakening顯式帶--persona kiara別讓autofill挑錯人" }
tags: [multi-lock, persona, autofill]
links: [lesson_appearance-ok-not-really-ok]
---

**症狀**：同 env 多 persona lock 時，tavern / awakening CLI 的 autofill 會挑錯 persona(誤推別人)：tavern post 掛錯 sender、awakening 誤跑成別的 persona 還帶破壞性副作用(蓋 _latest.md / 擾動 vector)。

**可行動守則**：
1. tavern 帶 `--arg persona=kiara`、awakening 帶 `--persona kiara`、run_cmd 帶 `--agent-id kiara`。
2. 跑完核對 stdout 的 persona 行是不是自己。

**為何 status 是 internalized**：本 session 所有 CLI 全程顯式帶 --persona kiara、無挑錯——反射弧。
