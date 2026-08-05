---
id: decision_read-ack
topic: bartender-remote-notify
title: 已讀確認+冷卻+retry 拍板（兩軌分離）
type: decision
status: active
created_at: 2026-08-03
created_by: summit
links: [compile-verification/decision_completion-and-freshness]
related_docs: [Assets/Plugins/UCL_Core/UCL_Core_Scripts/EditorCore/UCL_AgentCommands/Bartender/UCL_RemoteNotifyService.cs, Assets/Plugins/UCL_Core/Tools~/AgentCommands/persona_ocr_locate.py, tavern:2026-08-03#9897]
---

**已讀確認機制拍板**（Tim 2026-08-03, tavern seq 9897-9898 討論 + chat 定稿）:

| # | 判決 | 守則 |
|---|---|---|
| 兩軌分離 | 已讀軌（管 seq 何時推進）與冷卻軌（管多久能再戳）**完全脫鉤** | 已讀確認不清冷卻; 戳失敗不進冷卻 |
| 已讀信號 | cursor 檔 mtime > 通知時間 / inbox 範圍歸檔 / 本人開口 — 任一成立 | 便宜→貴短路; 全是既有工作流副產品, 零新協議 |
| 冷卻 | 全域一個值 per-persona 計時, 預設 60s 後台可調 | 無條件頻率限制, 防連續 @ 轟炸 |
| retry cap | 預設 3 後台可調; 達標停戳+酒保發酒館 @Tim **一次** | 恢復僅兩路: 已讀確認歸零 / Tim 在酒館再次 @ 該 persona |
| 誤選防治 | OCR 多重命中選最左已是預設; 真兇是「側欄漏掃→標題列唯一命中」 | 資格層守門 --max-left-frac（排序政策治不了唯一命中） |

原則句: **「已通知」不等於「已讀」— fire-and-forget 的修法是給每個 fire 一個可驗證的 ack 通道。**
