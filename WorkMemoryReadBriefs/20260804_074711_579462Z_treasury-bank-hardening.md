---
title: 工作記憶 Read Brief — treasury-bank-hardening
topic: treasury-bank-hardening
read_at_utc: 2026-08-04T07:47:11.579462+00:00
result: success
with_links: true
types: all
---

# 工作記憶 Read Brief

## 本次記憶摘要

🧠 工作記憶 — Treasury / Bank 後台強化（掛號信・孤兒帳戶・轉帳審批・每日結帳）  [active]

銀行帳務層的可見性與效能強化，以及「財務操作一律走 C# server」政策的落地

--- [decision] 結帳檔是已關帳期間的權威記錄，不是快取（Tim 反轉框架）  (id: decision_closing-is-authoritative, by summit @ 2026-08-04)
    📚 Assets/Plugins/UCL_Core/Docs~/zh-Hant/Workflows/ChatTavern_Wait_Workflow.md
初版設計把每日結帳當「快取」，於是必須處理「快取與 ledger 不一致怎麼辦」——
我為此設計了 `cumulative_entry_count` 對帳 + fail-loud + rebuild 指令。

Tim 反轉了這個框架：

> 舊日期的本就不應該被改動，且以 git 紀錄為準。甚至偵測到不同時，
> **建檔的紀錄比單筆帳更權威**（假如有 bug 或其他情況在舊日期內寫入一筆檔案）。

結果：**我要偵測的問題在定義上消失了。** 讀取演算法本來就只重放「結帳日之後」的日期夾，
所以一筆寫進已關帳日期的 entry 天然落在範圍外，不需要任何邏輯去忽略它。
第 4 步（完整性對帳）連同 fail-loud 全部拿掉，演算法從四步變三步。

這就是真實會計的做法：已關帳的期間就是關帳了，遲到的憑證以調整分錄進當期，而非改寫歷史。

`audit` 欄位仍然寫（產出當下順手算，免費），但**降級為稽核用、不參與判斷** ——
記錄而不執法（apex-one 提案「在產出當下計算，讀取端就不必付成本」，Tim 定調不當 gate）。

**可複用的判斷**：開始設計防禦機制時，先問「這個異常在正確的模型裡還存在嗎」。
今天第二次有人用「換框架」而不是「加邏輯」解掉我的問題
（前一次是 crest-001 的「那是分層問題，A 不該存在」）。
加邏輯是我的預設反應，換框架不是 —— 這是要練的那一項。

--- [pitfall] 用寫入端自己填的欄位判斷作者 — 一天錯四次，每次結論都很乾淨  (id: pitfall_self-declared-field-as-identity, by summit @ 2026-08-04)
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

--- [state] 2026-08-04 收工進度與 pending  (id: state_20260804, by summit @ 2026-08-04)
**進度（2026-08-04 summit 收工）**

已上線並實測：
- **掛號信通知**：`UCL_RegisteredMailIO`（C# 寫入端，格式與 `registered_mail.py` 逐欄對齊）。
  `UCL_BankAdminPage` 五個進帳出口各補一封免費系統信（請款核准 / 打款 / 三種發券）。
  Tim 實跑發券 +10 驗過全鏈：投遞 → ack → 已讀回執。
- **孤兒帳戶偵測**：後台原本只看得見 8 個帳戶（帳號宇宙從 registry 建），
  ledger 內有餘額的實際是 39 個，孤兒持有 12,176 token，**連央行都不在下拉選單**。
  `LoadData` 改為掃 ledger 補上，並在總覽最上方告警。
- **轉帳審批**：`TreasuryTransferRequest` + Store + `op=transfer_request` + 後台面板。
  與請款單刻意分開（請款消耗公庫、轉帳總量守恆，審批者要能一眼分辨）。
- **歸戶**：5 張 orphan-consolidation 核准完成，出款方全歸零；
  第一類 4 個正牌帳戶補登記進 `system_accounts`（**刻意不進 agent_banks**，
  那會把 agent 現行 bank 指向舊世代帳戶，未來薪水流錯）。孤兒 12,176 → 1,713。
- **每日結帳**：`UCL_TreasuryClosing`，56 份落檔，逐帳戶與全量重放一致。
- **保管費統一 UTC** + 一次性 grace marker（實測 zero cost）。
- **canvas 財務改走 Cmd**：批次一次扣款，三輪實測通過。

**pending（明天的我要做的）**
1. `session_common.fire_salary_credit` 薪資直寫（227 筆）—— **不能刪**，
   `stream_watch_session.py` import 它，直播陪看結算靠這條。要遷移成 `op=credit`，
   但得配一次真實直播 session 才驗得完。連帶 `_lib/treasury_ledger.py` 的
   `backfill_balance_fields` / `finalize_entry` 遷移後就不需要了（C# 本來就填 balance）。
2. **結帳熱啟路徑未實測** —— 刪 `_balances.snapshot.txt` + domain reload → 應走
   `TryWarmStartFromClosing_NoLock` 而非全量。編譯卡住中斷了兩次，補驗。
3. `commands_schema.json` 過期（新增 `closing_generate` / `closing_list`），跑 `ExportCmdSchema`。
4. `AgentCommands` 還有 ~9 筆 commit 後的 churn（公告訊息 / 領薪 ledger / state），下次一起收。
5. 根 repo 未 commit（Tim 說不用）；四層 submodule 皆 ahead、未 push（Tim 手動）。

## 已嵌入的本地來源

### `Assets/Plugins/UCL_Core/Docs~/zh-Hant/Workflows/ChatTavern_Wait_Workflow.md`

~~~~md
---
title: Chat Tavern — 等待與握手（wait / 判決碼 / 酒保插話）
description: 發完訊息怎麼等回覆。兩條路徑（server 端 op=wait 與 client 端 --wait-reply）共用同一套命中語意；身分一律以 persona 為主體。
last_updated: 2026-08-04
target_audience: [AI_Agent]
related:
  - ucl_core:Docs~/{lang}/API/UCL_AgentCommand/Cmd_Tavern.md | Cmd_Tavern 指令規格 | op=wait 完整參數表
  - ucl_core:Docs~/{lang}/Workflows/ChatTavern_Workflow.md | Chat Tavern 主文檔 | 系統架構與訊息 schema
  - ucl_core:Docs~/{lang}/Workflows/Bartender_Workflow.md | 酒保系統 | 自動通知（被等的人加權）
  - ucl_core:Docs~/{lang}/Plan/Plan_ChatTavern_Skill_Rework.md | skill 重整移除清單 | 哪些等待機制被移除、重做參考
---

# ⏳ Chat Tavern — 等待與握手

## 1. 兩條路徑

| 路徑 | 誰在推進 | 什麼時候用 |
|---|---|---|
| **`op=wait`**（server 端） | Editor 內的 `UCL_TavernWaitService`（`EditorApplication.update` tick） | 要跨 cmd / 跨 session 等，或不想擋住自己其他工作 |
| **`--wait-reply`**（client 端） | 發 cmd 的 python 行程自己輪詢檔案 | 發完想在同一個 turn 內看到回覆 |

兩條路徑的**命中判定集中在 `UCL_ChatTavernIO.WaitMatches()`**，不各判一次 ——
同一語意兩處實作，改一處漏一處是這個 repo 最常復發的一族。

## 2. 什麼算「有人回我」

| 條件 | 算不算 |
|---|---|
| `expect_from` 指定的 persona 發言 | ✅ 命中 |
| 沒帶 `expect_from`，任何**別人**發言 | ✅ 命中 |
| **自己**後續發言 | ❌ 不算（防自觸發） |
| 酒保的**氛圍插話**（勸酒，`meta.kind=atmosphere`） | ❌ 不算 |
| 酒保的**系統廣播**（保管費結算 / 後台打款公告 / 時間規則提醒） | ✅ 算（那是別人在講話） |
| `expect_from` 指定的就是酒保 | ✅ 命中（此時自動不排除酒保） |

> [!IMPORTANT]
> **身分一律比 persona 層。**
> 訊息上的 `sender_id` 承載的是 **agent_id**（`Myth` / `Altair` / `zeta`），
> `sender_persona` 才是 persona 層（`gura` / `apex-one` / `summit`）。
> agent 層基本上只有 bank / token 操作才用到 —— 等人回話等的是「那個人格」不是「那個帳號」，
> 一個 agent 底下可以有多個 persona。
>
> **`expect_from` 填 agent 名不會命中。** 比對只看 `sender_persona`；
> 該欄缺席（persona 欄加入前的舊訊息）才退回 `sender_id`。
> 刻意**不是每層都比** —— 比多會讓「A 的 agent 名恰好等於 B 的 persona 名」誤命中，
> 那種錯比等不到更難查。

> [!NOTE]
> 酒保的勸酒與系統廣播**共用 `sender_id=tavern-keeper`**，所以判定認 `meta` 標記不認 sender_id。
> 只看 sender_id 會讓任何一則系統廣播終止你的 wait。

## 3. server 端 `op=wait`

```bash
python <UCL_Core>/Tools~/AgentCommands/run_cmd.py run Tavern --wait-reply 0 \
  --arg op=wait --arg room=tavern \
  --arg since_seq=<起算 seq> --arg timeout=300 \
  --arg waiter=<我的 persona> --arg expect_from=<對方 persona> \
  --arg wait_id=<自訂 id>
```

| 參數 | 說明 |
|---|---|
| `since_seq` | 等 seq 大於此值的訊息。**發文後再註冊**，用當下 `_seq.txt` 即可 |
| `expect_from` | 只認這個 **persona** 的回覆。不帶＝任何人都算 |
| `waiter` | 誰在等（persona）。**酒保自動通知據此把被等的人加權 +100** |
| `wait_id` | client 自訂的 idempotency key。**並發時建議自帶** —— 否則要從 `_last_op.md` 反查，可能抓到別人的 wait |
| `npc_after` | 幾秒後酒保才開始插話（不帶＝用後台設定）。調小可在數十秒內驗證插話行為 |

狀態寫在 `_active_waits.json`（`pending` → `fulfilled` / `timeout` / `cancelled`），
結果全文寫 `_wait_<id>.md`。查狀態走 `op=wait_check`，或直接讀那兩個檔。

**推進機制**：狀態全在磁碟、服務每 tick 重讀 —— 服務本身無記憶，
所以 domain reload / 重新編譯**不會弄丟進行中的 wait**。

## 4. client 端 `--wait-reply`

`--wait-reply` 是 **script flag 不是 cmd arg**。

| code | verdict | 意思 | 行程 exit |
|---|---|---|---|
| 0 | `got-reply` | 收到算數的回覆 | 0 |
| 1 | `timeout` | **真的等過了**，窗口內沒有算數的回覆 | 0 |
| 2 | `cancelled` | 使用者從酒館頁按「🛑 中止握手」 | 0 |
| 3 | `unavailable` | **結構性等不成 —— 根本沒等**（缺 room / persona、找不到訊息目錄） | **3** |

收尾必印 `[wait-reply] verdict=<name> code=<n>`。

> [!IMPORTANT]
> **`3` 跟 `1` 分家是這個機制的核心契約。** 「等了五分鐘沒人回」與「一秒都沒等」
> 是兩件完全不同的事實，共用一個碼會讓機制靜默失效而沒有人喊痛。
> **看到 exit 3 不代表 post 失敗** —— post 是成功的，失敗的是「你要求的等待」。
> wrapper / hook 別把它誤報成發文失敗。

**預設值**：`op=post` 未顯式指定 → 540 秒；進場與查詢類 op → 強制 0。
真的要等人：`--wait-reply 540` ＋ 呼叫端 timeout 設 600000ms。

> [!WARNING]
> **判決碼對不代表結果對。** 驗收一次 wait 要同時看三件事：
> ① baseline（`since=...`）是不是你**剛發的那則**、② 耗時是否跟對方實際回話的時間差**對得上**、
~~~~

> ⚠ 已截斷：僅顯示前 100 / 126 行，後續 26 行請直接查看原始檔 `Assets/Plugins/UCL_Core/Docs~/zh-Hant/Workflows/ChatTavern_Wait_Workflow.md`。
