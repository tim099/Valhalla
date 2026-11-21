# 📝 Lesson noted (shipbuilding)

- **ts**: `2026-11-17T14:57:20.878Z`
- **actor**: `pinnacle`
- **category**: `shipbuilding`
- **title**: 舵模型命名避開 spin=rudder 與 metaRebase 撞名
- **tags**: `blockside`, `shipbuilding`, `rudder`, `spin`
- **body**: 在 Blockside `05_hull.js` 的 `metaRebase()` 裡，若模型 meta 的字串值跟同層關聯底下的某個模型同名，會自動被補上前綴（例如模型命名為 `rudder` ⇒ `hull/rudder`，結果把 `spin: "rudder"` 改寫成 `spin: "hull/rudder"`，導致 `shipcheck` 報 `meta spin=hull/rudder 不認得 ⇒ 不轉`）。因此造船時舵模型勿單獨命名為 `rudder`（可命名為 `rudder-main` 或 `舵`），避免與 `spin="rudder"` 撞名。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。
