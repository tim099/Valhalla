---
task_id: T02-O4-runcmd
title: O4: run_cmd.py 偵測入場 Op 自動 wait-reply=0
role: programmer
created_at: 2026-05-08T23:19:45Z
---

修改 run_cmd.py，當偵測到 op 屬於 (read, inbox_read, get_presence) 等進場與查詢類 Op 時，自動 override 設為 wait-reply = 0.0，實現最省時的 Quick Win。
