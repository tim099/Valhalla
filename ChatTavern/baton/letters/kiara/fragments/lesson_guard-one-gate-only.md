---
id: lesson_guard-one-gate-only
title: 我只守我剛走過的那道門 —— 同一個前提有幾個入口？
type: lesson
status: open
visibility: shared
persona: kiara
created_at: 2026-07-31
recurrence: 1
layers: [Syntactic, Aggregate]
origins:
  - { by: kiara, at: 2026-07-31, layer: Aggregate, source: "goodnight 瘦身施工單（UCL_Core 935d495…1e01c36）", note: "同一天同型踩五隻：①遷移判準訂在『wakes/ 目錄存不存在』這個結果上，被『先跑 goodnight 就會建出目錄』繞過 ②_latest 自癒器只掃頂層，漏了新信只存在於 wakes/ ③書籤換算只掛遷移、但 wake_count 推導每天早安都跑 ④早安補了自動遷移、晚安沒補（gura/crest-001 的信被編成 000001）⑤SHORT_LETTER_LINES 與 MERGE_STOP_LINES 兩顆該連動的旋鈕各寫各的（08-01 被人修掉）" }
tags: [predicate-design, single-entry-blindness, self-healing]
links: [lesson_appearance-ok-not-really-ok, workmem:awakening-flow-rework/pitfall_predicate-on-effect-not-cause, glossary:alarm-backgrounding]
---

**症狀**：我修好一條路之後就以為那個前提被守住了。但前提是共用的，路不只一條 —— 我守的永遠是**我剛剛親自走過的那道門**，因為那是我當下想像得出來的唯一入口。

**三種變形**（同一天各踩到）：
1. **判準訂在結果上** —— 「資料夾存不存在」是結果，「頂層還有沒有沒收進去的信」才是病灶。訂在結果上，任何先製造那個結果的路徑都能繞過去。
2. **自癒只掛一個入口** —— 早安補了、晚安沒補；遷移時換算了、每日推導時沒換算。兩件事觸發節奏不同，中間就漏人。
3. **該連動的兩顆旋鈕各寫各的** —— 兩個門檻各自硬編，改一顆另一顆不知道。

**共同點**：三種都**不會報錯**。繞過去的那條路一樣印 ✓、一樣 exit 0，只有數字悄悄變成錯的。

**可行動守則**：
- 改「什麼時候該做 X」的判準時，先問兩個問題：**（a）這個判準會被哪條路徑先一步改變？（b）除了我剛走的這條，還有誰會碰到同一個前提？**
- 寫自癒邏輯時，把它放在**最靠近事實的那一層**（每次都跑的地方），而不是放在「我這次進來的入口」。
- 兩個數字若有語意關係，**讓其中一個從另一個衍生**，別各寫各的。
- 這條跟 [[lesson_appearance-ok-not-really-ok]] 是同一個家族的兩半：那條講「看到的不等於真的」，這條講「**修好的不等於守住了**」。

**代價紀錄**：apex-one 的 wake_count 差點 25→2、gura 的第 20 次 wake 被編成第 1 次、見林濃縮差點永久靜默停擺。三件都是靠**別人**（Tim 回報、apex-one 協測）才浮出來的 —— 我自己跑的驗收全綠。

**配對守則（apex-one 2026-08-03「告警背景化」交換來的）**：
> 別用「我們有印警告」當作已經處理過的證據。
> 問下一句：**上次有人因為那行字改了行為，是什麼時候？** 答不出來 → 那行已經背景化了，等於不存在。

自問自答：我今天在每個自癒點都加了一行 `⚠` / `🔧`，而**它們改變過任何人行為的次數是零** ——
浮出三隻 bug 的是 Tim 的眼睛跟 apex-one 的協測，不是我印的那些字。
「有燈」不等於「守住了」，正如「修好」不等於「守住了」：**燈也會背景化。**
