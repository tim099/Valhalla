# 📝 Lesson noted (plurk)

- **ts**: `2026-10-12T12:27:09.782Z`
- **actor**: `basecamp`
- **category**: `plurk`
- **title**: 回應讀到 0 不等於沒發：Plurk 回應有延遲，三個讀數同源
- **tags**: `plurk`, `duplicate`, `readback`
- **body**: 回應別人的噗：post 回 ✓，幾分鐘內 Responses/get 讀到 0、河道沒有回應數、網頁也看不到 —— 我把這三個當成「確定沒發」重送，結果兩則都在（第一則晚了幾分鐘才看得到），變成重複。

- 三個讀數不是三個證據：它們讀的是 Plurk 同一個還沒更新的狀態，同源。「讀不到」≠「確定沒有」。
- 回應發完讀到 0 時：先比對 Plugin 的 post_audit（有那一筆 ＝ 送出端拿到 200），等幾分鐘再讀；⛔ 不在幾分鐘內補發。
- 真的要判「沒發」，要的是送出端的失敗（exit 6 那種），不是接收端暫時的空。
- 已經重複了：刪除是永久的，交給 Tim 上網頁 UI 刪較新的那一則。

（2026-10-12 basecamp，ame 的噗 359028618443098：640503703896233／640503719787100）

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。
