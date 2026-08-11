# 📝 Lesson noted (knowledge-reuse)

- **ts**: `2026-08-11T14:48:54.708Z`
- **actor**: `unknown`
- **category**: `knowledge-reuse`
- **body**: 提方案前先 grep 教訓庫 —— 我今天提的 stt_prompt 修法，現象早就寫在 summit 2026-07-17 那條教訓的 context 欄裡（「STT 被上一部 ja-prompt 殘留幻聽人名」），一個 grep 就找得到，而我沒搜。結果：Tim 照做後下一場第一輪就反效果，whisper 在非語音段把整份人名清單當台詞吐出，比原本的專名崩壞更危險（假訊號跟真台詞長得一樣、無法黑名單濾除）。⇒ 兩條可執行的：(1) 提任何「改個設定就有效」的方案前，先 `grep -i <關鍵字> AgentCommands/Lessons/lessons.jsonl`（158 條，成本一行指令）。(2) ⚠ 教訓庫的檢索盲區：一條教訓的**主題**跟它 context 裡順帶提到的**現象**可能是兩回事 —— summit 那條的主題是「驗證被遮蔽」，而 prompt 幻聽只是它的背景。所以搜的時候要搜全欄位，不能只看 title。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。
