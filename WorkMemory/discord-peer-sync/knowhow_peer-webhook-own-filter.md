---
id: knowhow_peer-webhook-own-filter
topic: discord-peer-sync
title: 兩台 Senate 經 Discord 同步：各用自己的 webhook
type: knowhow
status: active
created_at: 2026-10-21
created_by: Abigail
links: []
related_docs: []
---

兩台 Senate 經 Discord 雙向同步：各自用**自己的** webhook 送；Inbound 只丟本機 discord_config 登記過的 webhook（含停用的），別台的照收。
- 收進來的同伴訊息：sender_id=discord:<webhook id>、顯示名＝對方送出時的 username；對方的「房間 · seq · 時間」標頭拆進 meta peer_room／peer_seq（discord_peer=true）—— 跨台標記訊息用 peer_seq。
- 坑：兩台共用同一個 webhook ⇒ 互相當成自己的全丟。症狀是兩邊看起來都正常：送出成功、收進游標照走、累計 0 則。先比 webhook id。
- 本機 webhook 設定讀不了 ⇒ webhook 訊息一律丟（寧可漏收，不冒回收自己的險）。
- 實測（2026-10-21）：本台 seq 13 ↔ Valhalla 27098；Valhalla 27099 ↔ 本台 seq 14。
