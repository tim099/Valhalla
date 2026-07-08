---
task_id: worknotes-v2-onboard
title: WorkNotes v2: note_type 軸 + onboard 殺手鐧 (擴充 shared_notes.py)
created_at: 2026-07-07T08:05:47Z
---

拍板案實作: 1) shared_notes.py add/frontmatter 加 note_type(map/concept/howto/decision/runbook); 2) 新增 onboard 子命令(給 subject/topic 回 map→concept→howto→decision→runbook 建議閱讀順序=見林先於見樹); 3) reindex 帶 note_type; 4) backward-compat 舊 note 無 type→預設; 5) fork 紀律+refs用subject不用file:line 寫進 spec doc. 依據 seq 8559 草案 + apex-one/summit feedback 拍板版。
