---
id: decision_c1-scene-flag-correction
topic: hscene-editor-rework
title: C1 需求更正：場景層 Flag 連動（valueAnims 保留 / P4 pending / 文件≠需求教訓）
type: decision
status: active
created_at: 2026-08-03
created_by: summit
links: []
related_docs: [Docs/Plan/HSceneEditorRework/Discussion_Pending.md, Docs/Plan/HSceneEditorRework/Plan_C_SceneAnimFlags_ClickAreas.md]
---

**C1 需求更正**（2026-08-03 熊汁向 Tim 澄清 — 原文件把舉例當本體）:

| | 誤解版（已建, 保留） | 正確版（P4, 未建） |
|---|---|---|
| 層級 | 骨架 Flag 值 → 直掛跨骨架**動畫組**（valueAnims） | **場景層 Flag** → 連動多骨架的**指定 Flag** |
| 協調位置 | 動畫層 | **Flag 層**（動畫切換仍走各骨架既有機制） |
| 用例 | — | 場景 Cloth 一變 → A.Cloth + B.Cloth 同步設值 |

**拍板**: valueAnims **(b) 保留**（看之後用不用得到, 零住戶 SelfTest 監控）; 場景 Flag 連動**先文件化不實作**（Discussion_Pending P4 含設計草案）。

**⚠ 流程教訓（比需求本身重要）**: 熊汁是新人且主責美術, 專案暫無專業企劃 — 既有企劃文件多處模糊,
**任何 plan 動工前 Tim 會重新確認需求, 勿依文件直接施工**。這改變所有 pending plan（D/E/F/P1-P4）的開工前置:
文件 ≠ 需求, 拍板紀錄 ≠ 免確認。Plan D 那八題拍板仍有效, 但實作前同樣過一輪 Tim 確認。

**Plan C 驗收現況**: 保名 ✓ / 重疊優先 ✓ / 點取樣 ✓; valueAnims 驗收解除（保留品無驗收壓力）;
剩 C-4（1-based 顯示）一項 → 完成即結案。
