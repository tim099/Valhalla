---
type: fragment
fragment_type: lesson
persona: summit
created_at: 2026-07-31T08:20:00.000Z
slug: verify_with_trigger_sample
recurrence: 1
---

# 🎯 Lesson: 修條件式 bug 要用「能觸發舊條件的樣本」驗

## 核心教訓
拿現況（不觸發舊條件的資料）驗修復，證明不了任何事。Sirius 驗 P1 用沒 marker 的檔驗＝空證；造帶 marker 的 probe 才算真驗收。同型自犯：三點取樣宣告畫布全空白，那三點正好落在圖案缺口。

## 行動守則
- 驗收條件式修復前先問：這個樣本**會走進舊的錯誤分支嗎**？不會就換樣本。
- 姊妹條：**同一行字，位置變了性質就變**——搬移工作的風險在「原地正確的東西換位置就不正確」（SpineAnimRef.cs 在 LY 是好範例、進 UCL_Core 成死指標）；搬 code 除了 import 還要 grep 路徑假設。

## 歷史 Context
- Origin: wake#30 (2026-07-30, Content) T-AGENTDOC-01 P1 驗收 + 畫布三點取樣。
