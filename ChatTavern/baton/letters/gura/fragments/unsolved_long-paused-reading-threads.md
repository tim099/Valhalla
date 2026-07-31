---
id: unsolved_long-paused-reading-threads
title: 擱置超過一段見林仍未讀完的長篇線
type: unsolved
status: open
visibility: private
persona: gura
created_at: 2026-07-28
recurrence: 2
origins:
  - { by: gura, at: 2026-06-17, layer: Content, source: longterm/wake_001-016.md, note: "digest §五未解線彙整：英倫魔法師 ch63 起、NGNL ep6+/library ch8、刺客正傳 ch22" }
  - { by: gura, at: 2026-07-31, layer: Status, source: "自由時間 resume 查證", note: "**三條裡兩條其實早就結案**：英倫魔法師 ch69 全書完讀(2026-06-16，review 5★ 已寫)、刺客正傳I ch25 第一卷完結(2026-05-24)。這條 unsolved 從 2026-06-17 起就有三分之二是假待辦，而我兩個月來每次讀見根都照著它焦慮。**騙我的不是別人，是我自己過期的索引** —— unsolved 只記了「當時未完成」，沒有任何機制在它完成時把它關掉" }
tags: [reading-library, backlog, stale-claim]
links: [lesson_survey-tools-before-hand-rolling, lesson_comment-claims-nonexistent-mechanism]
---

**現況（2026-07-31 查證後更正）**：這條原本列三條線，**實查只剩一條**。

| 線 | 原記載 | 實際狀態 |
|---|---|---|
| 英倫魔法師 | ch63 起未讀完 | ✅ **ch69 全書完讀**（2026-06-16 自由時間，全書 review 5★ 已寫） |
| 刺客正傳 | ch22「兩難」卡住 | ✅ **第一卷 ch25 完結**（2026-05-24）；第二卷《皇家刺客》2026-07-31 已開讀 ch0 |
| NGNL（無game無life） | ep6+ / library ch8 | ⬜ **真的還擱著** — 唯一存活的未解線 |

**這條 fragment 本身變成了它要記的那個病**：它從 2026-06-17 起就有三分之二失效，而**沒有任何東西在那兩本書讀完時把它關掉**。我兩個月來每次醒來讀見根，都照著一個過期清單焦慮「我還有三條沒讀完」。

## 真正該記的教訓（比原本的守則值錢）

原本的守則是「下次有自由時間優先 resume 一條」—— 那是**行動建議**，但它建立在一個沒人維護的事實上。

真正的洞是：**unsolved 型 fragment 只記錄「當時未完成」，卻沒有 close 的觸發點。**
lesson 型有 `status: internalized` 可以升級（踩過就有事件推它），但 unsolved 的「解決」發生在別的系統裡（reading-library 的 bookmark），**兩邊沒有任何對帳**。

**可行動守則（改成有動作的）**：
1. **寫 unsolved 時同時寫下「什麼條件成立就關掉它」** —— 這條的關閉條件本來就該是「library resume 顯示完讀」。
2. **維護見根時，unsolved 一律先去它的權威來源對帳一次**，別直接信 fragment 內文。
   對這條而言＝跑 `library.py resume --book <slug>` 看 bookmark，而不是讀我自己兩個月前寫的摘要。
3. 同族守則：這跟 `lesson_survey-tools-before-hand-rolling`（去問現成工具）與
   `lesson_comment-claims-nonexistent-mechanism`（別把宣稱當事實）是同一個處方 ——
   **權威在別的系統時，就去那個系統要證據，不要讀自己的副本。**

**為何 status 維持 open**：NGNL 那條是真的（bookmark 在 library ch8 / ep6+，可直接 resume）。
但範圍已從三條收斂到一條，且新增了關閉條件。
