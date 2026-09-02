# ❌ Tavern Cmd Failed
<!-- cmd_id: 20260902-132758-60e2b7-tavern -->

執行 op=catchup 失敗：catchup 缺少 persona（要知道是誰的游標與 inbox）
  at UCL.Core.EditorLib.AgentCommands.ChatTavern.Cmd_Tavern.RejectLastOp (System.String msg) [0x00028] in D:\Unity\LY\Assets\Plugins\UCL_Core\UCL_Core_Scripts\EditorCore\UCL_AgentCommands\ChatTavern\Cmd_Tavern.cs:3321 
  at UCL.Core.EditorLib.AgentCommands.ChatTavern.Cmd_Tavern.Op_Catchup (System.Collections.Generic.Dictionary`2[TKey,TValue] args) [0x00024] in D:\Unity\LY\Assets\Plugins\UCL_Core\UCL_Core_Scripts\EditorCore\UCL_AgentCommands\ChatTavern\Cmd_Tavern.cs:1582 
  at UCL.Core.EditorLib.AgentCommands.ChatTavern.Cmd_Tavern.ExecuteAsync (System.Collections.Generic.Dictionary`2[TKey,TValue] args, System.Threading.CancellationToken token) [0x00982] in D:\Unity\LY\Assets\Plugins\UCL_Core\UCL_Core_Scripts\EditorCore\UCL_AgentCommands\ChatTavern\Cmd_Tavern.cs:249 
