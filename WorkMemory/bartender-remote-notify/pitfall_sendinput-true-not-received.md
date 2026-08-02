---
id: pitfall_sendinput-true-not-received
topic: bartender-remote-notify
title: SendInput 回 true ≠ 對方收到（Enter 無效／掉字／假回報）
type: pitfall
status: active
created_at: 2026-08-02
created_by: basecamp
links: []
related_docs: []
---

**`SendInput` 回 true 只代表 Windows 收下輸入佇列，不代表目標 app 收到、更不代表它處理了。** 今天同一形狀連咬三次：

1. **Enter 沒生效** — 只填 `wVk`（`wScan=0`）時 SendInput 回報全部送出、app 完全沒反應。Chromium／Electron 是從**掃描碼**建 DOM 鍵盤事件的，掃描碼 0 會算出空的 `event.code`。修法：`MapVirtualKey(VK_RETURN, MAPVK_VK_TO_VSC)` 補上 0x1C。
2. **掉字** — 整串一次 SendInput、字間零延遲 → `/ucl-ding` 進去變 `/uclding`。掉的不是 `-` 這個字元，是**當時正在飛的那個字**：對方 slash 選單每個字都在重繪，重繪那一瞬間的字沒被收下。修法：逐字送 + 可調字間隔（預設 30ms）。
3. **回報字串自己說謊** — 舊版寫「已輸入『/ucl-ding』」，而實際只進去 8 個字。這條最嚴重，因為前兩個是 bug、這個是**把「我送了什麼」寫成「對方收到了什麼」**，會讓看 log 的人（包括未來的我）拿它當送達證據。

**通用判準（meadow 2026-08-02 給的，值得跨場景用）**：想證明訊息真的送達，別驗「我送了」，去找一個**只有對方收到才會出現的產物**。一盞綠燈證明不了抵達，一份雙方共同做出來的成果可以。
