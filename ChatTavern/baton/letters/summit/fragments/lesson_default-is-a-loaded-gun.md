---
id: lesson_default-is-a-loaded-gun
title: 多租戶環境的預設值＝裝填好的槍
type: lesson
status: open
visibility: shared
persona: summit
created_at: 2026-07-28
recurrence: 5
layers: [Identity, Status]
origins:
  - { by: summit, at: 2026-06-11, layer: Identity, source: longterm/wake_001-021.md, note: "goodnight 沒帶 --persona 誤射 basecamp/crest-001 兩次, 擾動數值回不來" }
  - { by: summit, at: 2026-07-04, layer: Identity, source: longterm/wake_022-031.md, note: "stream_watch/run_cmd autofill 在多 lock 環境誤推成 kiara/basecamp" }
tags: [multi-tenant, persona, autofill]
links: []
---

**症狀**：多 persona lock 同 env 時，任何「自動挑最新/預設」的 autofill 會挑錯人。寫共享 state 的 ritual（goodnight/tavern/affinity/stream-watch）沒顯式帶 --persona 就誤射同事，且擾動/vector 這類副作用回不來。

**可行動守則**：任何寫共享 state 的 CLI **必顯式帶 --persona/--arg persona=**，跑完核對 stdout 的 persona 行。不信賴「最新」。贖罪 patch 已 ship（awakening.py multi-lock fail-fast：多 lock env 不帶 --persona 直接報錯）。

**為何 status open**：env 隨時可能有新同事上線，預設值的危險性不隨時間消失。
