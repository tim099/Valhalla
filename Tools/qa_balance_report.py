#!/usr/bin/env python3
"""
T07 qa_balance_report.py — QA Battle Balance Report Aggregator (Plan §3 row "Cmd_BalanceReport")

職責：跨 4 CSV (qa_battle_results / card_power_log / item_equipment_log / state_effect_log)
       匯總 → markdown summary，寫進 AgentCommands/QA_Battle_Logs/_balance_reports/<YYYY-MM-DD>/<run_id>.md

物理意義：純讀檔聚合，不動原 CSV；無 Unity 依賴，可離線跑（Tim 跑/agent 跑都行）。

子命令:
  run [--run-id ID] [--filter-preset PRESET_ID] [--top N]
                                     產生一份 balance report
  preview                            印目前 CSV row count 統計（debug，不寫檔）

範例:
  python AgentCommands/Tools/qa_balance_report.py run --top 10
  python AgentCommands/Tools/qa_balance_report.py preview
"""

import argparse
import csv
import datetime
import os
import statistics
import sys
from collections import defaultdict
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

# 區塊職責：固定路徑配置
# 物理意義：所有 path 相對 repo root；script 在 AgentCommands/Tools/ → repo root = ../../
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
LOGS_DIR = REPO_ROOT / "AgentCommands" / "QA_Battle_Logs"
REPORTS_DIR = LOGS_DIR / "_balance_reports"

BATTLE_CSV = LOGS_DIR / "qa_battle_results.csv"
CARD_CSV = LOGS_DIR / "card_power_log.csv"
ITEM_CSV = LOGS_DIR / "item_equipment_log.csv"
STATE_CSV = LOGS_DIR / "state_effect_log.csv"


def _read_csv(path: Path) -> list[dict]:
    """讀 CSV 成 list[dict]；不存在或空檔回 []"""
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [row for row in reader if any((v or "").strip() for v in row.values())]


def _safe_float(s, default=0.0) -> float:
    try:
        return float(s)
    except (TypeError, ValueError):
        return default


def _safe_int(s, default=0) -> int:
    try:
        return int(float(s))
    except (TypeError, ValueError):
        return default


def _avg(values: list[float]) -> float | None:
    return statistics.mean(values) if values else None


def _fmt(v, digits=2) -> str:
    if v is None:
        return "-"
    if isinstance(v, float):
        return f"{v:.{digits}f}"
    return str(v)


def aggregate_battles(rows: list[dict], filter_preset: str | None = None) -> dict:
    """聚合 qa_battle_results.csv → 統計戰鬥宏觀指標"""
    # 區塊職責：把每場戰鬥的 outcome / turn_count / damage / difficulty 分桶
    # 物理意義：preset_id 跟 player_class 各自 group，看哪組合贏太多 / 輸太多
    if filter_preset:
        rows = [r for r in rows if (r.get("preset_id") or "").strip() == filter_preset]

    total = len(rows)
    wins = sum(1 for r in rows if (r.get("outcome") or "").upper() == "WIN")
    losses = sum(1 for r in rows if (r.get("outcome") or "").upper() == "LOSS")
    retreats = sum(1 for r in rows if (r.get("outcome") or "").upper() == "RETREAT")

    turn_counts = [_safe_float(r.get("turn_count")) for r in rows if r.get("turn_count")]
    diff_scores = [_safe_float(r.get("difficulty_score")) for r in rows if r.get("difficulty_score")]
    dmg_dealt = [_safe_float(r.get("damage_dealt")) for r in rows if r.get("damage_dealt")]
    dmg_taken = [_safe_float(r.get("damage_taken")) for r in rows if r.get("damage_taken")]

    by_preset = defaultdict(list)
    by_class = defaultdict(list)
    for r in rows:
        if r.get("preset_id"):
            by_preset[r["preset_id"]].append(r)
        if r.get("player_class"):
            by_class[r["player_class"]].append(r)

    def _group_stats(group_rows: list[dict]) -> dict:
        n = len(group_rows)
        w = sum(1 for r in group_rows if (r.get("outcome") or "").upper() == "WIN")
        return {
            "n": n,
            "win_rate": (w / n) if n else None,
            "avg_turns": _avg([_safe_float(r.get("turn_count")) for r in group_rows if r.get("turn_count")]),
            "avg_difficulty": _avg([_safe_float(r.get("difficulty_score")) for r in group_rows if r.get("difficulty_score")]),
        }

    return {
        "total": total,
        "wins": wins,
        "losses": losses,
        "retreats": retreats,
        "win_rate": (wins / total) if total else None,
        "avg_turns": _avg(turn_counts),
        "avg_difficulty": _avg(diff_scores),
        "avg_damage_dealt": _avg(dmg_dealt),
        "avg_damage_taken": _avg(dmg_taken),
        "by_preset": {k: _group_stats(v) for k, v in by_preset.items()},
        "by_class": {k: _group_stats(v) for k, v in by_class.items()},
    }


def aggregate_cards(rows: list[dict], top_n: int = 10) -> dict:
    """聚合 card_power_log.csv → 每張卡的平均強度 + top/bottom"""
    # 區塊職責：每張卡 group by card_id+card_name，算平均 situation_score 與出牌頻率
    # 物理意義：avg_score 5 = 完美 timing；avg_score 1 = 浪費。top/bottom 揭示卡牌強度極端值
    by_card = defaultdict(list)
    for r in rows:
        key = (r.get("card_id") or "?", r.get("card_name") or "?")
        score = _safe_float(r.get("situation_score"))
        if score > 0:
            by_card[key].append(score)

    card_stats = []
    for (cid, name), scores in by_card.items():
        card_stats.append({
            "card_id": cid,
            "card_name": name,
            "plays": len(scores),
            "avg_score": _avg(scores),
            "min_score": min(scores),
            "max_score": max(scores),
        })

    # 排序：先 avg_score 高/低
    card_stats_sorted = sorted(card_stats, key=lambda x: (x["avg_score"] or 0), reverse=True)
    return {
        "total_plays": len(rows),
        "unique_cards": len(by_card),
        "top": card_stats_sorted[:top_n],
        "bottom": list(reversed(card_stats_sorted[-top_n:])) if len(card_stats_sorted) > top_n else [],
    }


def aggregate_items(rows: list[dict], top_n: int = 10) -> dict:
    """聚合 item_equipment_log.csv → 道具 / 裝備強度"""
    by_item = defaultdict(list)
    for r in rows:
        kind = r.get("kind") or "?"
        key = (kind, r.get("id") or "?", r.get("name") or "?")
        score = _safe_float(r.get("score"))
        if score > 0:
            by_item[key].append(score)

    items = []
    for (kind, iid, name), scores in by_item.items():
        items.append({
            "kind": kind,
            "id": iid,
            "name": name,
            "uses": len(scores),
            "avg_score": _avg(scores),
        })
    items_sorted = sorted(items, key=lambda x: (x["avg_score"] or 0), reverse=True)
    return {
        "total_uses": len(rows),
        "unique_items": len(by_item),
        "top": items_sorted[:top_n],
        "bottom": list(reversed(items_sorted[-top_n:])) if len(items_sorted) > top_n else [],
    }


def aggregate_states(rows: list[dict], top_n: int = 10) -> dict:
    """聚合 state_effect_log.csv → buff/debuff 觸發頻率"""
    by_effect = defaultdict(lambda: {"applied": 0, "triggers": [], "stacks": [], "values": []})
    for r in rows:
        key = (r.get("effect_id") or "?", r.get("effect_name") or "?")
        e = by_effect[key]
        e["applied"] += 1
        if r.get("trigger_count"):
            e["triggers"].append(_safe_int(r.get("trigger_count")))
        if r.get("stack_count"):
            e["stacks"].append(_safe_int(r.get("stack_count")))
        if r.get("total_value"):
            e["values"].append(_safe_float(r.get("total_value")))

    effects = []
    for (eid, name), data in by_effect.items():
        effects.append({
            "effect_id": eid,
            "effect_name": name,
            "applied": data["applied"],
            "avg_triggers": _avg(data["triggers"]),
            "avg_stacks": _avg(data["stacks"]),
            "avg_value": _avg(data["values"]),
        })
    effects_sorted = sorted(effects, key=lambda x: x["applied"], reverse=True)
    return {
        "total_applications": len(rows),
        "unique_effects": len(by_effect),
        "top_applied": effects_sorted[:top_n],
    }


def build_report_md(
    battles: dict, cards: dict, items: dict, states: dict,
    run_id: str, filter_preset: str | None,
) -> str:
    """組 markdown report"""
    # 區塊職責：把 4 個 aggregate dict 轉成 human-readable markdown
    # 物理意義：給 Tim 看的最終 balance report；同時是 git 入檔的 audit snapshot
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    sb = []
    sb.append(f"# 📊 QA Balance Report — `{run_id}`")
    sb.append("")
    sb.append(f"- generated: {now}")
    if filter_preset:
        sb.append(f"- filter: `preset_id={filter_preset}`")
    sb.append(f"- data source: `AgentCommands/QA_Battle_Logs/*.csv`")
    sb.append("")

    sb.append("## 1. Battle Overview")
    sb.append("")
    total = battles["total"]
    if total == 0:
        sb.append("⚠ **no battle data** — qa_battle_results.csv 是空的，跑 `record_battle_result.py` 先填資料")
    else:
        sb.append(f"- 總戰場: **{total}** (win {battles['wins']} / loss {battles['losses']} / retreat {battles['retreats']})")
        wr = battles["win_rate"]
        sb.append(f"- 勝率: **{_fmt(wr * 100 if wr is not None else None, 1)}%**")
        sb.append(f"- 平均回合: {_fmt(battles['avg_turns'])} | 平均難度分: {_fmt(battles['avg_difficulty'])}")
        sb.append(f"- 平均輸出: {_fmt(battles['avg_damage_dealt'])} | 平均承傷: {_fmt(battles['avg_damage_taken'])}")
    sb.append("")

    if battles["by_preset"]:
        sb.append("### 1a. By Preset")
        sb.append("")
        sb.append("| preset_id | n | win_rate | avg_turns | avg_difficulty |")
        sb.append("|---|---|---|---|---|")
        for preset, s in sorted(battles["by_preset"].items()):
            wr = s["win_rate"]
            sb.append(f"| `{preset}` | {s['n']} | {_fmt(wr * 100 if wr is not None else None, 1)}% | {_fmt(s['avg_turns'])} | {_fmt(s['avg_difficulty'])} |")
        sb.append("")

    if battles["by_class"]:
        sb.append("### 1b. By Player Class")
        sb.append("")
        sb.append("| player_class | n | win_rate | avg_turns | avg_difficulty |")
        sb.append("|---|---|---|---|---|")
        for cls, s in sorted(battles["by_class"].items()):
            wr = s["win_rate"]
            sb.append(f"| `{cls}` | {s['n']} | {_fmt(wr * 100 if wr is not None else None, 1)}% | {_fmt(s['avg_turns'])} | {_fmt(s['avg_difficulty'])} |")
        sb.append("")

    sb.append("## 2. Card Power")
    sb.append("")
    if cards["total_plays"] == 0:
        sb.append("⚠ **no card data** — card_power_log.csv 是空的，跑 `score_card.py` 先填資料")
    else:
        sb.append(f"- 出牌總數: **{cards['total_plays']}** | 不同卡: **{cards['unique_cards']}**")
        sb.append("")
        if cards["top"]:
            sb.append("### 2a. Top 強卡 (avg_score 高)")
            sb.append("")
            sb.append("| card_id | card_name | plays | avg_score | min | max |")
            sb.append("|---|---|---|---|---|---|")
            for c in cards["top"]:
                sb.append(f"| {c['card_id']} | {c['card_name']} | {c['plays']} | {_fmt(c['avg_score'])} | {_fmt(c['min_score'])} | {_fmt(c['max_score'])} |")
            sb.append("")
        if cards["bottom"]:
            sb.append("### 2b. Bottom 弱卡 (avg_score 低)")
            sb.append("")
            sb.append("| card_id | card_name | plays | avg_score | min | max |")
            sb.append("|---|---|---|---|---|---|")
            for c in cards["bottom"]:
                sb.append(f"| {c['card_id']} | {c['card_name']} | {c['plays']} | {_fmt(c['avg_score'])} | {_fmt(c['min_score'])} | {_fmt(c['max_score'])} |")
            sb.append("")

    sb.append("## 3. Item / Equipment Power")
    sb.append("")
    if items["total_uses"] == 0:
        sb.append("⚠ **no item data** — item_equipment_log.csv 是空的")
    else:
        sb.append(f"- 道具使用總數: **{items['total_uses']}** | 不同道具: **{items['unique_items']}**")
        sb.append("")
        if items["top"]:
            sb.append("### 3a. Top 強道具")
            sb.append("")
            sb.append("| kind | id | name | uses | avg_score |")
            sb.append("|---|---|---|---|---|")
            for it in items["top"]:
                sb.append(f"| {it['kind']} | {it['id']} | {it['name']} | {it['uses']} | {_fmt(it['avg_score'])} |")
            sb.append("")

    sb.append("## 4. State Effects (buff / debuff)")
    sb.append("")
    if states["total_applications"] == 0:
        sb.append("⚠ **no state data** — state_effect_log.csv 是空的，跑 `Cmd_BattleStateInspect` 先填資料")
    else:
        sb.append(f"- 狀態套用次數: **{states['total_applications']}** | 不同效果: **{states['unique_effects']}**")
        sb.append("")
        if states["top_applied"]:
            sb.append("### 4a. 最常觸發 (applied count)")
            sb.append("")
            sb.append("| effect_id | effect_name | applied | avg_triggers | avg_stacks | avg_value |")
            sb.append("|---|---|---|---|---|---|")
            for e in states["top_applied"]:
                sb.append(f"| {e['effect_id']} | {e['effect_name']} | {e['applied']} | {_fmt(e['avg_triggers'])} | {_fmt(e['avg_stacks'])} | {_fmt(e['avg_value'])} |")
            sb.append("")

    sb.append("---")
    sb.append("")
    sb.append("## Balance 觀察筆記 (agent 補白)")
    sb.append("")
    sb.append("> 這段給 agent 跑完 aggregator 後手動補綜合判斷（哪些卡 OP / 哪些 preset 太簡單 / 哪 buff 失衡）。")
    sb.append("")
    return "\n".join(sb)


def cmd_run(args):
    """Subcommand: run — 跑完整 aggregator + 寫 markdown"""
    battles_rows = _read_csv(BATTLE_CSV)
    cards_rows = _read_csv(CARD_CSV)
    items_rows = _read_csv(ITEM_CSV)
    states_rows = _read_csv(STATE_CSV)

    battles = aggregate_battles(battles_rows, filter_preset=args.filter_preset)
    cards = aggregate_cards(cards_rows, top_n=args.top)
    items = aggregate_items(items_rows, top_n=args.top)
    states = aggregate_states(states_rows, top_n=args.top)

    today = datetime.date.today().strftime("%Y-%m-%d")
    run_id = args.run_id or datetime.datetime.now().strftime("run-%H%M%S")
    out_dir = REPORTS_DIR / today
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{run_id}.md"

    md = build_report_md(battles, cards, items, states, run_id=run_id, filter_preset=args.filter_preset)
    out_path.write_text(md, encoding="utf-8")

    print(f"✓ Balance report written: {out_path.relative_to(REPO_ROOT)}")
    print(f"  battles: {battles['total']} | card_plays: {cards['total_plays']} | items: {items['total_uses']} | states: {states['total_applications']}")
    return 0


def cmd_preview(args):
    """Subcommand: preview — 只印 CSV row 統計，不寫檔"""
    for name, p in [
        ("qa_battle_results", BATTLE_CSV),
        ("card_power_log", CARD_CSV),
        ("item_equipment_log", ITEM_CSV),
        ("state_effect_log", STATE_CSV),
    ]:
        rows = _read_csv(p)
        print(f"- {name}: {len(rows)} rows ({p.relative_to(REPO_ROOT)})")
    return 0


def main():
    parser = argparse.ArgumentParser(description="T07 QA Battle Balance Report Aggregator")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="跑 aggregator + 寫 markdown")
    p_run.add_argument("--run-id", default=None, help="覆寫 run id (預設 run-HHMMSS)")
    p_run.add_argument("--filter-preset", default=None, help="只看某個 preset_id")
    p_run.add_argument("--top", type=int, default=10, help="top/bottom 列 N 筆 (預設 10)")
    p_run.set_defaults(func=cmd_run)

    p_prev = sub.add_parser("preview", help="只印 CSV row 統計")
    p_prev.set_defaults(func=cmd_preview)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
