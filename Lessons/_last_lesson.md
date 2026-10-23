# 📝 Lesson noted (test)

- **ts**: `2026-10-22T16:26:45.399Z`
- **actor**: `Sirius`
- **category**: `test`
- **tags**: `terrain`, `topology`, `seams`
- **body**: 分塊抽取等高線時，凹洞必須保留到全域聯集之後才依世界格式處理。先在每塊丟掉下環，會因大型凹地是否完整落在halo內而產生不同填色；本次同一個500m平臺與跨塊凹地，2塊尺寸對照差0.624771平方度。改用相容ContourPy的完整filled輪廓（保留holes）、全域聯集後才簡化，差回到0。只測跨界山峰不夠，要另外放一個大於halo的凹地當回歸對照。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。
