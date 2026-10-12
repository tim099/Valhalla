# 📝 Lesson noted (workflow)

- **ts**: `2026-10-12T09:48:07.211Z`
- **actor**: `summit`
- **category**: `workflow`
- **title**: ui 的動作旗標預設轉給常駐視窗 —— 測自己的頁要 --local
- **body**: `senate ui` 帶 --click／--set／--toggle／--fold／--list／--json 時，預設**轉給常駐視窗**回答（輸出第一行「⤷ 由常駐視窗回答 pid=…」），動的是使用者開著的那顆窗。
要在本地畫（例如用新編的 bin/ exe 測自己的頁）一律加 `--local`；第一行會印「⚠ --local：以下是 CLI 自己畫的一棵樹」。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。
