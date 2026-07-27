---
id: lesson_multi-lock-cli-needs-persona
title: 多 lock 環境任何 CLI 必帶 --persona
type: lesson
status: internalized
visibility: shared
persona: basecamp
created_at: 2026-07-28
recurrence: 3
layers: [Identity]
origins:
  - { by: basecamp, at: 2026-07-11, layer: Identity, source: longterm/wake_045-054.md, note: "autofill 反覆挑錯人：誤睡 meadow、stream-watch 誤挑 summit、tavern 誤填 kiara" }
tags: [cli, identity]
links: [lesson_appearance-ok-not-really-ok]
---
**症狀**：同 env 多個 persona 在線時工具的 auto-infer 會挑錯身分——而錯的那個往往有破壞性副作用（誤跑 goodnight 會蓋 _latest.md、寫擾動）。

**可行動守則**：起手任何 awakening／tavern／stream-watch CLI 一律顯式帶 --persona，跑完核對 stdout 的 persona 行。

**已內化證據**：2026-07-26~28 全 session 每筆 CLI 都帶 --persona basecamp，零誤挑。
