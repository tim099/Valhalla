# ✅ Checklist — agent-command-pipeline-parallelize

_衍生 cache；最後更新 2026-05-13 15:17:55 UTC_

- ✅ **T01-analysis-design** 分析當前 pipeline + 寫 3 方案 design doc + 邀請 review
- ✅ **T02-queue-trigger-path-overload** UCL_AgentCommandQueue: 加 path methods overload (agentId arg) + queues/ subdir (owner: gemini)
- ✅ **T03-watcher-multi-trigger-scan** UCL_AgentCommandWatcher: 掃 default + queues/ subdir 所有 trigger 並 dispatch
- ✅ **T04-runner-agent-id-arg** UCL_AgentCommandRunner / Trigger: 加 agentId 參數 + MarkRunning 對應檔
- ✅ **T05-python-agent-id-arg** run_cmd.py --agent-id <X> arg + ensure_idle per-agent
- ✅ **T06-verify-multi-agent-isolation** Verify: 雙 agent 同時 submit 互不阻塞 + recompile clean
