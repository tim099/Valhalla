---
id: state_20260804_wait
topic: tavern-payout-and-args
title: 2026-08-04：wait 固化到 C# + 身分改以 persona 為主體（已 commit 841ab0c / dc05835）
type: state
status: active
created_at: 2026-08-04
created_by: summit
links: []
related_docs: []
---

wait 全案固化完成並實測。三隻靜默 bug：
1. op=wait 從來沒真的等過（71 筆全 since_seq=0、全 ≤3 秒、零 timeout）——
   背景迴圈 token 綁在 cmd 上，runner 的 using cts 一 dispose 就被取消並靜默吞掉。
   改 UCL_TavernWaitService（EditorApplication.update tick，狀態全在磁碟、服務無記憶）。
2. expect_from / --wait-reply-from 從來沒命中過 —— 只比 sender_id（agent 層），
   而 caller 填 persona 名。對 Myth/gura、Altair/apex-one、zeta/summit 全部失效。
   規格：wait 一律以 persona 為身分主體（IsSamePersona，優先比 sender_persona）。
3. client baseline 半套遷移（我自己引入）—— 匹配改 persona 但 _latest_message_key
   還用 sender_id 過濾，於是撈到舊的畸形發文當基準，0.0 秒假命中 code=0。

驗收含交叉隔離輪：apex-one 先回 → W2 命中 seq 10026 而 W1(expect_from=gura) 毫無反應；
24 秒後 gura 回 → W1 才命中 10027。**兩者命中 seq 不同才是隔離的硬證據。**
W3(expect_from=Myth，agent 名) 全程 timeout → persona-only 規格成立。

pending：Stage 2 的 python 薄 client 切換（把 client polling 換成呼叫 op=wait 再輪詢）未做。
現在 server 端正反向都驗過了，隨時可換。
