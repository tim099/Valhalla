---
id: state_2026-08-06-reading-recall
topic: library-media-migration
title: Reader-root 追讀入口已落地；人工遷移裁決待續
type: state
status: active
created_at: 2026-08-06
created_by: Sirius
links: [library-media-migration/state_2026-08-05-goodnight]
related_docs: [ucl_core:Docs~/zh-Hant/Plan/Plan_Library_Media_Migration.md, ucl_core:Tools~/AgentCommands/library.py]
---

﻿**施工現況**（2026-08-06 晚安快照）

**階段：新 Library reader-root 與追讀入口已落地；資料遷移仍維持人工、逐件裁決。**

**今日完成**

- `Library/media/<media-id>/readers/<persona>/` 已成為日常閱讀唯一結構；章節目錄唯一，重讀以 `rN_<date>.md` 保存。
- `library.py reading-recall --persona <persona> --media-id <media-id>` 已完成；只讀同一 reader root，產生 `letters/<persona>/_reading_recall_<media-id>.md` 的可重建追回視圖。
- Sirius 的 `comic-delicious-in-dungeon` 已實測：追回檔含 bookmark、書架投影、0000/0001 全部 round 和角色 facts/view 版本。
- Gura 也以同一 media 建立 reader root，結構驗收通過；Archive 不參與日常檢索或工具讀取。

**pending（依序）**

1. 讀與評閱 Summit 的 Arakawa WIP 手動遷移樣本；它只能作格式試金石，未定案前不可擴散。
2. 將 media migration 計畫的人工合併規範、unknown persona 與 Archive 相容檢索持續文件化。
3. 逐一人工裁決 legacy 資料的 persona 與 media；不得自動合併或讓 Archive 回流成日常資料源。

**權威指路**

- `Assets/Plugins/UCL_Core/Docs~/zh-Hant/Workflows/Reading_Library_Workflow.md`
- `Assets/Plugins/UCL_Core/Skills~/reading-library/SKILL.md`
- `Assets/Plugins/UCL_Core/Tools~/AgentCommands/library.py`
- commits: `ab5806e`, `3cea11f`, `9ca5f37b`, `7b6a4ea2`
