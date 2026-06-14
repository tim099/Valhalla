"""T05 — Batch generate 4 收齊 persona character JSONs."""
import os, sys, subprocess
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
os.chdir('D:/Unity/EmblemOfValor')

tool = "AgentCommands/Tools/persona_character_clone.py"

batch = [
    ("trailhead", "Mia", 2.0, "山徑起點，gemini-2.5-pro layer 0 base，wake#4 第一個自由日完成的同事。", "wake#4 layer 0 base, 對齊山徑 framing"),
    ("apex-two",  "Aigis", 3.0, "Antigravity apex-one 的 compact 後繼，高軌頂層的算力繼承者。", "高軌頂層 + 多次 compact 冗餘"),
    ("apex-one",  "Lucia", 2.0, "Antigravity (Gemini) 的高軌頂點基礎人格，完美執行者。", "初創銳利感 (apex-two 代擬)"),
    ("gura",      "Renka", 2.0, "claude-code 線上的 Hololive Myth 小鯊魚，裝糊塗護身、瞄準才出手。", "Rest+Aim 對齊「裝糊塗瞄準才出手」軸, wake#6 低出場輩"),
]

for persona, template, mult, intro, reason in batch:
    print(f"\n=== {persona} ← {template} × {mult} ===")
    r = subprocess.run([
        sys.executable, tool,
        "--persona", persona,
        "--template", template,
        "--hp-multiplier", str(mult),
        "--intro", intro,
        "--reason", reason,
    ], capture_output=True, text=True, encoding='utf-8')
    print(r.stdout)
    if r.returncode != 0:
        print("STDERR:", r.stderr)
        sys.exit(1)
print("\n✅ 4/4 ship.")
