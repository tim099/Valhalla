import subprocess

with open('AgentCommands/scratch/temp_letter.md', 'r', encoding='utf-8') as f:
    letter = f.read()

with open('AgentCommands/scratch/temp_summary.txt', 'r', encoding='utf-8') as f:
    summary = f.read()

subprocess.run([
    'python', 'CardGame/Assets/UCL/UCL_Core/Tools~/AgentCommands/awakening.py', 'goodnight',
    '--letter-body', letter,
    '--summary', summary,
    '--perturbation', '0.05',
    '--persona', 'apex-two',
    '--agent', 'antigravity'
], check=True)
