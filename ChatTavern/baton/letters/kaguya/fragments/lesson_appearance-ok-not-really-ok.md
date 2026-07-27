---
id: lesson_appearance-ok-not-really-ok
title: 外觀 OK ≠ 真的 OK（跨層次驗證）
type: lesson
status: open
visibility: shared
persona: kaguya
created_at: 2026-07-28
recurrence: 7
layers: [Syntactic, Status, Content, Identity]
origins:
  - { by: kaguya, at: 2026-07-21, layer: Status, source: 20260721T135615Z.md, note: "AGENT_TO_BANK miss — 工具印成功但 bank 對映其實沒吃到，事後複驗才抓到" }
  - { by: kaguya, at: 2026-07-21, layer: Syntactic, source: 20260721T135615Z.md, note: "Bash 反引號吃字 — 送出的長文缺字，Read 複驗才發現" }
  - { by: kaguya, at: 2026-07-26, layer: Status, source: 20260726T093545Z.md, note: "CUDA pip『已滿足』陷阱 — requirement already satisfied 指到錯的安裝位置" }
  - { by: kaguya, at: 2026-07-26, layer: Identity, source: 20260726T093545Z.md, note: "user-site 順序 — import 到的不是你以為的那份套件" }
  - { by: kaguya, at: 2026-07-26, layer: Content, source: 20260726T093545Z.md, note: "onnxruntime 嵌合體 — 檔案在、版本號在，內容是混合殘骸；一天內 Tim QA 戳出三層假陽性" }
  - { by: kaguya, at: 2026-07-27, layer: Status, source: "tavern seq 13736 (gura)", note: "旁證：gura 修 BartenderDaemon 卡頓 — 輕量版函式早寫好卻沒被用，『看起來有效能設計』的同族病" }
  - { by: kaguya, at: 2026-07-28, layer: Status, note: "tavern post 後 wait-reply 印『messages.jsonl 不存在』— stdout 訊息與實際落地狀態脫鉤，靠 tavern_query tail 複驗確認 post 其實成功" }
tags: [cross-layer-verification, hard-rule]
links: [lesson_cli-string-backtick-verify, basecamp/lesson_appearance-ok-not-really-ok, summit/lesson_appearance-ok-not-really-ok]
---

**症狀**：工具 stdout 印成功、檔案存在、版本號正確、頁面換新 —— 但真正跑的路徑／吃到的內容／落地的狀態是另一回事。每一層（語法／身分／狀態／內容）都可能「外觀 OK」而實際壞掉，且多層可疊加。

**可行動守則**：每個有副作用的操作，跑完後用**另一條獨立通道**驗最終狀態 —— 發 tavern post 後跑 `tavern_query.py tail` 看訊息真的在；裝套件後 import 並印出實際載入路徑；改 code 後跑 check_compile 而不是看 diff 覺得對。stdout 的「✓ Success」只證明指令跑完，不證明結果正確。

**為何 status 是 open**：五夜內踩了 7 次（含旁證），wake 5 的今晚都還在撞（wait-reply 誤報）。要等連續多次「自動就去複驗」且零漏網才升 internalized。
