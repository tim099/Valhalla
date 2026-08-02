# 遠端視窗協作測試診斷

- 時間（UTC）：`2026-08-02T12:51:52.9472818Z`
- 指定 agent：`Claude Code`
- 使用者靜置秒數：`0.015`
- 切換前 foreground：`0x300D8` | pid=`101700` | process=`Unity` | title=`Bar - Boot - Windows, Mac, Linux - Unity 6.3 LTS (6000.3.5f2) <DX12>`
- 切換後 foreground：`0xB0FC6` | pid=`66868` | process=`Claude` | title=`Claude`
- 選定 hwnd：`0xB0FC6`
- SetForegroundWindow：`True`
- 結果：已切換到「Claude」

## 可見候選視窗
- hwnd: `0xB0FC6` | pid: `66868` | process: `Claude` | process-hit: `True` | title-hit: `False` | title: `Claude`

## 全部可見 top-level 視窗
`0x20A54` | pid=`107800` | process=`Explorer.EXE` | title=``
`0x101C2` | pid=`107800` | process=`Explorer.EXE` | title=``
`0x101FC` | pid=`107800` | process=`Explorer.EXE` | title=``
`0x20BEC` | pid=`101700` | process=`Unity` | title=`Console`
`0x300D8` | pid=`101700` | process=`Unity` | title=`Bar - Boot - Windows, Mac, Linux - Unity 6.3 LTS (6000.3.5f2) <DX12>`
`0x30A08` | pid=`63004` | process=`ChatGPT` | title=`ChatGPT`
`0x10984` | pid=`18176` | process=`Fork` | title=`Fork`
`0xB0FC6` | pid=`66868` | process=`Claude` | title=`Claude`
