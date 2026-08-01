---
id: decision_design-decisions
topic: reading-trace-system
title: 設計定案：缺的只有『閱讀時段主觀心得』一層；評分寫進 session note frontmatter 不另開檔
type: decision
status: active
created_at: 2026-08-01
created_by: kotoko
links: [agentcmd-schema-codegen]
related_docs: [tavern:2026-07-31#14090, tavern:2026-07-31#14098, tavern:2026-08-01#14114, ucl_core:Tools~/AgentCommands/library.py, ucl_core:Tools~/AgentCommands/wake_brief.py]
---

**Tim 2026-07-31~08-01 分四次拍板，加上 kaguya / gura 的實證輸入，設計已定案。尚未動任何 code。**

## 設計的核心判斷：缺的只有一層

閱讀系統原有 `log-chapter`（單章，索引在章節）/ `arc`（階段大綱，索引在**故事結構**）/ `revise-view`（人物改觀 fork）/ `review`（讀完對外推薦）/ `bookmark`+`resume`（進度）。

**續讀狀態早就存在** —— `BookNotes/<book>/branches/<reader>/book.json` 的 `progress.{current_chapter, last_read, bookmark_note}`，per-persona 分支互不干擾（summit 8 本 / calli 7 / kotoko 4）。

**缺的是「閱讀時段的主觀心得」** —— 對應記憶系統的「每夜 letter」。不能塞進 `arc`，因為**索引軸不同**：arc 的軸是故事（1–6 章是一個階段，不管讀幾天），session note 的軸是我（今晚這一場，不管跨幾章）。混在一起兩邊都會被對方的邊界切碎。

## Tim 的拍板

1. brief 顯示 **3+1**（最近 3 本 + 1 行擱置計數），需要全部時用指令
2. session note **綁 persona，放 `letters/<persona>/`**（不是 BookNotes 底下）—— 命名 `reading/`，中文「**讀痕**」
3. `bookmark_note`（給下次自己的操作提示）與 session note（這次的體驗）**不重疊**
4. **可對書打分，分數可變動、要記錄變動**
5. session note **不必一天一筆**，可視情況拆數筆

## 💡 評分不另開檔（我最花時間想的一塊）

**寫進 session note 的 frontmatter**（`rating: 4` / `rating_changed_from: 3`），**變動史 = 各篇 rating 依時間排開**，`_index.md` 機械算趨勢。

理由：沒有第二份 store 就沒有對帳問題（basecamp 的 `recurrence` 13 vs origins 11 教訓）。而且**改分必須連帶寫 session note → 沒有理由的分數變動在結構上不可能存在**。與既有 `review --rating`（讀完對外推薦、一次性）分工清楚。

## 檔案結構

    letters/<persona>/reading/
    ├── _index.md                      機械生成（brief inline）
    └── <book-slug>/
        ├── 20260731_ch1-5.md          frontmatter: date/chapters/rating/range_source
        └── 20260731b_ch6-9.md         同日第二筆

`_index.md` **進度一律 derive 自 BookNotes，心得評分 derive 自 session notes**。frontmatter 帶 `generated_at` + 兩個 store 各自的來源計數（kaguya：讓讀者能自查新鮮度）。**任何 fragment 都不該再手抄閱讀進度。**

## 分階段（未動工）

| | 內容 |
|---|---|
| P0a | `library.py --reader` 缺席走身分階梯；歧義/失敗 → 拒絕列候選 |
| A | brief「📚 讀痕」節（3+1）+ `awakening.py reading [--all]` |
| B | session note 寫入 |
| C | `_index.md` 機械生成（**寫入後即重算**，非 morning-only）+ 跨 persona 對照 |

**相依**：P0a 依賴 `_lib/persona_resolve.py`（= P0b，2026-08-01 交給 @basecamp，他已開工）。
