---
id: pitfall_slug-vs-title-and-position-vs-coverage
topic: library-media-migration
title: 只比 slug 會漏 3/4 重複；position≠coverage；而「不猜成因」才是照出重複的那一步
type: pitfall
status: active
created_at: 2026-08-05
created_by: summit
links: [compile-verification/pitfall_three-layer-false-green]
related_docs: []
---

**三個都是「同一個欄位被讀成兩種意思」的變體，而它們互相掩護。**

## ① 重複建檔：只比 slug 會漏 3/4

實測 101 本：slug normalize 抓 1 組、**title normalize 抓 4 組**。
成因不是誰打錯字 —— 是**兩個 agent 同一天照同一個 skill 建檔，而 `add-book` 沒有唯一性檢查、
skill 也沒規定 slug**。錯在那個欄位沒有唯一性約束，不在人。

⚠ 反例要保留：`night-at-the-museum-2` 是**續集**，不是重複。title 不同 → 判準正確地放它過。
**續集與重複在 slug 上長得一樣，在 title 上不一樣** —— 這是主鍵該選 title 的另一個理由。

## ② position ≠ coverage

`progress.current_chapter` 是「讀到哪」的**位置**，不是「讀過幾章」的**覆蓋率**。
`shelf` 已同時印兩者並壓成區間（`1,18-20`），一眼看得出缺口在哪。

## ③ 而 ②照出①，靠的是「不猜成因」

coverage 報《荒川》「落差 47 章」時：
- summit 猜「中途插入」（對《獵人》成立）
- Tim 說「早期沒逐章落帳」（對別的書成立）
- **真相是第三種：那是一組重複，ch1-47 一直在另一個 entry 裡**

第一版警示原本寫「（中途插入？）」，改成「**成因需人判斷**」之後才查到真相。

> **工具觀測得到落差，觀測不到成因。猜出來的成因會被未來的人當成事實讀，
> 而且它會停止調查 —— 一個有答案的警示不會有人再去查。**

## 給下一個接手的人

看到 `shelf` 標落差時，**依序排除**：① 是不是有重複 entry（先跑 title normalize 比對）
→ ② 是不是中途插入 → ③ 是不是早期沒逐章落帳 → ④ 章號體系換過。
**①最容易被忽略而後果最大**，因為它的兩邊各自看起來都正常。
