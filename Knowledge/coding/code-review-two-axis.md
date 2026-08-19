# Code review 拆成兩軸：合不合規範 vs 合不合當初要的東西

## 會這樣問

- code review 要看什麼？
- 這個 PR 怎麼審比較不會漏？
- review 只看 diff 夠嗎？
- 怎麼判斷實作有沒有偏離規格？

## 一句話

**Review 是兩個不同的問題：Standards（合不合這個 repo 的規範）與 Spec（有沒有做到當初那張 issue 要的事）——
分開跑、並排報，不要合成一句「看起來 OK」。**

## 做法／判準

- **先釘住比較基準點**：`git diff <基準>...HEAD`（**三個點**，比的是 merge-base）。
  動手前先確認 ref 解得開、diff 非空 —— **讓它在這裡就失敗，不要失敗在兩個平行子代理裡面。**
- **兩軸各跑一個子代理**，理由是**不讓彼此的 context 互相污染**，最後再由上層彙整。
- **Spec 那一軸要先找到規格來源**：commit 訊息裡的 issue 編號 → 使用者指定的路徑 → `docs/`／`specs/`
  底下對得上分支名的檔。真的沒有就明說「no spec available」，**不要自己想像一份規格來對**。
- **Standards 那一軸有基線**：即使 repo 什麼都沒寫，也套一組 Fowler 味道（Mysterious Name…）。
  兩條綁定規則：**repo 寫的規範永遠勝過基線**；每一條都是**帶標籤的啟發式**（「疑似 Feature Envy」），
  不是硬性違規；**工具已經在管的就不要再審一次**。

⇒ 可搬回本專案的形狀：這跟「交接時把**驗過的**與**沒驗的**分兩欄列」是同一個手勢 ——
**把兩個不同性質的問題分欄，讀的人才不必去猜哪一半有證據。**

## 出處

外部：`mattpocock/skills` → `skills/engineering/code-review/SKILL.md`（**讀了原文** 前 45 行；
完整 smell 清單未讀）。
提煉：basecamp 2026-08-19。
