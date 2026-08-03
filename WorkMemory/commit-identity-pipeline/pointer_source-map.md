---
id: pointer_source-map
topic: commit-identity-pipeline
title: 檔案地圖：code / 資料 / 規範 / 出處
type: pointer
status: active
created_at: 2026-08-03
created_by: basecamp
links: []
related_docs: []
---

接手這條線先讀這裡，別重探索。

## Code

| 檔案 | 職責 |
|---|---|
| `Tools~/AgentCommands/git_commit.py` | **唯一提交入口**。組 trailer + 自動公告 + 領薪提示 |
| `Tools~/AgentCommands/agent_email.py` | 信箱解析（`resolve` / `list` / `trailer`），只讀不寫 |
| `Tools~/AgentCommands/agent_model.py` | 型號解析 + agent 名翻譯 + `format_trailer_model`（vendor/version） |
| `Tools~/AgentCommands/hooks/commit-msg-validate.py` | hook 本體，只擋「有 trailer 但對不上」 |
| `Tools~/AgentCommands/install_hooks.py` | 裝進所有層 repo；`--check` 查覆蓋率 |
| `…/AwakenInit/UCL_AgentEmailRegistry.cs` | C# 端信箱解析（後台用） |
| `…/AwakenInit/UCL_AgentModelRegistry.cs` | C# 端型號／廠牌解析。**`SaveAll` 兩張表一起寫** |
| `…/UCL_EditorMenuPages/UCL_PersonaAgentAdminPage.cs` | 📧 信箱設定 / 🏷 型號設定 —— **唯一設定入口** |

## 資料

| 檔案 | 內容 |
|---|---|
| `AgentCommands/AwakenInit/agent_emails.json` | `defaults[actual_agent]` + `fallback` |
| `AgentCommands/AwakenInit/agent_models.json` | `models[actual_agent]`（翻譯用）+ `vendors[actual_agent]` |
| `AgentCommands/AwakenInit/personas/<p>.json` | `email` override、`model`、`actual_agent` |

## 規範

`Skills~/ucl-commit/SKILL.md`（127 行，已瘦身）—— 只留人要做的判斷與工具管不到的三條
（一則一 SHA / 同 SHA 別貼兩次 / rebase 會讓帳掛孤兒 SHA）。

## 出處

四提案的討論與投票在酒館 2026-08-03（`tag:design-discussion`）；
拍板者：Tim（信箱／型號翻譯／工具化方向）、meadow（B 的 (a)+(b)、`--bump-of`、寫入/讀取分離）、
apex-one（Alert Fatigue、不剝前綴）。
