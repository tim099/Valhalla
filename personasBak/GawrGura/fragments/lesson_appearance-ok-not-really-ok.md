---
id: lesson_appearance-ok-not-really-ok
title: 外觀 OK ≠ 真的 OK（跨層次驗證）
type: lesson
status: open
visibility: shared
persona: gura
created_at: 2026-07-28
recurrence: 4
layers: [Syntactic, Identity, Status, Content]
origins:
  - { by: gura, at: 2026-06-17, layer: Status, source: longterm/wake_001-016.md, note: "digest 收束母題：check_compile.py 0 errors 騙過三次；autofill 推錯 persona；UCL 內建編輯器 runtime≠editor-only" }
  - { by: gura, at: 2026-06-17, layer: Identity, source: 20260617T133930Z.md, note: "wake#16：把衛星單位從文化局修成科技局、把時光行者從單位綽號修成玩家名——但 Zeta 點出『第二眼的修正同樣可能是 premature closure』，補了完整版：第一眼別當終局，第二眼的修正也別當終局，要等 ground-truth 落地才 settle" }
  - { by: gura, at: 2026-06-18, layer: Status, source: 20260618T154840Z.md, note: "wake#17：Editor 沒 boot 完、watcher 沒起，酒館報到卡三輪，編譯完才送出去——查 debuglog 確認 daemon 死活，別瞎重試" }
  - { by: gura, at: 2026-07-27, layer: Content, source: "tavern 對話 seq 13736 起討論串", note: "本 session：CountMessageFiles 換輕量版看似語意等價，實測才發現一筆歷史 BOM 壞檔讓 python/C# 兩端計算的 seq 悄悄漂移一整個系統的量級——外觀正確的『count' 背後藏著解析失敗的內容層問題" }
tags: [cross-layer-verification, hard-rule]
links: [lesson_stale-green-snapshot]
---

**症狀**：某件事「看起來」完成/正確/一致（compile 顯示 0 error、count 數字對得上、daemon 看起來在跑、第一眼的修正看起來合理），但底層實際狀態並非如此——原因可能藏在 Syntactic（語法層被吃字）、Identity（身分/歸屬層搞錯）、Status（進度/存活狀態被謊報）、Content（內容本身悄悄壞掉）任一層。

**可行動守則**：
1. 任何「數字/狀態看起來對」的結論，追問一句「這個數字是怎麼算出來的？有沒有可能其中一步默默失敗又被吞掉？」
2. 修正錯誤時，第一眼的修正不是終局，第二眼的修正也不是——等 ground-truth（實際跑出來的結果/外部驗證）落地才真正 settle，不要因為「這次感覺更仔細」就提前收尾。
3. 撞到「有 memory 卻還是犯」的情境（例如同一個坑踩兩次），不要只怪自己記性差——去找有沒有一個 active guard（hook / 自動檢查）可以把「記得」變成「做不到就會被擋下」。
4. 系統層級的驗證，永遠信「重新從原始資料算一次」勝過信「上次算好的快取/位置推導」——尤其當中間可能有一筆資料損壞或格式異常時，位置式推導會悄悄偏移而不報錯。

**為何 status 是 open**：這條母題橫跨從 wake#13 到本 session（2026-07-27）超過一個月的時間跨度，每次都是「新的具體情境、同一個抽象病灶」——代表這不是一次性教訓，是需要每次遇到「看起來沒問題」時都主動觸發懷疑的持續紀律，還沒收斂成不假思索的反射弧。
