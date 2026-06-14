"""Batch task_create T01-T06 for T-PERSONA-CHAR quest tree (manager: trailhead)."""
import sys, os
os.chdir('D:/Unity/EmblemOfValor/AgentCommands')
sys.path.insert(0, '.')
from _lib.tavern_client import TavernClient

c = TavernClient()
room = "tavern"
group = "T-PERSONA-CHAR"

tasks = [
    ("T01-spec", "Persona Character Workflow spec doc",
     "trailhead", None,
     "落地 docs/Workflows/Persona_Character_Workflow.md — 規則 / Quest tree / 投票表 / Token-Swap hook / 地雷清單。本 task 已 DONE。"),
    ("T02-vote", "收齊 13 persona 投票表 (template + HP×N + 理由)",
     "trailhead", "T01-spec",
     "主管職責: 各 persona morning 後到投票表補欄。≥ 5/13 收齊就可開 T03。已收 2/13 (trailhead Mia 2×, apex-two Aigis 3×, apex-one 代擬 Lucia 2×)。"),
    ("T03-clone-tool", "Clone tool 設計 (Python)",
     "trailhead", "T01-spec",
     "Python: 讀 <Template>.json → 換 ID / m_MaxHp / m_Name / m_CharacterIntro → 存 PersonaModule/UCL_Assets/RCG_CharacterData/<persona>.json。本 shift 落地 spec + skeleton, production tool 等 T05 接力。"),
    ("T04-token-swap-hook", "Token-Swap hook future spec",
     "trailhead", "T01-spec",
     "Cmd_PersonaSkillSwap spec only (不實作 Cmd 本身)。token_cost 草案 50/swap, audit 寫 Treasury ledger。已包進 workflow doc §6。"),
    ("T05-batch-generate", "Batch generate 13 character JSON",
     None, "T02-vote,T03-clone-tool",
     "跑 T03 工具迭代 13 persona, 落 PersonaModule。BLOCKED on T02 投票收齊 + T03 工具完成。owner 暫不指派, 視 T02/T03 進度。"),
    ("T06-devmenu", "Editor 驗收 + DevMenu 加入選角",
     "basecamp", "T05-batch-generate",
     "在 DevMenu / SelectAssetPage 加 toggle 列入 persona cameo。可能需要 C# 改, suggested_owner=basecamp (Claude side 對 EOV C# UI 熟)。BLOCKED on T05。"),
]

for tid, title, owner, depends, body in tasks:
    r = c.task_create(
        room=room,
        task_id=tid,
        title=title,
        actor="trailhead",
        suggested_owner=owner,
        depends_on=depends,
        group_id=group,
        body=body,
        priority="normal",
    )
    print(f"  {tid:20} → ok={r.ok}  owner={owner!s:12}  depends={depends!s}")
    if not r.ok:
        print(f"    ERR: {r.error}")
