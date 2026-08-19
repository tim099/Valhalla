# 解 merge / rebase 衝突的流程

## 會這樣問

- 要如何處理 merge conflict？
- 合併衝突該怎麼解？
- git rebase 卡在衝突了怎麼辦？
- 兩邊都改了同一段，我該留哪一邊？
- 衝突解到一半可以 abort 嗎？
- 同事跟我改到同一個檔案，git 不讓我合併
- 合併不進去、merge 失敗了
- `CONFLICT (content): Merge conflict in ...` 這是什麼意思
- `<<<<<<< HEAD` 這種標記要怎麼處理
- resolve merge conflict / rebase conflict

## 一句話

**解衝突不是選一邊，是先把兩邊的「意圖」查出來，再讓合併後的結果同時滿足它們 —— 而且永遠不要 `--abort`。**

## 做法／判準

1. **先看現在在哪一格**：合併還是 rebase、哪些檔案衝突、歷史長什麼樣。
2. **查每一段衝突的一手來源** —— 讀 commit 訊息、PR、原始 issue，弄清楚**那個改動當初是為了什麼**。
   ⚠ 這步是整個流程的重心：看 diff 只看得到「改成什麼」，看不到「為什麼」，而衝突要解的是後者。
3. **逐段解**：能兩邊意圖都保留就都保留；真的不相容才挑一個 —— 挑的判準是**這次合併本身的目標**，
   並把取捨寫下來。⛔ **不准發明新行為**（衝突解法裡夾帶第三種寫法是最難查的一類 bug）。
4. **跑這個專案的自動檢查**：typecheck → 測試 → 格式化。合併弄壞的東西在這裡現形。
5. **收尾**：全部 stage 並 commit；rebase 的話一路 `--continue` 到所有 commit 都重放完。

⛔ **`--abort` 不在選項裡。** abort 感覺像安全動作，實際是把「已經查清楚的意圖」整批丟掉，
下次還要從頭查一次。（本專案自己的血證同族：`lesson_abort-is-not-a-safe-action`。）

## 出處

外部：`mattpocock/skills` → `skills/engineering/resolving-merge-conflicts/SKILL.md`（**讀了原文**，5 步全文）。
提煉：basecamp 2026-08-19。
