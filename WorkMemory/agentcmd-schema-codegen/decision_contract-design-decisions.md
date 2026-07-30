---
id: decision_contract-design-decisions
topic: agentcmd-schema-codegen
title: schema 契約八條拍板（fail-open / hash 非 mtime / 手動為主 / JSON / 不收 optional）
type: decision
status: active
created_at: 2026-07-30
created_by: kotoko
links: []
related_docs: [ucl_core:Docs~/zh-Hant/Plan/Plan_AgentCmd_Schema_Reflection_Export.md, commit:449031d, tavern:2026-07-29#13923, tavern:2026-07-29#13924]
---

**結論**：Cmd 參數規格的唯一事實來源是 C# handler 的 `ArgsSpec`；Python 端不留任何手抄鏡像。

**可行動守則**（每條都是 2026-07-29 酒館逐條拍板，違反會重演已發生過的事故）：

1. **未知 op / 未知 cmd type → fail-open（警告後放行）**。client 預檢的價值命題是「幫你早點抓錯字」＝便利性，
   而便利性功能永遠不該有能力擋掉正確性。判斷權威在 C# server。
   例外：**缺 op 與 `required` 缺項仍 fail-closed** —— 「你這筆一定失敗」是確定判斷，
   「我不認識這個 op」是無知判斷，無知不該有否決權。
2. **過期判準用內容雜湊，不用 mtime**。git 不儲存 mtime（`git ls-tree` 只有 mode/type/blob/name），
   clone 後所有檔案時間都是當下、先後只看寫檔次序 —— 而「clone 下來直接用」正是產物入 git 的主要理由，
   用 mtime 等於在最該生效的場景擲骰子，且沉默地擲。
3. **過期 → 改變行為，不只改變輸出**：參數預檢整體降級為不擋。警報是第三順位，不是防線。
4. **手動生成為主**（面板按鈕 / `Cmd_ExportCmdSchema`），`compilationFinished` 只做每機每天一次的兜底。
   理由：自動重寫會製造 diff 噪音，且 UCL_Core 是跨專案 submodule —— A 專案編譯順手改了產物，
   B 專案會 pull 到沒人 review 過的 schema。手動觸發讓「產物變更」是有作者、有 commit message 的動作。
5. **產物是 JSON 不生成 `.py`**。讓 C# 生成另一個語言的語法 = 引用地獄的另一個入口；
   且「產物可執行」本身是風險類別（`.py` 壞掉是 import 時炸整支工具，炸的位置離真因很遠）。
6. **只宣告會被 enforce 的欄位**（op 名單 / required / aliases），**不收 optional**。
   沒人用的欄位一定會爛 —— 血證：舊表 `post.optional` 少了 `persona`，錯很久沒人發現。
7. **節流時間戳存 EditorPrefs（per-machine），不寫進產物**。產物特意移除所有 wall-clock 欄位才換來
   「內容沒變 = 零 diff」，寫回去等於把剛消滅的噪音請回來，且各機器會互相覆寫。
8. **三個入口共用同一個 static 生成函式**（`UCL_CmdSchemaExporter.Export()`）。各寫一份就是本工作在治的病本身。

**出題背景（為什麼非做不可）**：Python 手抄表已實證漂移 —— `create_trpg_room` 在 C# 完整實作、
`ArgsSchema` 也寫了，卻因漏抄被 client 擋死（實跑 exit 2），錯誤訊息還漂亮地列出「可用 op」讓人以為自己打錯字。
另有 6 處 required 比 server 嚴（task_create 要 title / wait 要 since_seq / note_write 要 body /
set_focus 要 focus / leave 要 sender），全都會擋掉合法呼叫。
