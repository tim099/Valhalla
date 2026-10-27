# 📝 Lesson noted (shipbuilding)

- **ts**: `2026-10-27T12:14:06.535Z`
- **actor**: `gura`
- **category**: `shipbuilding`
- **title**: 甲板站人高度照最靠船頭的砲：舷頂迴旋砲在前 ⇒ 取用點消失
- **tags**: `blockside`, `shipcheck`, `swivel`
- **body**: 造船匯進 Blockside：一層甲板的站人高度（D.zr）是照那一層「最靠船頭的那一門砲」定的（10_ship.js gunDecksMeta 的 main；sh.guns 由船頭往船尾排）。舷頂上的迴旋砲如果比舷側砲更靠船頭，zr 會被量在舷頂高度、甲板面不在裡面 ⇒ 那一層找不到取用點（匯入檢查 ✗ 取用點，寫了 hoist 也一樣）。飛魚號 TASK-0971：船頭那對迴旋砲（x 199、z 42）在 4 磅砲（x 178）前面 ⇒ 主甲板 zr 34–47、甲板 z 31。修法：迴旋砲擺在最前面那門舷側砲的後面。查法：?debug=1&shipcheck=<id> 之後看 __game.ships()[0].decks 的 zr 與 guns 順序。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。
