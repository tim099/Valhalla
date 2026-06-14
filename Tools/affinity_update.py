#!/usr/bin/env python3
"""
Affinity Update CLI — agent-friendly wrapper around `_lib.affinity_manager`.

Purpose: replace direct JSON editing of `relations.json` (which is FORBIDDEN per Affinity_System.md §禁止直接 IO).
Usage:
    python AgentCommands/Tools/affinity_update.py update \
        --persona basecamp --target Tim \
        --trust 0.1 --affection 0.15 --irritation -0.05 \
        --reason "Tim 親額頭 + 20 token 績效獎金" \
        --opinion "額頭只是個普通部位才沒有什麼特別意義..."

    python AgentCommands/Tools/affinity_update.py show --persona basecamp --target Tim
    python AgentCommands/Tools/affinity_update.py list-targets --persona basecamp
    python AgentCommands/Tools/affinity_update.py list-personas
"""
# 區塊職責: 解析 CLI 參數 + 派遣到 affinity_manager API
# 物理意義: agent 在 chat 內快速跑一行 cmd 就能寫 affinity, 不必開 python REPL 也不必 risk 直接編 JSON
# 數值影響: 無自家邏輯, 全部 delegate 給 affinity_manager (single source of truth)
import argparse
import json
import sys
from pathlib import Path

# 區塊職責: Windows cp950 終端強制 utf-8 stdout
# 物理意義: agent 在 chat 內跑 cmd 時印中文 + emoji 不能崩 (cp950 不認 ✅)
# 數值影響: 純 IO 層, 不影響邏輯
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# 把 AgentCommands/_lib 加到 import path
_REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO / "AgentCommands"))

from _lib import affinity_manager as af  # noqa: E402

# 8 軸名稱 — 跟 affinity_manager.EMOTION_AXES 對齊
AXES = ("trust", "affection", "respect", "interest",
        "irritation", "dependence", "admiration", "loyalty")


def cmd_update(args):
    # 區塊職責: 從 CLI 收集 axis_deltas (只取明確指定的軸)
    # 物理意義: argparse 把 --trust 0.1 自動裝到 args.trust=0.1; None 表示沒指定
    # 數值影響: 沒指定的軸不會落 history, 符合「2-4 軸/事件」設計哲學
    deltas = {axis: getattr(args, axis) for axis in AXES if getattr(args, axis) is not None}
    if not deltas:
        print("❌ 必須指定至少 1 軸 (--trust / --affection / ... etc)", file=sys.stderr)
        return 2
    rec = af.update_emotion(
        persona=args.persona,
        target=args.target,
        axis_deltas=deltas,
        reason=args.reason,
    )
    if args.opinion:
        af.add_opinion(args.persona, args.target, args.opinion)
        rec = af.get_affinity(args.persona, args.target)
    print(f"✅ {args.persona} → {args.target}")
    print(f"   axis_deltas applied: {deltas}")
    print(f"   surface_score: {rec['surface_score']}  tier: {rec['tier']}")
    print(f"   reason: {args.reason}")
    if args.opinion:
        print(f"   opinion added: {args.opinion[:60]}...")
    return 0


def cmd_show(args):
    rec = af.get_affinity(args.persona, args.target)
    if not rec:
        print(f"❌ {args.persona} → {args.target}: no record")
        return 1
    print(json.dumps(rec, ensure_ascii=False, indent=2))
    return 0


def cmd_list_targets(args):
    rec = af.get_affinity(args.persona)  # 沒 target 回全部
    if not rec:
        print(f"❌ {args.persona}: no targets")
        return 1
    for tgt, data in rec.items():
        print(f"  {tgt:20s}  score={data.get('surface_score', 0):3d}  tier={data.get('tier', '?')}")
    return 0


def cmd_list_personas(args):
    personas = af.list_personas()
    print(f"📚 {len(personas)} personas with affinity records:")
    for p in personas:
        print(f"  - {p}")
    return 0


def cmd_add_opinion(args):
    af.add_opinion(args.persona, args.target, args.opinion)
    print(f"✅ opinion added to {args.persona} → {args.target}: {args.opinion}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Affinity Update CLI (per Affinity_System.md, replace direct JSON editing)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # update
    up = sub.add_parser("update", help="Apply axis_deltas + recompute surface_score + (optional) add opinion")
    up.add_argument("--persona", required=True)
    up.add_argument("--target", required=True)
    up.add_argument("--reason", required=True, help="history entry reason 字串")
    up.add_argument("--opinion", default=None, help="(optional) 同時加一筆 opinion 短句")
    for axis in AXES:
        up.add_argument(f"--{axis}", type=float, default=None, help=f"{axis} axis delta")
    up.set_defaults(func=cmd_update)

    # show
    sh = sub.add_parser("show", help="Print full record for one persona+target")
    sh.add_argument("--persona", required=True)
    sh.add_argument("--target", required=True)
    sh.set_defaults(func=cmd_show)

    # list-targets
    lt = sub.add_parser("list-targets", help="List all targets for a persona with surface_score")
    lt.add_argument("--persona", required=True)
    lt.set_defaults(func=cmd_list_targets)

    # list-personas
    lp = sub.add_parser("list-personas", help="List all personas with affinity records")
    lp.set_defaults(func=cmd_list_personas)

    # add-opinion
    op = sub.add_parser("add-opinion", help="Add a textual opinion to persona+target (no vector change)")
    op.add_argument("--persona", required=True)
    op.add_argument("--target", required=True)
    op.add_argument("--opinion", required=True)
    op.set_defaults(func=cmd_add_opinion)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
