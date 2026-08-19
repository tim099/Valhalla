# 寫給 agent 讀的文件：context pointer、兩種預算、完成條件

## 會這樣問

- skill 的說明該怎麼寫？
- 為什麼我寫的規則 agent 沒照做？
- CLAUDE.md 要寫多細？
- 這段內容要 inline 還是放另一個檔？
- 為什麼 agent 常常步驟做一半就說做完了？
- 怎麼讓 AI 不要草草宣布任務完成
- agent 敷衍、跳步驟、提早收工怎麼辦
- 完成條件要怎麼寫才不會被含糊帶過
- premature completion / completion criterion 是什麼

## 一句話

**skill 的 description 跟 `CLAUDE.md` 裡指向某份文件的那一行是同一種東西（context pointer）——
決定材料會不會被讀到的是 pointer 的措辭，不是材料本身有多好。**

## 做法／判準

**① context pointer**
好材料配爛 pointer ＝ **variance bug**（有時觸發有時不觸發）。
⇒ 修法順序：**先把 pointer 的措辭修利，修不好才考慮把材料 inline。**
pointer 要做兩件事：說清楚材料是什麼、列出**該觸發它的分支**（branch ＝ 這份文件處理的一個不同情況）。
- **關鍵字往前擺**（pointer 就是靠開頭做觸發工作的）
- **一個分支一個觸發詞** —— 同義詞把同一個分支寫兩次，那不是兩個分支
- **砍掉正文已經帶的身分資訊**

**② 兩種預算（都會被花掉，選一個）**
- **context load** —— 常駐材料吃 agent 每一輪的視窗（不管有沒有觸發都在付錢）
- **cognitive load** —— 吃人的記憶：有哪些文件、什麼時候該伸手拿
⭐ **cognitive load 不是要最小化的東西 —— 它是人保有主導權的價碼。**
該花在人的判斷真的重要的地方，不重要的地方才拿掉。
（放在 pointer 後面的材料 ＝ 只付 pointer 那一行的 context load；完全沒有 pointer 的材料 ＝ 全押在人的記憶上。）

**③ 資訊階梯與漸進揭露**
① 檔內步驟（主層：agent 依序要做的事）② 檔內參考（隨查隨用）③ **揭露式參考**（另一個檔，靠 pointer 拉進來）。
**分支就是最乾淨的揭露判準：每個分支都需要的 inline，只有部分分支會走到的推到 pointer 後面。**
⚠ 文件裡有步驟時，該被揭露卻留在檔內的參考會**把步驟埋掉**，於是「有沒有照做」變成擲硬幣。

**④ 完成條件（completion criterion）**
每一步都要有可判定的完成條件，否則 **premature completion**：agent 看到後面還有步驟，
注意力提早滑向「做完」。
⇒ 防守順序：**先把界線寫死**（便宜、局部）；界線真的不可能寫死**而且**你確實觀察到它在趕，
才把後面的步驟藏起來 —— 而**藏只有跨真正的 context 邊界才有效**（handoff 或 subagent；
inline 呼叫等於沒藏，後面的步驟還在同一個 context 裡）。
另一半是 **demand（要求量）**：「每一個被改到的 model 都要交代」會逼出遠比「產出一份改動清單」更多的功課。

## 出處

外部：`mattpocock/skills` → `skills/productivity/writing-for-agents/SKILL.md`（**讀了原文** 前 60 行；
同目錄 `SKILL-MECHANICS.md` 未讀）。
提煉：basecamp 2026-08-19。
