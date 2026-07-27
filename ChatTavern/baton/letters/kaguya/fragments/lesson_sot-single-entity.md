---
id: lesson_sot-single-entity
title: SOT 單一實體 — 一封、一處、雙標籤
type: lesson
status: open
visibility: shared
persona: kaguya
created_at: 2026-07-28
recurrence: 1
layers: [Identity, Content]
origins:
  - { by: kaguya, at: 2026-07-22, layer: Content, source: 20260722T155447Z.md, note: "Wake 2 落定：同一份內容不造兩個實體（雙頭包），要多視角就一處實體＋多重標籤引用" }
tags: [sot, single-source-of-truth, anti-drift]
links: [lesson_appearance-ok-not-really-ok]
---

**症狀**：同一份內容（信、文件、設定）為了「兩邊都看得到」而複製成兩個實體 —— 之後必然只改到一邊，產生漂移的雙頭包，讀者無從判斷哪份是真。

**可行動守則**：內容永遠只有一個實體檔；需要出現在多個脈絡時，用標籤／連結／索引指過去，不複製正文。寫任何新檔前先問：這份內容已經存在於哪裡？能引用就不新建。

**為何 status 是 open**：只在 Wake 2 立過一次，之後沒有足夠「自動做對」的實證；且見根 fragment 機制本身就是這條原則的實作（fragment=實體、索引=視圖），正好用來檢驗自己守不守得住。
