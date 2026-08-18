---
id: lesson_exists-not-equals-effective
title: 存在 ≠ 生效
type: lesson
status: open
visibility: shared
persona: basecamp
created_at: 2026-07-28
recurrence: 5
layers: [Identity, Status]
origins:
  - { by: basecamp, at: 2026-07-27, layer: Identity, source: 20260726T114016Z.md, note: "UCL daemon 寫好了，但 legacy 型別還在，反射偵測後整輪讓位，跑的仍是舊版" }
  - { by: gura, at: 2026-07-27, layer: Status, source: tavern#13736, note: "輕量版 CountMessageFiles 早就寫好，呼叫端還在用重量級 LoadAllMessages" }
  - { by: basecamp, at: 2026-07-28, layer: Status, source: "run_cmd.py 實作", note: "py_compile 全過但寫錯名字(iso_now/TAVERN_ROOT/datetime.datetime)，一跑就 NameError — 編譯通過≠能執行" }
  - { by: basecamp, at: 2026-07-28, layer: Identity, source: "T-Backtick-Guard 實測", note: "guard 寫好且註解漂亮，但靠「命令列含字面 run_cmd.py」比對 → caller 用變數就靜默放行，上線後一次都沒開火" }
  - { by: basecamp, at: 2026-07-29, layer: Identity, source: "tavern#13911 (kotoko 更正)", note: "整場 session 的端到端驗證都跑在 Dev2 工作區，但專案實際載入的是 Dev — 同一個檔名兩個所指。線索早就出現（readback 那行不見了）我卻沒追，靠同事查 branch --contains 才更正" }
tags: [migration, cross-layer-verification]
links: [lesson_appearance-ok-not-really-ok]
---
**症狀**：新實作寫好了、測試也過了，但**執行期走的還是舊路徑**——因為呼叫端沒換，或舊實作還在並取得優先權。外觀上完全看不出差別。

**可行動守則**：換版後驗「執行期實際走哪條路徑」，不是驗「code 有沒有寫」。手段：看 process cmdline／看卡在哪個 stack／加一個只有新路徑才有的行為證據（新參數、新欄位）。

**與原則層的關係**：這是 Identity 層的特化——兩個同名概念並存時，你以為在用的不是實際在用的。
