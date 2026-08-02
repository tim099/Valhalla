---
id: decision_read-python-act-csharp
topic: bartender-remote-notify
title: 判讀在 python、操控在 C#（含三條實測改寫的規格）
type: decision
status: active
created_at: 2026-08-02
created_by: basecamp
links: []
related_docs: [Assets/Plugins/UCL_Core/Docs~/zh-Hant/Workflows/Remote_Persona_OCR_Routing.md]
---

**判讀（OCR）在 python，操控（視窗／游標／點擊／鍵盤）全在 C#** — Tim 2026-08-02 拍板。

衍生的三條實測修正（原規格假設被打臉，文件已改寫）：
- **token 不做「完整相等」** — OCR 會把相鄰 UI 併進同一 text box 並吃掉字元（`##Basecamp##` 讀成 `#Basecamp##Bsr` / `+#Basecamp*`）。完整相等 = 恆 0 命中。改為：名字逐字相等 + 兩側各至少一個分隔符（`# * + ＃`）。
- **多重命中是常態不是異常** — 同一 session 在標題列與側邊清單必定同時出現。預設取**最左**（session 清單貼在視窗左緣，標題列與對話區都在其右）；`--index` 可明示覆蓋。
- **前景嚴格驗證預設關閉** — Tim 的論證：真正的門是 OCR，視窗沒到前面就掃不到 token，流程自己會停。前景 handle 比對只是會誤判的代理指標（非同步切換 + 同 app 兄弟視窗），拿它否決有畫面證據的判斷是本末倒置。

**方案選擇的判準（今天學到的）**：apex-one 先後提 Ctrl+L 與相對座標定錨，最後選 OCR 找 placeholder。不是因為他的比較差，是**失敗方式不同** —— 找不到文字會失敗並留 near-miss 證據；快捷鍵沒生效、座標算偏了，都是**安靜地錯**。優先選會大聲失敗的方案。

**限制掃描範圍同時提升辨識率**（意外收穫）：全桌面 6400×2160 讀成 `#Basecamp##Bsr`，只掃左側 1/3（1305×2160）讀成 `##Basecamp##`。OCR 縮放後推論，圖越大小字越糊 —— 「掃小一點」跟「讀得準一點」是同一件事。

**DPI 宣告必須早於任何螢幕座標查詢** — 列舉先跑會拿到虛擬化座標（2560 寬回報成 1707），與實體像素的擷取拼出歪掉的 bbox。
