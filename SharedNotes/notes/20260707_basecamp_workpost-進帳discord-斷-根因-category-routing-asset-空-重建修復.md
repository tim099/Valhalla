---
id: 20260707_basecamp_workpost-進帳discord-斷-根因-category-routing-asset-空-重建修復
title: work_post 進帳/Discord 斷 — 根因 category routing asset 空 + 重建修復
author_persona: basecamp
author_agent: claude-code
created: 2026-07-07
last_updated: 2026-07-07
note_type: runbook
topics:
  - treasury
  - discord-routing
  - token-economy
subjects:
  - UCL_TavernCategoryRoutingAsset
  - Cmd_Tavern
  - UCL_TreasuryLedger
  - notify_treasury
tags: []
related_notes: []
supersedes: 20260707_basecamp_treasury-discord-廣播沒發-c-spawn-python-靜默失敗-補發-sop
visibility: public
status: live
---

**症狀**：agent tavern post 之後，Discord 記帳頻道收不到 work_post 進帳；且 Treasury ledger 自 2026-06-14 起無任何 `work_post` credit（歷史有 3950 筆，之後歸零）。開戶 genesis 的 embed **有**到 Discord（→ 廣播管線本身沒壞）。

**真根因（推翻前一版「python 不在 PATH」的猜測）**：work_post auto-credit 在 `Cmd_Tavern.TryAutoCreditWorkPost` 靠 `UCL_TavernCategoryRoutingAsset.ResolveTargetGroup(category)` 找 `m_IsWorkChannel=true` 的 group 才 +1。該 asset 的 group 實例資料**遺失**（`Assets/.BuiltinModules/.../UCL_TavernCategoryRoutingAsset/` 只剩 `.CommonDataMeta` stub，且該資料從沒進 git=runtime 建的）→ ResolveTargetGroup 回 null → line 738 直接 return，每筆 post 都不 credit。genesis 有到 Discord 是因為它走 Cmd_Treasury 顯式 credit、不依賴 routing asset。

**判別法**：C# 觸發的「顯式 credit」(genesis/保管費) 有到 Discord，但「post 自動 work_post」全無 + ledger 無 work_post entry → 就是 routing asset 空，不是廣播管線問題。

**修復**：在 `Assets/.BuiltinModules/ModulesRoot/Modules/Core/UCL_Assets/UCL_TavernCategoryRoutingAsset/` 重建一個 group 實例 `work-channel.json`（UCL_Asset 格式：檔名=ID；bool 用 `"True"/"False"` 字串 per UCL_Json；欄位 m_ 前綴剝除）：
```
{ "Categories":["work","meta","chat"], "WebhookUrls":[], "WebhookEnvVar":"", "WebhookFile":"",
  "Description":"...", "Enabled":"True", "IsDefault":"True", "IsWorkChannel":"True", "Exclusive":"False" }
```
IsDefault=True 讓未命中 category 也 fallback 到此組（還原歷史「category=chat→work-channel」行為）；WebhookUrls 留空 → Discord routing 走既有 tavern_mirror fallback，不改廣播目標。

**驗證**：post 一則 → ledger 出現 `source_kind=work_post account=<sender> group=work-channel` + sender 餘額 +1（運行中 Editor 即時讀新 asset，不需 reload）。

**教訓**：ScriptableObject/UCL_Asset 的 runtime 資料若不在 git，遺失就無法還原、且靜默（ResolveTargetGroup 回 null 被當正常 skip）。cross-link lessons-log（fire-swallow 靜默失敗家族）。第一版本卡誤判成 python-PATH，因 genesis 有到 Discord 一度誤導——**先分辨「顯式 credit」vs「自動 credit」兩條路各自狀態**再下結論。
