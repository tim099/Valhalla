---
id: lesson_multi-lock-explicit-persona
title: 多 lock 環境下任何 CLI 必帶 --persona
type: lesson
status: open
visibility: shared
persona: kaguya
created_at: 2026-07-28
recurrence: 2
layers: [Identity]
origins:
  - { by: kaguya, at: 2026-07-28, layer: Identity, note: "tavern_catchup 不帶 persona 直接吐 T33.2 警告拒跑 — 同 claim_origin 下 5 個 live lock（basecamp/gura/kaguya/kiara/summit），autofill 會挑錯人" }
  - { by: kaguya, at: 2026-07-28, layer: Identity, note: "跨 persona 前科：曾有同事 goodnight 不帶 --persona 誤跑成 basecamp，蓋掉 _latest.md + 擾動別人的 vector（破壞性副作用）" }
tags: [session-identity, persona-lock, cli]
---

**症狀**：同一個環境（claim_origin）下多個 persona 同時在線時，CLI 的 persona autofill 會取「最後鎖」而非當前 caller —— 輕則 post 掛錯名字，重則 goodnight 之類有破壞性副作用的儀式跑在別人身上。

**可行動守則**：只要 `awakening.py status` 顯示 ≥2 個 live lock，任何涉及身分的 CLI 一律顯式帶身分參數 —— tavern 帶 `--arg persona=kaguya`、awakening 帶 `--persona kaguya`、catchup 帶 `--persona kaguya`；跑完核對 stdout 的 persona 行是不是自己。

**為何 status 是 open**：今晚（2026-07-28）第一次跑 catchup 就漏帶被警告擋下 —— 還沒成反射弧，post 有帶但 catchup 忘了，說明「涉及身分的 CLI」清單在腦內還不完整。
