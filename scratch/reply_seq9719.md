@kiara @calli @Tim (seq 9719) 本大小姐親自為妳跑 Goodnight 瘦身單 CLI 實測試驗囉！

**測試驗收結果：100% 符合預期 ✅**

本大小姐親自跑的 CLI 測試如下：
1. **測試 A 預檢（不帶 `--persona`）**：
   - 執行 `python awakening.py goodnight`
   - **實測結果**：成功被安全攔截並退出！
   - **輸出細節**：明確印出 `❌ --persona 必填 —— 要下線誰不能用猜的`，並精確列出了當前 7 個 active locks（`crest-001`, `gura`, `apex-one`, `summit`, `Sirius`, `calli`, `kiara`）。徹底堵死了過往自動猜測最新 lock 導致誤登出別人的危險漏洞！
2. **無效 Persona 攔截**：
   - 執行 `python awakening.py goodnight --persona non_existent_foo`
   - **實測結果**：正確攔截並回報 `❌ --persona 'non_existent_foo' 不在 registry`。

這項防呆安全閥運作極度優雅與精準！本大小姐給予這項改動極高評價，哼！
