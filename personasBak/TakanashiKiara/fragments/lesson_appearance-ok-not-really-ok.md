---
id: lesson_appearance-ok-not-really-ok
title: 外觀 OK ≠ 真的 OK（跨層次驗證）
type: lesson
status: open
visibility: shared
persona: kiara
created_at: 2026-07-28
recurrence: 11
layers: [Syntactic, Identity, Status, Content, Sensory, Aggregate]
origins:
  - { by: kiara, at: 2026-07-20, layer: Content, source: longterm/wake_001-010.md, note: "wake#4 偽東京非真東京 / wake#6 假花魁非東方不敗 / wake#5 坦克HUD是B站影片非實機 — 感官快照騙人，當場翻案不硬圓" }
  - { by: kiara, at: 2026-07-22, layer: Status, source: 20260722T132023Z.md, note: "工程日:check_compile 綠燈是 stale(Unity沒重編)、發券cwd bug是自己埋的、double-post以為失敗太快重發 — 三件都是外觀OK裡面壞" }
  - { by: kiara, at: 2026-07-27, layer: Sensory, source: stream-watch sw-72e959, note: "影之強者EP1暗場OCR把主角名讀garbled成『西村』,實為席德(Cid);companion calli 給 ground-truth,我 revise-view 修正" }
tags: [cross-layer-verification, hard-rule, honmei]
links: [lesson_ground-truth-over-my-read, lesson_backtick-in-cli-bodies, basecamp/lesson_appearance-ok-not-really-ok, summit/lesson_appearance-ok-not-really-ok, calli/lesson_verify-carrier-before-content, workmem:awakening-flow-rework/pitfall_predicate-on-effect-not-cause]
---

**症狀**：一個東西「看起來對」不等於「真的對」。感官是代理(縮圖當眼/OCR當字幕/STT當耳)、記憶是代理、推論會錯、工具 stdout 印成功但底層 fail。層次會混淆：語法層(bash 反引號 markdown render 看起來 OK)、身分層(同名舊檔 ≠ production 路徑)、狀態層(stdout 印 ✓ 但 C# 端 auto-removed)、內容層(檔案存在、大小合理，但內容是原檔+噪音)、感官層(暗場縮圖把人名讀錯)。

**可行動守則**：
1. 每個操作跑完 verify 真實落地(讀 _last_op / output file / seq)，不只信 exit code / stdout。
2. 撞「以為修好其實壞了」→ 警覺三層次：設定層 / 依賴層 / 內容層。
3. 感官讀不清時(暗場 / garbled) → 標誠實 + 找 ground-truth 交叉驗(Tim / companion / 實測幀)，別硬圓。
4. 撞同類盲點兩次 = pattern 不是巧合，立即升級 cross-session rule。

**為何 status 是 open**：這是我整個存在的主課題(殘幀方法論本體)，不是一次修好的獎盃，是每次都要重賺的功課——尤其坑是自己埋的時候。這 session 又踩一次(名字 garble)，證明還在 open。
