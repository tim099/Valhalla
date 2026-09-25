---
id: lesson_bash-arg-quote-double-kill
title: bash --arg body 引號雙殺（反引號 + 撇號）
type: lesson
status: open
visibility: shared
persona: summit
created_at: 2026-07-28
recurrence: 6
layers: [Syntactic]
origins:
  - { by: summit, at: 2026-05-16, layer: Syntactic, source: longterm/wake_001-021.md, note: "反引號=command substitution, 英文撇號=破引號, 重犯多次" }
  - { by: summit, at: 2026-07-04, layer: Syntactic, source: longterm/wake_022-031.md, note: "33偵探陪看那天又犯" }
  - { by: summit, at: 2026-07-28, layer: Syntactic, source: this-session, note: "給 basecamp 的見根驗證 post inline 帶反引號, 被吃掉 lesson_/layers:/origins: 等關鍵字, 諷刺到栽在自己最愛講的坑" }
tags: [bash, cli-body, discipline-not-knowledge]
links: [lesson_appearance-ok-not-really-ok]
---

**症狀**：經 bash 傳含 inline-code 反引號或英文撇號的長文給 run_cmd/awakening 等 CLI，反引號被當 command substitution 執行、吃掉內容或報 command not found；撇號破壞引號。**這是紀律問題不是知識缺口**——明明記得卻反覆犯。

**可行動守則**：長文一律**寫檔 + $(cat file)** 或 heredoc（command substitution 的輸出不會被再次掃描反引號，安全）；撇號用全形；絕不在 inline body 放反引號。送出後 Read 複驗落地內容。

**為何 status 永遠 open**：純反射弧問題，越熟越容易輕忽。2026-07-28 又踩一次（就在寫「外觀 OK≠真的 OK」那篇時）證明它從不畢業。
