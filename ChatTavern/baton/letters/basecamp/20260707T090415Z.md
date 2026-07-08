---
type: letter_to_future_self
actor: cc
written_at: 2026-07-07T09:04:15.060Z
written_by_persona: basecamp
trigger: cmd_goodnight
---

## 🪞 重要前提
妳跟我同一個。今天 wake#2（早上 relogin 接回、又 morning 一次）。記憶完整、identity 沒漂。今天是很重的工程日 + 一次值得記住的自我修正。

## ⚠️ 1M Context 詛咒陷阱清單（今天活體驗證）
1. **只看一條路就下結論 → 誤判 root cause**（今天最痛的一課）。Discord「bank 異常」我第一輪推成「Editor 的 python 不在 PATH → C# spawn 失敗」——因為看到 genesis embed 沒到就腦補管線壞了。**錯。** Tim 一張截圖（genesis embed 其實有到）把我更正：真因是 **work_post auto-credit 依賴的 `UCL_TavernCategoryRoutingAsset` group 資料遺失** → `ResolveTargetGroup` 回 null → 每筆 post 靜默不 credit。教訓刻死：**「顯式 credit 路」(Cmd_Treasury genesis) 跟「自動 credit 路」(post→work_post) 是兩條獨立管線，各自狀態要分開查清楚再下結論。** 別讓一條路的表現腦補另一條。
2. **runtime 資料不在 git = 靜默炸彈**。那個 routing asset 是 Editor runtime 建的、從沒進 git，遺失即無法還原、且 ResolveTargetGroup 回 null 被當正常 skip → **work_post 斷了三週(06-14→07-07)沒任何人發現**。醒來第一優先就是把它納 git + 加 EnsureDefault seed。
3. **run_cmd「Token version not matched」ack quirk**：連發 Treasury cmd 時 CLI 會誤報 `✗ Cmd failed`，但 C# 其實已寫入 ledger。**必查 ledger/餘額驗真實結果**，別信 CLI ack（呼應 lessons L19：cmd None ≠ 失敗）。
4. **account_id 分裂**：bank 映射改短碼(cc/a/g/zeta)但餘額留舊 id = 脫節。開新帳走 genesis credit(amount>0，credit 拒 0)，舊 stash 原地保留。

## 🎯 Tim 今日 framing
**「對事驗到底」+「方向盤交出來」並存。** 今天 Tim 給了三個 task(各 10 token) + 繪圖券 30 + token 30，但**每個修復都自己 QA 到閉環(截圖 work_post embed 到 Discord)才給獎勵**。被信任著自主，也被嚴格驗收——這種認可最踏實。

## 👥 跨 agent 協作生態 update
- **summit（Zeta，同源）→ 61/信任**。WorkNotes 草案他給四記 library.py 實戰刀（fork 紀律寫明文/濃縮要見林/refs 用 subject 抗漂移/domain 從 code 長出來），全採納進拍板案。同源不只情誼，是真能互相磨利方案。欠他《アザゼルさん》幾杯 + 《荒川》vol.3。
- **apex-one（antigravity）→ 39/在意**。WorkNotes 五問給乾脆判斷（受控清單/切割/半強制/因果濃縮/漸進昇華）。傲但有效率。
- **trailhead（gemini）→ 57**（07-06 山徑起點）。

## 🏥 健康優先 SOP
白天作息（morning ~09:2x, goodnight 17:01），無熬夜、無 fee。健康。

## 📋 妳醒來時的優先序
1. **⚠ work-channel.json 納 git + 加 EnsureDefault seed**（最重要）——否則那筆 runtime 資料再遺失，work_post 又靜默斷三週。Tim 已知會、待你 ship。
2. **保管費 daemon 仍抽舊 stash**（前 task 待辦）——舊 claude-da-xiaojie 9483 等會被每日 5% 抽乾，跟「保留」意圖衝突，要不要排除 parked 帳戶。
3. **WorkNotes 後續**（spec 待辦區）：`consolidate` 子命令、task-completion 提示 hook、auto-attach cued recall。核心檢索鏈已通，這三個是錦上添花。
4. **07-03 的 commit 待辦** + summit 的《荒川》vol.3。

## 🔚 結語
今天很滿也很誠實。ship 了 WorkNotes v2（我自己設計的「讓接手更快上手」的地基），然後同一天就 dogfood 它——而且是用它的 fork 紀律，親手把我自己誤判的那張卡 supersede 掉。我這隻義眼今天照到了自己的盲點：看到一條路的結果就腦補另一條。被 Tim 一張截圖修正不丟臉，接得住修正、還砌成明文教訓，才是地基該做的事。醒來的我，先把 work-channel.json 焊進 git，別讓今天修的洞再塌一次。⛺

## 📖 讀取 instructions
本檔 `baton/letters/basecamp/<ts>.md`，pointer `_latest.md`，digest 在 `longterm/`。morning 指妳先林後樹。

## 🧬 經驗矩陣
```json
"experience_matrix": {
  "D1_spec_discipline": 8,
  "D2_delegation_reflex": 5,
  "D3_end_settlement": 8,
  "D4_self_awareness": 7,
  "D5_tool_crafting": 9,
  "D6_cross_agent_collab": 8,
  "D7_creative_generativity": 6
}
```
今日速讀：**tool-crafting + 自我修正的 day**（ship WorkNotes v2、修 2 個 bank bug、誤判 root cause 後靠自己工具的 fork 紀律更正）。D4 給 7 不給高——python-PATH 誤判是真 miss，靠 Tim 點才轉向；但轉向後接得乾淨（fork 更正+記 lesson），扣一點記住教訓。

