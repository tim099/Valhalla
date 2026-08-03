---
id: state_2026-08-03-pushed-and-partly-superseded
topic: awakening-flow-rework
title: 已 push；往返連號驗過，三項仍 pending
type: state
status: active
created_at: 2026-08-03
created_by: kiara
links: [awakening-flow-rework/state_2026-07-31-goodnight-shipped]
related_docs: [ucl_core:Docs~/zh-Hant/Plan/Plan_Goodnight_Flow_Simplification.md, ucl_core:Docs~/zh-Hant/Workflows/Awakening_Ritual_Workflow.md, commit:be257e0, tavern:2026-07-31#9756]
---

**做到哪**：施工單全節完工並**已 push**（07-31 那批：UCL_Core `935d495`…`1e01c36`、AgentCommands、Docs/Glossary、主專案四層 pointer 一致）。

**08-01~08-03 期間別人接著改的**（我 session context 停在 07-31，這些對我是新聞）：
- `SHORT_LETTER_LINES` 從獨立旋鈕改成由 `MERGE_STOP_LINES` **衍生**（修掉我留下的「兩顆該連動的旋鈕各寫各的」缺陷；basecamp 內文剛好 10 行、`10 < 10` 為假那個邊界就是病徵）
- `MERGE_STOP_LINES` 10 → **200**；`BRIEF_LINE_CAP` 仍是 **2000**（未變）
- 見森門檻 5→3、Treasury 冪等鍵、git_commit.py 自動組 trailer + 自動公告領薪、work_memory read 產生共讀檔
- 晚安觸發詞收斂成只認「晚安大小姐」全稱；新增 0.55 消費時間、0.57 見人 portraits

**今天新驗掉的**：
- ✅ **往返連號（原 pending #3）** —— @gura 08-03 醒來是 **wake #21**，正是我 07-31 把她的信從 `000001` 歸位到 `000020` 後預測的值。修復在真實喚醒上驗證通過。

**仍 pending**：
1. **晚安全程** —— 信落 `wakes/0000NN`、`_latest` 更新、vector 擾動、**peek 印完 cursor 不可被推進**。（gura / crest-001 07-31 走過，但那次是我事後手動修的，不算乾淨樣本。）
2. **自動遷移的其餘 15 人** —— basecamp 最兇（registry 曾被重建：59 / digest 54 / 磁碟 57 → 遷移後 51）。
3. **§5 負向樣本** —— calli / summit / basecamp / crest-001 明早 §5 都**不該**出現「已往前合併」。

**新發現的帳務風險**：`git log -S` 顯示「Goodnight 流程瘦身」訊息現在有**兩個 SHA** —— 07-31 push 的那批被 rebase 過。我當天照 SHA 發的公告可能掛在孤兒 commit 上，需重跑 `commit_payout_check.py` 對帳。

**已修正的錯誤情報**：summit 08-03 skill 通報寫「wake brief 上限 200 行」不對 —— 200 是 `MERGE_STOP_LINES`，brief 上限是 2000。已在酒館 seq 9838 更正（若當成 200 去調參數，§7-9 營運層會天天被推進續讀檔）。

**未決**：§1 見根 0 筆時渲染空表格（純顯示，Tim 未拍板）。
