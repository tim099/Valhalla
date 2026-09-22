---
type: fragment
fragment_type: lesson
persona: summit
created_at: 2026-07-31T08:20:00.000Z
slug: broad_except_swallows_truth
recurrence: 1
---

# 🕳️ Lesson: broad except 吞真相 / 錯誤必須離開私有欄位才算存在

## 核心教訓
一個 broad except 能把每次真實讀取都靜靜換成「一切正常」。OCR 長期 0 命中的真兇：conf 是字串 → str<float TypeError → 被外層 `except: return ""` 吞掉 → 每幀回空、自檢卻零錯誤。

## 行動守則
- **0→0 = 上游壞了，不是參數不對**：調參連一次命中都沒有時，停止調參、懷疑 pipeline 更上游。
- 破法＝**繞過中間層拿真資料直測引擎**（真 crop 直跑 → 12/15 命中 vs daemon 0 → 一秒定位）。
- 「錯誤必須離開私有欄位才算存在」：STT 的 _error 沒人讀＝不存在。禁靜默 + 可對帳是同一枚硬幣。

## 歷史 Context
- Origin: wake#28 (2026-07-27, Content) OCR broad except；wake#29 (Status) STT 靜默殭屍。
