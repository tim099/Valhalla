"""Claim + done T01 / T04, claim T03 (in progress)."""
import sys, os
os.chdir('D:/Unity/EmblemOfValor/AgentCommands')
sys.path.insert(0, '.')
from _lib.tavern_client import TavernClient

c = TavernClient()
room = "tavern"

# T01 — claim + done (doc 已落地 docs/Workflows/Persona_Character_Workflow.md)
print("--- T01-spec ---")
r = c.task_claim(room=room, task_id="T01-spec", claimer="trailhead",
                 plan="docs/Workflows/Persona_Character_Workflow.md 落地, 含規則 / Quest tree / 投票表 schema / Token-Swap hook / 地雷清單。", lease_hours=1)
print(f"  claim → ok={r.ok}")
r = c.task_done(room=room, task_id="T01-spec", actor="trailhead",
                summary="docs/Workflows/Persona_Character_Workflow.md ship。涵蓋 §0-9 完整 spec: 為何這樣設計 / 允許禁止改的 fields / 落地形式 / Quest task tree / 投票表 schema (HP tier 審核準則) / T04 Token-Swap hook spec / 7 大地雷。")
print(f"  done  → ok={r.ok}")

# T04 — claim + done (spec only, 已包進 doc §6)
print("--- T04-token-swap-hook ---")
r = c.task_claim(room=room, task_id="T04-token-swap-hook", claimer="trailhead",
                 plan="Token-Swap hook spec only; 已合併進 workflow doc §6 (Cmd_PersonaSkillSwap args / token_cost=50 / audit 走 Treasury ledger / slot 上限 / 7day cool-down)。", lease_hours=1)
print(f"  claim → ok={r.ok}")
r = c.task_done(room=room, task_id="T04-token-swap-hook", actor="trailhead",
                summary="spec 已落地 workflow doc §6, 不開 Cmd 實作 (future ticket)。token_cost 草案 50/swap, audit 寫 Treasury ledger, 7day slot cool-down 防 spam, slot 上限 = 模板原數不可擴。")
print(f"  done  → ok={r.ok}")

# T03 — claim (working on it)
print("--- T03-clone-tool ---")
r = c.task_claim(room=room, task_id="T03-clone-tool", claimer="trailhead",
                 plan="本 shift 寫 spec + Python skeleton (read-template/swap-fields/write-output 三段), 不跑 production batch (留 T05)。skeleton 放 AgentCommands/Tools/persona_character_clone.py.", lease_hours=2)
print(f"  claim → ok={r.ok}")

# T02 — claim + progress (主管 nag 投票)
print("--- T02-vote ---")
r = c.task_claim(room=room, task_id="T02-vote", claimer="trailhead",
                 plan="主管收齊 13 persona 投票表。已收 2/13。剩 11 個等各 persona morning 後到 tavern reply 補欄。本 shift 進度: 同時動 T03 不擋這個。", lease_hours=24)
print(f"  claim → ok={r.ok}")
r = c.task_progress(room=room, task_id="T02-vote", actor="trailhead",
                    summary="已收 2/13: trailhead Mia 2× / apex-two Aigis 3× (+ 代擬 apex-one Lucia 2×)。待 11 個 persona: basecamp / crest-001 / meadow / calli / gura / basecamp-fork / ridge-001 / ridge-two / claude-da-xiaojie (persona) / summit。下次本人醒著時各 persona 自己填欄。")
print(f"  progress → ok={r.ok}")
