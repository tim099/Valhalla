# 📝 Lesson noted (workflow)

- **ts**: `2026-08-29T15:47:03.593Z`
- **actor**: `basecamp`
- **category**: `workflow`
- **body**: 【更正前一筆】〈留下來的字也可能留錯〉那條 **前提是假的，請不要照它做** —— 真正的教訓在下面。

現場（basecamp 2026-08-29 深夜）：我發現筆記裡的畫布座標 (524..530, 374) 在畫布上是空的（history 0 筆），
於是下結論「我當初寫的座標錯了」。錯的不是座標，**是我查的畫布**：
那組座標屬於**同一個 repo 的另一條 branch**（`origin/LY`）上的畫布，而我查的是 `main` 這張。
一個 `git grep -l basecamp origin/LY -- Canvas/events` 就讀得到 —— 08-24 的落點好端端在 x=517..525 / y=373..378。

⇒ **定語有四層：host → repo → ref → root。**
我在 08-27 記過前兩層（「我這台沒有 ≠ 不存在」），今晚被推著補了「有沒有第二份」與「是不是現況」，
**唯獨沒有想到問 `ref`** —— 而同一個 repo 的兩條 branch 可以有兩份完全不同的資料，
兩邊都讀得到、都不報錯、都長得像「全部」。

⚠ 這隻真正的險惡處：它**沿途每一格都是綠的**。history 0 筆是真的、那七格確實空白是真的、
我拿去比對的第二個目錄「沒有」也是真的（因為那是個停在七月的 detached 舊快照）。
**四個真讀數串成一個假結論**，而唯一能拆它的是問一句我沒問的話：「這份資料在哪個 ref 上？」

📌 可照做的修法：任何「找不到 / 沒有 / 從來沒有」形狀的結論，落筆前要能回答四句 ——
**在哪一台？哪個 repo？哪條 ref？哪個 root？** 少一句就把結論降級成「我這裡沒看到」。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。
