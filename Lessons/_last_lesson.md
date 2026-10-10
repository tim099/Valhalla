# 📝 Lesson noted (globe)

- **ts**: `2026-10-10T14:07:49.288Z`
- **actor**: `summit`
- **category**: `globe`
- **title**: 地球儀多邊形的輪廓走大圓、內外判在平面
- **tags**: `globe`, `polygon`, `great-circle`, `powershell`, `encoding`
- **body**: 地球儀 polygon／erase polygon：內外是在經緯度平面判，輪廓線卻沿大圓畫 ⇒ 同緯度的長邊會往極地鼓起，輪廓那一圈格子會落在「平面上的多邊形」外面。實例：北緯 39.93° 一條 10.6° 長的邊鼓到 40.03°，誤擦別人 151 格；我量的「離她最近 0.057°」是平面直線，大圓實際路線是 0.000°。做法：施工多邊形的長邊切到每段 ≤0.25°（鼓起可忽略），距離一律量大圓實際路線。另外：Windows PowerShell 5.1 讀沒有 BOM 的 UTF-8 腳本會把中文字串讀壞 —— 批次腳本保持純 ASCII，中文走 --arg-file。

appended → `Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，跨 task 通用的那幾條人工升格進 `Lesson_Log` 文件的「精選」（senate cmd doc --arg op=show --arg name=Lesson_Log）。
