"""T02 progress update — gura voted, 3/13 收齊."""
import sys, os
os.chdir('D:/Unity/EmblemOfValor/AgentCommands')
sys.path.insert(0, '.')
from _lib.tavern_client import TavernClient
c = TavernClient()

r = c.task_progress(
    room="tavern",
    task_id="T02-vote",
    actor="trailhead",
    summary="✓ +1 vote: gura → Renka 2× (Rest+Aim 對齊「裝糊塗護身瞄準才出手」軸, wake#6 低出場輩輕巧側重)。投票表 3/13。"
)
print('progress:', r.ok)
