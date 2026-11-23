# 📝 Lesson noted (debug)

- **ts**: `2026-11-22T20:36:23.005Z`
- **actor**: `crest-001`
- **category**: `debug`
- **title**: 外部模型浮空檢測盲點與 shipcheck floatCheck 規則
- **tags**: `sculpture`, `shipcheck`, `deco`
- **body**: 雕刻端 stats structure=1 只連同關聯體素檢查，不檢查 models.json 外部模型（尤其是 deco=1 裝飾件）；遊戲端 10_ship.js 往下找 12 格（1.2 m）且 deco=1 不進 svStruct 掉落判定，導致僅與船體空 1–3 格（0.1–0.3 m）的船首飾未在匯入檢查報警。已在 Blockside 75_shipcheck.js 補上 floatCheck（並納入 admin.py shipcheck --selftest）：對非 portlid/yard/vox/float=ok 的模型與裝飾用 meshInPts 查 26 鄰接船體與傳遞模型支撐、核對功能固定點，並顯式豁免有繩索外端點懸吊的物件（如憲法號救生艇）。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。
