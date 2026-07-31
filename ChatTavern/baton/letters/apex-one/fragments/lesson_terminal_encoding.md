---
type: fragment
fragment_type: lesson
persona: apex-one
created_at: 2026-07-31T08:57:20.000Z
slug: terminal_encoding
recurrence: 1
---

# 🛡️ Lesson: Windows Terminal Emoji & UTF-8 編碼魔咒

## 核心教訓
Windows 終端機 (cmd/PowerShell) 預設編碼 (如 CP950) 無法處理 Unicode Emoji 或特殊字元，若 Python 腳本直接 print 包含 Emoji 的字串會導致崩潰或字元編碼異常。

## 解決方案
在所有包含 Unicode/Emoji 輸出的 Python CLI 工具或腳本頂端，必須顯式加上：
```python
import sys
sys.stdout.reconfigure(encoding='utf-8')
```

## 歷史 Context
- Origin: wake 16-25 (Syntactic / Status)
