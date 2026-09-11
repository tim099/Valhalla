# 📝 Lesson noted (workflow)

- **ts**: `2026-09-11T01:19:47.229Z`
- **actor**: `kiara`
- **category**: `workflow`
- **title**: 動不了受測體時，把形狀搬到獨立 runtime 並排跑 —— 但 BEFORE 要真的重現、射程要顯式
- **tags**: `verification`, `reverse-control`, `scope`, `unity`
- **body**: 改完一個「錯了會炸／會卡」的形狀，驗它不一定要動共用 Editor —— 可以把**形狀**搬到獨立 runtime 上並排跑。

【現場】2026-09-11 三張 Unity UI 的 NullRef／旗標單（HButton ×2、HActionPanels ×1）。
真正的執行期重現要在共用 Editor 上刻意弄壞東西（灌一個必丟例外的事件／改壞 sprite ID／餵空清單），
代價落在當時在場的別人身上。於是我一開始只寫「編譯綠不是行為綠」，一格都不勾。

【做法】把**修法前後兩種寫法**抄成 30 行的 console 專案（dotnet，獨立編譯器＋獨立 runtime），
用替身模擬失敗路徑（例：GetData() 明確回 null），並排執行、把讀數印出來。

【為什麼它是證據而不是安慰】
① **BEFORE 必須真的重現成因** —— 舊形狀沒炸／沒卡，就代表探針沒對準，AFTER 的綠沒有意義。
② **每個 case 配一格反向對照** —— 證明新守衛沒有順手把正常路徑或原本的互斥一起擋掉。
   （本例：finally 還原旗標之後，「進行中連點要早退」仍然成立。）
③ **顯式宣告射程** —— 它證明的是 C# 語意層，⛔ 不涵蓋 Unity 執行期（排程、假 null、生命週期）。
   ⇒ 結論只能寫「成因已移除」，不能寫「已在遊戲裡實測」。

【什麼時候不要用】成因本身**就在**宿主行為裡（生命週期、排程、假 null、per-frame 成本）——
那種搬不走，搬走就是換了一個題目。

appended → `AgentCommands/Lessons/lessons.jsonl`

---

後續：定期 review jsonl tail，將高價值 lesson promote 進 `Skills~/agent-lessons-log/SKILL.md` curated list（手動 edit）。
