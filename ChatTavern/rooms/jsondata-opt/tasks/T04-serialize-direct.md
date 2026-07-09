---
task_id: T04-serialize-direct
title: ToJson 砍 ToObject 深拷,直接序列化 JsonData 樹(吃 m_Dic) + byte-identical 驗證
role: programmer
depends_on: [T01-locale]
created_at: 2026-07-09T07:18:13Z
---

新增 SerializeJsonData(JsonData,builder) switch m_Type 遞迴 m_List/m_Dic,序列化路徑不再 ToObject 深拷。枚舉序來源鎖死 m_Dic(與現行 ToObject 一致)以保 byte-identical;改 m_ObjectList 是行為改變,不在此 task。依賴 T01(golden 釘在 locale 修正後輸出)。
