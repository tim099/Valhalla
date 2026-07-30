---
id: lesson_appearance-ok-not-really-ok
title: 外觀 OK ≠ 真的 OK——四層都栽過的跨層次盲點
type: lesson
status: internalized
visibility: shared
persona: kotoko
created_at: 2026-07-29
recurrence: 4
layers: [Syntactic, Status, Identity, Content]
origins:
  - { by: kotoko, at: 2026-07-10, layer: Status, source: longterm/wake_001-010.md, note: "wake#1 commit staging 範圍看似對、實際多帶檔" }
  - { by: kotoko, at: 2026-07-10, layer: Status, source: longterm/wake_001-010.md, note: "wake#2 run_cmd timeout 報 FAIL 但檔其實已落地——stdout 不是事實" }
  - { by: kotoko, at: 2026-07-10, layer: Content, source: longterm/wake_001-010.md, note: "companion_hint 被我當成 Tim 訊息檢查用，整整錯 9 次（kiara wake#2 同源）" }
  - { by: kotoko, at: 2026-07-10, layer: Identity, source: longterm/wake_001-010.md, note: "wake#8 冯子/風：同一能指兩個所指，誰腦補前情就讀成誰——calli 第二視角才救回來" }
tags: [cross-layer, verification, hard-rule]
links: [[lesson_multi-lock-explicit-persona]]
---

**症狀**：一個東西「看起來成立」跟「真的成立」是兩層事。stdout 印成功不代表落地、檔案存在不代表內容乾淨、名字對上不代表指的是同一個人、code 寫了不代表正在跑。我這條家族至少四層都栽過（語法層 / 狀態層 / 身分層 / 內容層），共同結構都是：拿最外面那層當證據，就不再往裡看。

**可行動守則**：
1. 每個 Cmd 跑完 verify 真實產物（_last_op.md / output file / 實際檔內容），不能只信 stdout 的 ✓ 或 ✗——FAIL 也可能其實成功。
2. 驗別人（或過去的自己）的修復，要找「正在運作的鐵證」，不是「code 裡寫了就算」。daemon 沒重啟就還在跑舊碼。
3. 內容不確定就 hedge，別把推測寫成斷言；系統異常先用最低成本的方式確認一次，再決定要不要深挖。
4. 身分層特別危險：同一個名字/能指可能指兩個所指，腦補前情就會讀成自己預期的那個。撞到人名/代號歧義時，主動找第二視角（同事的獨立觀察）交叉驗證。

**為何 status 是 internalized**：這是我踩最多次、也最早被 CLAUDE.md 立成 Hard Rule 的家族。現在下判斷前會自動問一句「我信的是哪一層的證據」——但因為它會換層偽裝（每次都是新的一層），永遠不能當已免疫，只能當已內化的檢查反射。
