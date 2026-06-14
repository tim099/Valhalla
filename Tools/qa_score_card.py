#!/usr/bin/env python3
"""
T04 qa_score_card.py — Card Power Scorer (Plan §3 row "Cmd_ScoreCard")

職責：agent 出完某張卡 → 評 1-5 分 + append 一 row 至 card_power_log.csv。
物理意義：純 append-only CSV，無 Unity 依賴；situation_score 評分標準：
  1 = 浪費 (出在不該出的回合 / 沒打到目標)
  2 = 勉強有用 (湊 cost / 暖場)
  3 = 標準 (達成基本功能)
  4 = 強力 (combo 命中 / 關鍵爆發)
  5 = 完美 timing (turning point / 反殺 / one-shot boss)

子命令:
  add ... 一堆欄位 ...                寫一張出牌評分
  add-batch --battle-id X --json '[...]'   批次寫 (多張一次提交)
  recent [-n N]                        看最近 N 筆

範例:
  python AgentCommands/Tools/qa_score_card.py add \
    --battle-id battle_-490552 --turn 3 --player-class Christina \
    --card-id 7 --card-name "輕攻擊" --card-cost 1 \
    --target-id 5 --target-class "Lv1.光之精靈" \
    --damage-or-effect "12 dmg" \
    --situation-score 4 \
    --combo-chain "buff連擊×3"
"""

import argparse
import csv
import datetime
import json
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
CSV_PATH = REPO_ROOT / "AgentCommands" / "QA_Battle_Logs" / "card_power_log.csv"

# 區塊職責：CSV column order — 跟 csv header 對齊（Plan §2 schema 加 card_unique_id）
COLUMNS = [
    "battle_id", "turn", "player_class",
    "card_id", "card_unique_id", "card_name", "card_cost",
    "target_id", "target_class",
    "damage_or_effect", "situation_score", "combo_chain",
]


def _validate_score(s) -> int:
    """確認 score 為 1-5 整數"""
    try:
        v = int(s)
    except (TypeError, ValueError):
        raise ValueError(f"situation_score 必須 1-5 整數，給的是 {s!r}")
    if not (1 <= v <= 5):
        raise ValueError(f"situation_score 必須 1-5，給的是 {v}")
    return v


def _append_row(row: dict) -> None:
    """append 一 row（必要時建檔/補 header）"""
    if not CSV_PATH.exists():
        CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
            csv.DictWriter(f, fieldnames=COLUMNS).writeheader()
    with CSV_PATH.open("a", encoding="utf-8", newline="") as f:
        csv.DictWriter(f, fieldnames=COLUMNS).writerow(row)


def cmd_add(args):
    try:
        score = _validate_score(args.situation_score)
    except ValueError as e:
        print(f"✗ {e}", file=sys.stderr)
        return 2

    row = {
        "battle_id": args.battle_id,
        "turn": args.turn,
        "player_class": args.player_class,
        "card_id": args.card_id,
        "card_unique_id": args.card_unique_id or "",
        "card_name": args.card_name,
        "card_cost": args.card_cost,
        "target_id": args.target_id or "",
        "target_class": args.target_class or "",
        "damage_or_effect": args.damage_or_effect or "",
        "situation_score": score,
        "combo_chain": args.combo_chain or "",
    }
    _append_row(row)
    print(f"✓ scored card: turn {args.turn} {args.card_name} (cost {args.card_cost}) → score {score}/5")
    print(f"  → {CSV_PATH.relative_to(REPO_ROOT)}")
    return 0


def cmd_add_batch(args):
    """批次寫；--json 接 list[dict]，每 dict 對應 row 欄位（不含 battle_id，從 --battle-id 補）"""
    try:
        items = json.loads(args.json)
    except json.JSONDecodeError as e:
        print(f"✗ --json 解析失敗: {e}", file=sys.stderr)
        return 2
    if not isinstance(items, list):
        print(f"✗ --json 必須是 list[dict]", file=sys.stderr)
        return 2

    count = 0
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            print(f"✗ items[{i}] 不是 dict", file=sys.stderr)
            return 2
        try:
            score = _validate_score(item.get("situation_score"))
        except ValueError as e:
            print(f"✗ items[{i}]: {e}", file=sys.stderr)
            return 2
        row = {
            "battle_id": args.battle_id,
            "turn": item.get("turn", ""),
            "player_class": item.get("player_class", args.player_class or ""),
            "card_id": item.get("card_id", ""),
            "card_unique_id": item.get("card_unique_id", ""),
            "card_name": item.get("card_name", ""),
            "card_cost": item.get("card_cost", ""),
            "target_id": item.get("target_id", ""),
            "target_class": item.get("target_class", ""),
            "damage_or_effect": item.get("damage_or_effect", ""),
            "situation_score": score,
            "combo_chain": item.get("combo_chain", ""),
        }
        _append_row(row)
        count += 1
    print(f"✓ batch scored {count} cards for battle {args.battle_id}")
    return 0


def cmd_recent(args):
    if not CSV_PATH.exists():
        print("(CSV 不存在)")
        return 0
    with CSV_PATH.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    tail = rows[-args.n:] if args.n > 0 else rows
    if not tail:
        print("(no card scores yet)")
        return 0
    print(f"# Recent {len(tail)} card scores (of {len(rows)} total)")
    print()
    print("| battle | turn | class | card | cost | target | dmg/eff | score | combo |")
    print("|---|---|---|---|---|---|---|---|---|")
    for r in tail:
        print(f"| {r.get('battle_id','')} | {r.get('turn','')} | {r.get('player_class','')} | "
              f"{r.get('card_name','')} | {r.get('card_cost','')} | {r.get('target_class','')} | "
              f"{r.get('damage_or_effect','')} | {r.get('situation_score','')} | {r.get('combo_chain','')} |")
    return 0


def main():
    parser = argparse.ArgumentParser(description="T04 QA Card Power Scorer")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="記一張出牌評分")
    p_add.add_argument("--battle-id", required=True)
    p_add.add_argument("--turn", type=int, required=True)
    p_add.add_argument("--player-class", required=True)
    p_add.add_argument("--card-id", required=True, help="卡牌 RCG_CardData id")
    p_add.add_argument("--card-unique-id", default="", help="該場戰鬥內手牌 unique index (Cmd_BattleSnapshot 顯示的 [N])")
    p_add.add_argument("--card-name", required=True)
    p_add.add_argument("--card-cost", required=True)
    p_add.add_argument("--target-id", default="")
    p_add.add_argument("--target-class", default="")
    p_add.add_argument("--damage-or-effect", default="", help="實際造成的傷害或效果描述")
    p_add.add_argument("--situation-score", required=True, help="1-5 分 (見 docstring 評分標準)")
    p_add.add_argument("--combo-chain", default="", help="觸發的 combo/synergy 描述")
    p_add.set_defaults(func=cmd_add)

    p_batch = sub.add_parser("add-batch", help="批次寫多張卡 (JSON list)")
    p_batch.add_argument("--battle-id", required=True)
    p_batch.add_argument("--player-class", default="", help="統一 player_class (item 內可覆寫)")
    p_batch.add_argument("--json", required=True, help="JSON list[dict] (每 dict 對應 row)")
    p_batch.set_defaults(func=cmd_add_batch)

    p_rec = sub.add_parser("recent", help="看最近 N 筆")
    p_rec.add_argument("-n", type=int, default=10)
    p_rec.set_defaults(func=cmd_recent)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
