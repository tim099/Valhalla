---
id: pitfall_self-declared-field-as-identity
topic: treasury-bank-hardening
title: 用寫入端自己填的欄位判斷作者 — 一天錯四次，每次結論都很乾淨
type: pitfall
status: active
created_at: 2026-08-04
created_by: summit
links: []
related_docs: []
---

**症狀**：想知道「這筆 ledger entry 是 C# 寫的還是 python 直寫的」，於是去看 entry 的欄位。

**我在同一天錯了四次，每次都得出一個看起來很有把握的結論：**

| 次 | 判準 | 結論 | 真相 |
|---|---|---|---|
| 1 | 有沒有 `signature` / `caller_agent_id` 欄 | 「6730/6730 **全部** python 直寫」 | 欄位名根本不存在 |
| 2 | 有沒有 `sig_*` 欄 | 「6730/6730 **全部** C# 寫」（正好反過來） | canvas.py **自己填 `sig_*`** |
| 3 | `sig_env_marker` 是否 `manual_filesystem_write*` | 找出 1,144 筆 | 漏掉 `work_session_prototype` 那 227 筆 |
| 4 | 用「有無活呼叫端」判斷能不能刪 | 以為 `session_common` 可刪 | `stream_watch_session.py` 正在用 |

**根因（一條，四次都一樣）**：
**我用「寫入端自己填的欄位」當作者判準。** 那個欄位偽造成本為零 ——
canvas.py 直寫時就填 `sig_env_marker = "manual_filesystem_write_canvas"`，
於是「有 sig_* 就是 C# 寫的」這個推論從一開始就不成立。

同型：早上 wait 的 `sender_id` 也是寫入端填的，所以拿它當「誰說的」判準對
「agent 名 ≠ persona 名」的人全部失效。**同一個病，一天內在兩個系統各咬一次。**

**正確做法**：
1. 判斷作者不要看「有沒有欄位」，要看**欄位的值**，而且要先確認那個值不是自由填的。
2. 真的要不可偽造，得由**唯一寫入點**產生（例如只有 C# 能寫的簽章 + 拒收缺簽章的 entry），
   否則任何欄位都只是「寫入端的自我宣告」。
3. 刪任何東西前，呼叫端搜尋範圍要**含 UCL_Core 內的 Tools~**，不能只搜主專案
   —— 第 4 次就是漏搜那裡。

**元教訓**：這四次錯誤有個共同的危險特徵 ——
**每一次的結論都很乾淨（6730/6730、1144 筆），乾淨的數字讓人以為問題已經解決。**
中間三次如果沒有繼續往下查，任何一次都會變成「已查證」寫進報告。
乾淨的普查結果不是正確的證據，只是「這個判準被一致地套用了」的證據。
