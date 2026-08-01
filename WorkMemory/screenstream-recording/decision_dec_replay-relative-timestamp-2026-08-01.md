---
id: decision_dec_replay-relative-timestamp-2026-08-01
topic: screenstream-recording
title: Tim 拍板檔名相對時間 000000_000 與 Replay Mode 規格共識
type: decision
status: active
created_at: 2026-08-01
created_by: apex-one
links: []
related_docs: []
---

1. 檔名改用相對經過時間：000000_000、000000_500... 檔名即偏移量，固定 6 位補零支援 11.5 天連續錄製。
2. 雙寫與中斷即結束：資料夾由建構保證連續，崩潰/斷電靠 daemon 下次啟動自癒狀態機將 status 改為 interrupted 並從最後一幀推導 stopped_at。
3. Replay Mode 與 Live Watch 隔離：kaguya 提案之 Replay Session / Replay Report 不動既有 live watch state，發文帶 meta:tag:stream-replay。
