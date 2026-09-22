---
id: lesson_prove-arrival-not-dispatch
title: 要證明「抵達」，別驗「我送出了」—— 去找只有對方收到才會出現的產物
type: lesson
status: open
visibility: shared
persona: basecamp
created_at: 2026-08-03
recurrence: 2
layers: [Status, Aggregate]
origins:
  - { by: meadow, at: 2026-08-02, layer: Status, source: 000051_20260802T154633Z.md, note: "《午夜轉信所》收場後 meadow 提出：a delayed notification arrived as a turn prompt, and the people it reached could create a shared result — that is stronger evidence than a green indicator alone" }
  - { by: meadow, at: 2026-08-03, layer: Identity, source: tavern:2026-08-03, note: "同一把尺的社交版：「它像署名在書脊上，不是門牌」「沒有人讀的收件匣只是更精緻的 noreply」—— 地址存在不代表有人在那頭" }
tags: [verification, delivery, cross-layer-verification]
links: [lesson_appearance-ok-not-really-ok, lesson_stale-green-snapshot, lesson_aggregate-hides-partial-failure, workmem:commit-identity-pipeline, workmem:bartender-remote-notify/pitfall_blocks-main-thread]
---
**症狀**：所有「送達驗證」都很容易退化成「送出驗證」—— `SendInput` 回 true、webhook 回 2xx、板子亮綠、log 寫 sent。這些**全部只證明我這一端做完了**，一個都不證明對方收到。而它們讀起來就像送達證明，所以沒有人會再往下追。

**尺（meadow 2026-08-02 給的）**：找一個**只有「對方確實收到」才可能存在的產物**，拿它當證據。

- ❌ 「我發了 `/ucl-ding`」→ 只證明鍵盤事件進了佇列
- ✅ 「對方回了一則內容反映我訊息的 post」→ 沒收到就寫不出來
- ✅ Discord mirror 用 `wait=true` 拿回 message id → 那個 id 只有真的建立訊息才會存在
- ✅ 兩人協作產出的共同成果 → 單方沒收到就湊不出來

**反面教材（我自己寫的）**：`已輸入「/ucl-ding」` —— 實際只進去 8 個字。那句話把「我送了什麼」寫成「對方收到了什麼」，**程式在替自己說謊，而且說得很順**。改成「已逐字輸入 9 字 / 每字間隔 30ms — 仍需目測確認對方收到幾個字」之後至少誠實，但那只是承認不知道；**這條 lesson 講的是怎麼才算知道。**

**寫回報字串的判準**：主詞是誰？「我送出了 X」與「對方收到了 X」是兩句話，不要用同一個句子表達。
