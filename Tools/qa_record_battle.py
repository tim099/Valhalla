#!/usr/bin/env python3
"""
T03 qa_record_battle.py — Battle Result Recorder (Plan §3 row "Cmd_RecordBattleResult")

職責：戰後 agent 觀察結果 → append 一 row 至 qa_battle_results.csv。
物理意義：純 append-only CSV row 寫入，無 Unity 依賴；agent 從 Cmd_BattleSnapshot/Summary
        看到的數據，配合自己觀察手動填值。

子命令:
  add ... 一堆欄位 ...    寫一場戰鬥結果
  recent [-n N]           看最近 N 筆 (預設 10)

範例:
  python AgentCommands/Tools/qa_record_battle.py add \
    --battle-id battle_-490552 \
    --preset-id Spiderwood_Normal_Lv1_SpiderQueen \
    --enemy-comp "SpiderQueen+2 spiderlings" \
    --player-class Christina \
    --player-count 1 \
    --turn-count 4 \
    --outcome WIN \
    --damage-dealt 87 --damage-taken 12 \
    --mana-avg 2.5 --cards-played 9 --items-used 0 \
    --difficulty-score 2 \
    --notes "Lv1 boss 順手，front HP 從未掉破半"
"""

import argparse
import csv
import datetime
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
CSV_PATH = REPO_ROOT / "AgentCommands" / "QA_Battle_Logs" / "qa_battle_results.csv"

# 區塊職責：CSV column order — 必須跟 csv header 完全對齊（Plan §2 schema）
COLUMNS = [
    "battle_id", "timestamp", "preset_id", "enemy_comp",
    "player_class", "player_count",
    "turn_count", "outcome",
    "damage_dealt", "damage_taken",
    "mana_avg", "cards_played", "items_used",
    "difficulty_score", "notes",
]

VALID_OUTCOMES = {"WIN", "LOSS", "RETREAT", "DRAW"}


def cmd_add(args):
    """寫一筆 battle result"""
    outcome = (args.outcome or "").upper()
    if outcome not in VALID_OUTCOMES:
        print(f"✗ outcome 必須是 {VALID_OUTCOMES}，給的是 {outcome!r}", file=sys.stderr)
        return 2

    if not (1 <= args.difficulty_score <= 5):
        print(f"✗ difficulty_score 必須 1-5，給的是 {args.difficulty_score}", file=sys.stderr)
        return 2

    ts = args.timestamp or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    row = {
        "battle_id": args.battle_id,
        "timestamp": ts,
        "preset_id": args.preset_id,
        "enemy_comp": args.enemy_comp,
        "player_class": args.player_class,
        "player_count": args.player_count,
        "turn_count": args.turn_count,
        "outcome": outcome,
        "damage_dealt": args.damage_dealt,
        "damage_taken": args.damage_taken,
        "mana_avg": args.mana_avg,
        "cards_played": args.cards_played,
        "items_used": args.items_used,
        "difficulty_score": args.difficulty_score,
        "notes": args.notes or "",
    }

    # 確認 header 存在 + 對齊（防舊 csv 缺欄）
    if not CSV_PATH.exists():
        CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
            csv.DictWriter(f, fieldnames=COLUMNS).writeheader()

    with CSV_PATH.open("a", encoding="utf-8", newline="") as f:
        csv.DictWriter(f, fieldnames=COLUMNS).writerow(row)

    print(f"✓ recorded battle: {args.battle_id} {outcome} turn={args.turn_count} diff={args.difficulty_score}")
    print(f"  → {CSV_PATH.relative_to(REPO_ROOT)}")
    return 0


def cmd_recent(args):
    """看最近 N 筆"""
    if not CSV_PATH.exists():
        print("(CSV 不存在)")
        return 0
    with CSV_PATH.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    tail = rows[-args.n:] if args.n > 0 else rows
    if not tail:
        print("(no battles recorded yet)")
        return 0
    print(f"# Recent {len(tail)} battles (of {len(rows)} total)")
    print()
    print("| timestamp | battle_id | preset | class | turns | outcome | diff |")
    print("|---|---|---|---|---|---|---|")
    for r in tail:
        print(f"| {r.get('timestamp', '')} | {r.get('battle_id', '')} | "
              f"{r.get('preset_id', '')} | {r.get('player_class', '')} | "
              f"{r.get('turn_count', '')} | {r.get('outcome', '')} | {r.get('difficulty_score', '')} |")
    return 0


def main():
    parser = argparse.ArgumentParser(description="T03 QA Battle Result Recorder")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="記錄一場戰鬥結果")
    p_add.add_argument("--battle-id", required=True, help="戰鬥 ID (e.g. battle_-490552 from Cmd_BattleSnapshot)")
    p_add.add_argument("--timestamp", default=None, help="ISO timestamp (預設 now UTC)")
    p_add.add_argument("--preset-id", required=True, help="BattlePreset id (e.g. Spiderwood_Normal_Lv1_SpiderQueen)")
    p_add.add_argument("--enemy-comp", default="", help="敵方組成描述")
    p_add.add_argument("--player-class", required=True, help="主將職業 (Christina / Lucia / Elsie / Shadlatir / Xinder)")
    p_add.add_argument("--player-count", type=int, default=1, help="玩家單位數")
    p_add.add_argument("--turn-count", type=int, required=True, help="戰鬥總回合數")
    p_add.add_argument("--outcome", required=True, help="WIN / LOSS / RETREAT / DRAW")
    p_add.add_argument("--damage-dealt", type=int, default=0)
    p_add.add_argument("--damage-taken", type=int, default=0)
    p_add.add_argument("--mana-avg", type=float, default=0.0)
    p_add.add_argument("--cards-played", type=int, default=0)
    p_add.add_argument("--items-used", type=int, default=0)
    p_add.add_argument("--difficulty-score", type=int, required=True, help="agent 主觀難度分 1-5 (1=超簡單 5=險勝/輸)")
    p_add.add_argument("--notes", default="", help="額外觀察")
    p_add.set_defaults(func=cmd_add)

    p_rec = sub.add_parser("recent", help="看最近 N 筆")
    p_rec.add_argument("-n", type=int, default=10)
    p_rec.set_defaults(func=cmd_recent)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
