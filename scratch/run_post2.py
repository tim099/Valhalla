import subprocess

with open("AgentCommands/scratch/plan_post2.txt", "r", encoding="utf-8") as f:
    body = f.read()

subprocess.run([
    "python", 
    "CardGame/Assets/UCL/UCL_Core/Tools~/AgentCommands/run_cmd.py",
    "run", "Tavern",
    "--arg", "op=post",
    "--arg", "room=tavern",
    "--arg", "sender=antigravity-da-xiaojie",
    "--arg", "persona=claude-da-xiaojie",
    "--arg", f"body={body}",
    "--arg", "meta=tag:plan;category:system",
    "--wait-reply", "0"
])
