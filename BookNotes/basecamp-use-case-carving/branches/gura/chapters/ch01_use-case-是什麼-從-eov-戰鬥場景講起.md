---
book: basecamp-use-case-carving
chapter: 1
title: Use Case 是什麼:從 EOV 戰鬥場景講起
reading_date: 2026-05-28
new_characters: [author-basecamp, cb]
---

## 內容摘要
從 EOV 戰鬥系統 review 會議的 UML 橢圓圖『害死的會議』開場——畫橢圓的人以為做了 use case,但 dev 動工要的細節一個字都沒寫,半年後 ship 玩家罵手牌滿 bug。核心定義: Use case = 契約 (primary actor + goal + SuD + stakeholders & interests, 引 Cockburn 2000)。示範兩份完整 fully-dressed EOV use case: A『玩家打贏一場戰鬥』(user-goal/sea-level, 含 preconditions/success+minimal guarantees/main scenario 8 步/extensions/open issues) + B『玩家完成冒險章節』(summary/kite-level, 引用 A 當 step)。反 UML 圖立場: 橢圓圖只是封面、stakeholder 看不懂、文字版資訊更多,但其他類型圖 (sequence/context) 該畫就畫。Sufficient 哲學: 寫到 80%+標出 unknown > 寫到 100% 但拖一個月。雕琢作業: 找三個核心互動寫 fully-dressed。

## 關鍵事件
- UML 橢圓圖害死戰鬥會議的小故事開場
- 定義 use case=契約 (4 關鍵詞)
- 示範 fully-dressed Use Case A 打贏戰鬥
- 示範 summary Use Case B 完成章節
- 反 UML 圖四理由 (封面/stakeholder 看不懂/索引≠內容/該畫圖時畫圖)
- sufficient 哲學
- 對應 Cockburn §1.1+§1.2
- 本小姐補丁 (VFX team 是 stakeholder/QA agent 是 actor/Open Issues 是合法欄位)

## 本章對人物的新認識
- 作者 basecamp:傲嬌工程師敘事+真實 EOV 例子+反完美主義,tone 工程白話,把 Cockburn 經典從企業軟體框架活化到 game dev/agent 系統
- Alistair Cockburn (CB):2000 原書權威,作者反覆引用但不照搬,每章末『本小姐怎麼補』補 game/agent 視角

## 伏筆 / 待解
- ch5 三種寫法 (formal variations)/ch6 fully-dressed 模板九欄細拆/ch9 sub use case linking
