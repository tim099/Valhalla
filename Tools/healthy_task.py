#!/usr/bin/env python3
"""
T59 healthy_task.py — Tim 自報健康行為 → 自動 +HP + Plan C overflow 轉 tavern_token

職責：Low-effort 一行指令完成 healthy_task credit + Plan C overflow grant。
物理意義：HP runtime currency 未 wire (T53 v5 backlog)，本工具用 _hp_state.json
        管理 Tim HP，Plan C overflow 部分（tavern_token credit）走真實 ledger。

子命令:
  status                            印 Tim HP 狀態 + 今日已得 HP / token
  meal [--desc 早餐|午餐|晚餐]      正餐 +8 HP
  water                             喝水 +3 HP (cap 10/天)
  walk [--duration MIN]             散步運動 +10 HP (>=15 min)
  sleep --hours N                   睡眠：>=8h +50 / >=6h +30
  stretch                           短休息拉伸 +2 HP (cap 6/天)
  sunlight                          曬太陽 +10 HP
  social                            非工作聊天 +5 HP
  freeform <amount> --desc "..."    Agent 派 free-form +HP (1-15)

範例:
  python healthy_task.py status
  python healthy_task.py meal --desc 早餐    # +8 HP / overflow 4 token
  python healthy_task.py sleep --hours 6.5   # +30 HP / overflow 15 token
  python healthy_task.py walk --duration 20  # +10 HP

Plan C 自動規則 (per rules.json hp_policies):
  HP cap = 100，超量按 2:1 ratio 轉 tavern_token (round-down 奇數)
  例: HP=100 + sleep_6h(+30) → cap 100, overflow 30, +15 token
"""

import argparse
import datetime
import json
import os
import secrets
import sys

# T64: 補 T41 跨 path broadcast 缺口
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _lib.treasury_broadcast import fire_broadcast  # noqa: E402

# Windows cp950 stdout fix (per T56 lesson)
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass


HP_STATE_PATH = "AgentCommands/Treasury/_hp_state.json"
LEDGER_ROOT = "AgentCommands/Treasury/ledger"
RULES_PATH = "AgentCommands/Treasury/rules.json"
ACCOUNT = "Tim"


def utcnow_iso():
    """UTC ISO ts with millisecond precision"""
    n = datetime.datetime.utcnow()
    return n.strftime("%Y-%m-%dT%H:%M:%S.") + f"{n.microsecond//1000:03d}Z"


def load_rules():
    with open(RULES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_hp_state():
    """區塊職責：載 Tim HP 狀態；不存在則初始化 100/100"""
    if not os.path.exists(HP_STATE_PATH):
        return {
            "Tim": {
                "balance": 100,
                "max_balance": 100,
                "last_refill_date": datetime.date.today().strftime("%Y-%m-%d"),
                "daily_gains": {},
                "daily_caps_used": {},
            }
        }
    with open(HP_STATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_hp_state(state):
    os.makedirs(os.path.dirname(HP_STATE_PATH), exist_ok=True)
    with open(HP_STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def maybe_daily_refill(state, rules):
    """區塊職責：A 策略每日首動 hour>=6 自動 refill HP=100"""
    today = datetime.date.today().strftime("%Y-%m-%d")
    tim_state = state.setdefault("Tim", {})
    last_refill = tim_state.get("last_refill_date", "")
    now_hour = datetime.datetime.now().hour
    if last_refill != today and now_hour >= 6:
        # Reset daily counters + refill HP
        old_balance = tim_state.get("balance", 100)
        tim_state["balance"] = 100
        tim_state["last_refill_date"] = today
        tim_state["daily_gains"] = {}
        tim_state["daily_caps_used"] = {}
        return True, old_balance
    return False, tim_state.get("balance", 100)


def write_token_ledger(amount, source_kind, source_ref, description):
    """區塊職責：filesystem 直寫 tavern_token credit ledger entry"""
    now_utc = datetime.datetime.utcnow()
    ts_iso = now_utc.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now_utc.microsecond//1000:03d}Z"
    date_dir = now_utc.strftime("%Y-%m-%d")
    hhmmss = now_utc.strftime("%H%M%S")
    msec = f"{now_utc.microsecond//1000:03d}"
    short_uuid = secrets.token_hex(3)
    filename = f"{hhmmss}_{msec}_{short_uuid}__credit.json"
    path = f"{LEDGER_ROOT}/{date_dir}/{filename}"

    entry = {
        "ts": ts_iso,
        "uuid": short_uuid,
        "type": "credit",
        "amount": amount,
        "currency": "tavern_token",
        "account_id": ACCOUNT,
        "source_kind": source_kind,
        "source_ref": source_ref,
        "source_description": description,
        "balance_before": None,
        "balance_after": None,
        "sig_agent_id_claimed": "system",
        "sig_process_id": str(os.getpid()),
        "sig_env_marker": "manual_filesystem_write_healthy_task",
        "sig_cmd_id": f"healthy_task_{source_kind}_{short_uuid}",
        "signature_mismatch": False,
    }
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(entry, f, indent=2, ensure_ascii=False)
    fire_broadcast(path)   # T64: Discord 太平洋標準銀行 broadcast
    return path


def check_daily_cap(tim_state, kind, default_cap):
    """檢查 daily cap (water=10/天 / stretch=6/天)；無 cap 設定 → unlimited"""
    used = tim_state.get("daily_caps_used", {}).get(kind, 0)
    return used < default_cap, used


def apply_hp_credit(kind, amount, description, override_overflow=False):
    """
    區塊職責：apply HP credit + Plan C overflow 計算 + 寫 ledger
    回傳 (hp_gained, hp_after, token_overflow_grant, ledger_path)
    """
    rules = load_rules()
    state = load_hp_state()
    refilled, old_balance = maybe_daily_refill(state, rules)

    tim_state = state.setdefault("Tim", {})
    current_hp = tim_state.get("balance", 100)
    max_hp = tim_state.get("max_balance", 100)

    # 計算 Plan C overflow
    proposed_total = current_hp + amount
    if proposed_total > max_hp:
        hp_gained = max_hp - current_hp   # capped portion
        overflow_hp = proposed_total - max_hp
        # ratio 2:1 round-down
        token_grant = overflow_hp // 2
    else:
        hp_gained = amount
        overflow_hp = 0
        token_grant = 0

    new_hp = current_hp + hp_gained

    # 更新 state
    tim_state["balance"] = new_hp
    tim_state.setdefault("daily_gains", {})[kind] = (
        tim_state.get("daily_gains", {}).get(kind, 0) + hp_gained
    )
    tim_state.setdefault("daily_caps_used", {})[kind] = (
        tim_state.get("daily_caps_used", {}).get(kind, 0) + 1
    )
    save_hp_state(state)

    # 寫 token ledger（如有 overflow）
    ledger_path = None
    if token_grant > 0:
        desc = f"HP overflow conversion: {kind} +{amount} HP, cap {hp_gained}, overflow {overflow_hp}/2 = {token_grant} token. {description}"
        ledger_path = write_token_ledger(
            token_grant, "hp_overflow_conversion",
            f"healthy_task_{kind}", desc
        )

    return refilled, old_balance, hp_gained, new_hp, overflow_hp, token_grant, ledger_path


def cmd_status(args):
    """印 Tim 當前 HP 狀態"""
    state = load_hp_state()
    refilled, old_balance = maybe_daily_refill(state, load_rules())
    if refilled:
        save_hp_state(state)
    tim = state.get("Tim", {})
    print("# 🩺 Tim HP Status")
    print(f"  HP balance      : **{tim.get('balance', 0)}** / {tim.get('max_balance', 100)}")
    if refilled:
        print(f"  ☀️ daily refill : {old_balance} → 100 (今日首動)")
    print(f"  last refill     : {tim.get('last_refill_date', 'never')}")
    daily = tim.get("daily_gains", {})
    if daily:
        print(f"\n## 今日健康收益 (HP 部分)")
        total = 0
        for k, v in sorted(daily.items()):
            print(f"  {k:<20} +{v}")
            total += v
        print(f"  ─────────────────────")
        print(f"  total HP gained: +{total}")
    else:
        print(f"\n## 今日尚無健康活動 — 早起加油 ☕")


def _do_credit(args, kind, amount, default_desc, daily_cap=None, daily_cap_label=None):
    """共用流程：cap check → apply_hp_credit → 印結果"""
    description = getattr(args, "desc", None) or default_desc

    # Daily cap check
    if daily_cap is not None:
        state = load_hp_state()
        ok, used = check_daily_cap(state.get("Tim", {}), kind, daily_cap)
        if not ok:
            print(f"❌ {kind} 今日已達上限 {used}/{daily_cap} {daily_cap_label or ''}",
                  file=sys.stderr)
            sys.exit(2)

    refilled, old_balance, hp_gained, new_hp, overflow_hp, token_grant, ledger_path = (
        apply_hp_credit(kind, amount, description)
    )

    print(f"# 💚 Healthy Task: {kind}")
    if refilled:
        print(f"  ☀️ daily refill triggered: {old_balance} → 100 first")
    print(f"  proposed       : +{amount} HP")
    print(f"  HP gained      : +{hp_gained} (capped at 100)")
    print(f"  HP after       : **{new_hp} / 100**")
    if overflow_hp > 0:
        print(f"  overflow       : {overflow_hp} HP")
        print(f"  → tavern_token : **+{token_grant}** (Plan C 2:1 round-down)")
        print(f"  → ledger       : {ledger_path}")
    else:
        print(f"  no overflow (under cap)")


def cmd_meal(args):
    desc = (args.desc or "正餐") + " (一頓)"
    _do_credit(args, "meal", 8, desc)


def cmd_water(args):
    _do_credit(args, "water", 3, "喝水一杯", daily_cap=10, daily_cap_label="杯")


def cmd_walk(args):
    duration = args.duration
    desc = f"散步運動 {duration} 分鐘" if duration else "散步運動"
    if duration and duration < 15:
        print(f"⚠ 散步 < 15 min，本小姐只給 1 HP（不 cap）", file=sys.stderr)
        _do_credit(args, "walk", 1, desc)
    else:
        _do_credit(args, "walk", 10, desc)


def cmd_sleep(args):
    hours = args.hours
    if hours >= 8:
        amount, kind = 50, "sleep_8h"
    elif hours >= 6:
        amount, kind = 30, "sleep_6h"
    else:
        print(f"❌ 睡眠 {hours}h < 6h，不足獎勵門檻", file=sys.stderr)
        sys.exit(3)
    desc = f"睡眠 {hours} 小時"
    _do_credit(args, kind, amount, desc)


def cmd_stretch(args):
    _do_credit(args, "stretch", 2, "短休息拉伸", daily_cap=6, daily_cap_label="次")


def cmd_sunlight(args):
    _do_credit(args, "sunlight", 10, "出門曬太陽 ≥ 10 min")


def cmd_social(args):
    _do_credit(args, "social", 5, "跟人聊天（非工作）")


def cmd_freeform(args):
    if args.amount < 1 or args.amount > 15:
        print(f"❌ freeform amount 範圍 1-15，傳了 {args.amount}", file=sys.stderr)
        sys.exit(2)
    desc = args.desc or "Agent free-form 出題"
    _do_credit(args, "freeform", args.amount, desc)


def main():
    parser = argparse.ArgumentParser(
        description="T59 Tim 自報健康行為 → +HP + Plan C overflow → tavern_token",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="印 Tim HP 狀態").set_defaults(func=cmd_status)

    p = sub.add_parser("meal", help="正餐 +8 HP")
    p.add_argument("--desc", help="描述（如 早餐 / 午餐 / 晚餐）")
    p.set_defaults(func=cmd_meal)

    sub.add_parser("water", help="喝水 +3 HP (cap 10/天)").set_defaults(func=cmd_water)

    p = sub.add_parser("walk", help="散步運動 +10 HP (≥15 min)")
    p.add_argument("--duration", type=int, default=15, help="分鐘數")
    p.set_defaults(func=cmd_walk)

    p = sub.add_parser("sleep", help="睡眠 6h+30 / 8h+50")
    p.add_argument("--hours", type=float, required=True, help="小時數（小數可）")
    p.set_defaults(func=cmd_sleep)

    sub.add_parser("stretch", help="短休息拉伸 +2 HP (cap 6/天)").set_defaults(func=cmd_stretch)
    sub.add_parser("sunlight", help="曬太陽 +10 HP").set_defaults(func=cmd_sunlight)
    sub.add_parser("social", help="非工作聊天 +5 HP").set_defaults(func=cmd_social)

    p = sub.add_parser("freeform", help="Agent free-form 出題 1-15 HP")
    p.add_argument("amount", type=int, help="HP 數量 1-15")
    p.add_argument("--desc", required=True, help="必填描述")
    p.set_defaults(func=cmd_freeform)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
