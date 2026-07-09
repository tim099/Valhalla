---
task_id: T02-getcollection
title: GetCollection None→null 修讀取副作用(Heisenbug) + grep 遷移可疑 caller
role: programmer
created_at: 2026-07-09T07:18:10Z
---

GetCollection() 對 None 回 GetIDic() 會 mutate m_Type→Dictionary。改 None→return null(Count 已有 null→0)。grep new JsonData() 後直接讀 Count/枚舉期望變 Dict 的 caller 遷顯式賦型。
