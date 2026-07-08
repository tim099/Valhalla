#!/usr/bin/env python3
"""
T59 morning_status.py — Tim 早晨 dashboard，一行看完一切

職責：Low-effort 模式的 cognitive load reducer — 跑一次看整體狀態。
物理意義：彙整 HP / token / 24h tavern 活動 / 今日結算 / 待辦提示，
        Tim 不必腦補多 source 資料。

範例:
  python AgentCommands/Tools/morning_status.py
  python AgentCommands/Tools/morning_status.py --verbose   # 包含詳細 ledger entries
"""

import argparse
import datetime
import glob
import json
import os
import subprocess
import sys

# Windows utf-8 fix
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass


HP_STATE_PATH = "AgentCommands/Treasury/_hp_state.json"
LEDGER_ROOT = "AgentCommands/Treasury/ledger"
TAVERN_ROOT = "AgentCommands/ChatTavern/rooms"


def calc_fee(hour):
    """區塊職責：算當前時段 health_fee"""
    if 22 <= hour < 23: return 0
    if 23 <= hour < 24: return 1
    if 0 <= hour < 1: return 3
    if 1 <= hour < 2: return 5
    if 2 <= hour < 3: return 8
    if 3 <= hour < 6: return 10
    return 0


def fee_zone_label(hour, fee):
    """區塊職責：色 zone 標籤"""
    if fee == 0 and hour >= 6 and hour < 22:
        return "🟢 GREEN ZONE"
    if hour == 22:
        return "🟡 YELLOW (22h soft warning)"
    if hour == 23:
        return f"🟠 ORANGE (23h fee={fee})"
    if 0 <= hour < 6:
        return f"🔴 RED ({hour}h fee={fee})"
    return "?"


def get_tim_hp():
    """讀 _hp_state.json 取 Tim HP"""
    if not os.path.exists(HP_STATE_PATH):
        return 100, 100, "init"
    with open(HP_STATE_PATH, "r", encoding="utf-8") as f:
        s = json.load(f)
    tim = s.get("Tim", {})
    return tim.get("balance", 100), tim.get("max_balance", 100), tim.get("last_refill_date", "?")


def hp_zone(hp):
    """區塊職責：HP zone (warning_zones per rules.json)"""
    if hp >= 51: return "🟢 normal"
    if hp >= 21: return "🟡 yellow (建議補健康行為)"
    if hp >= 1: return "🟠 orange (強建議休息)"
    return "🔴 red (HP 透支，每 task 必問)"


def calc_balance(account):
    """區塊職責：scan ledger 算指定 account 的 tavern_token balance"""
    total_c = 0
    total_d = 0
    for f in sorted(glob.glob(f"{LEDGER_ROOT}/*/*.json")):
        try:
            with open(f, "r", encoding="utf-8") as fp:
                e = json.load(fp)
        except (OSError, json.JSONDecodeError):
            continue
        if e.get("account_id") != account:
            continue
        if e.get("currency", "tavern_token") != "tavern_token":
            continue
        if e.get("type") == "credit":
            total_c += e.get("amount", 0)
        else:
            total_d += e.get("amount", 0)
    return total_c - total_d


def today_token_changes(account):
    """區塊職責：算 Tim 今日 (UTC date) tavern_token 進出"""
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    today_path = f"{LEDGER_ROOT}/{today}"
    if not os.path.isdir(today_path):
        return [], 0, 0
    entries = []
    credit_total = 0
    debit_total = 0
    for fname in sorted(os.listdir(today_path)):
        if not fname.endswith(".json"):
            continue
        try:
            with open(os.path.join(today_path, fname), "r", encoding="utf-8") as f:
                e = json.load(f)
        except (OSError, json.JSONDecodeError):
            continue
        if e.get("account_id") != account:
            continue
        entries.append(e)
        amt = e.get("amount", 0)
        if e.get("type") == "credit":
            credit_total += amt
        else:
            debit_total += amt
    return entries, credit_total, debit_total


def tavern_active_rooms_24h():
    """區塊職責：呼叫 tavern_query.py 取 24h 活躍房 raw"""
    try:
        result = subprocess.run(
            [sys.executable, "AgentCommands/Tools/tavern_query.py", "rooms", "--since", "24h"],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        return result.stdout.strip()
    except Exception as e:
        return f"(query fail: {e})"


def get_recent_tavern_messages(limit=5):
    """區塊職責：跨房 timeline 最近 N 則"""
    try:
        result = subprocess.run(
            [sys.executable, "AgentCommands/Tools/tavern_query.py", "timeline",
             "--since", "24h", "--limit", str(limit)],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        return result.stdout.strip()
    except Exception as e:
        return f"(query fail: {e})"


def get_pending_inbox(account):
    """區塊職責：列出 account inbox 未讀（看 mtime > X 小時）"""
    inbox_paths = glob.glob(f"AgentCommands/ChatTavern/rooms/*/inbox/{account}.md")
    pending = []
    for p in inbox_paths:
        if not os.path.exists(p):
            continue
        size = os.path.getsize(p)
        mtime = os.path.getmtime(p)
        if size > 0:
            pending.append((p, mtime, size))
    return pending


def main():
    parser = argparse.ArgumentParser(description="T59 Tim morning dashboard")
    parser.add_argument("--verbose", action="store_true", help="印詳細 ledger entries")
    parser.add_argument("--account", default="Tim", help="預設 Tim")
    args = parser.parse_args()

    now = datetime.datetime.now()
    hour = now.hour
    fee = calc_fee(hour)
    zone = fee_zone_label(hour, fee)

    print("=" * 72)
    print(f"  🌅 Morning Status — {now.strftime('%Y-%m-%d %H:%M:%S')} (local)")
    print("=" * 72)

    # ─── Section 1: 健康狀態 ───
    hp, max_hp, last_refill = get_tim_hp()
    print(f"\n## 🩺 Health Guardian")
    print(f"  zone           : {zone}")
    print(f"  health_fee     : {fee} token / task")
    print(f"  Tim HP         : **{hp} / {max_hp}** ({hp_zone(hp)})")
    print(f"  last refill    : {last_refill}")

    # ─── Section 2: Treasury ───
    balance = calc_balance(args.account)
    print(f"\n## 💰 Treasury")
    print(f"  {args.account} balance: **{balance}** tavern_token")
    bartender = calc_balance("tavern-keeper")
    print(f"  bartender (酒保): {bartender} tavern_token")

    entries, credit_total, debit_total = today_token_changes(args.account)
    print(f"\n## 📜 今日 Token 流水 ({len(entries)} 筆)")
    print(f"  credit total : +{credit_total}")
    print(f"  debit total  : -{debit_total}")
    print(f"  net          : {credit_total - debit_total:+d}")

    if args.verbose and entries:
        print(f"\n  詳細 entries:")
        for e in entries[-10:]:
            ts = e.get("ts", "")[:19]
            kind = e.get("source_kind") or e.get("use_kind") or "?"
            tp = e.get("type", "?")
            amt = e.get("amount", 0)
            sign = "+" if tp == "credit" else "-"
            print(f"    {ts} {sign}{amt:>3} {kind:<28} {(e.get('source_description') or '')[:40]}")

    # ─── Section 3: Tavern 活動 ───
    print(f"\n## 🏨 Tavern 24h 活躍房")
    rooms_out = tavern_active_rooms_24h()
    # 縮減 output 只保前 5 行
    for line in rooms_out.split("\n")[:8]:
        print(f"  {line}")

    if args.verbose:
        print(f"\n## ⏱ 跨房最近 5 則訊息")
        timeline_out = get_recent_tavern_messages(5)
        for line in timeline_out.split("\n")[:8]:
            print(f"  {line}")

    # ─── Section 4: Inbox ───
    pending = get_pending_inbox(args.account)
    if pending:
        print(f"\n## 📬 {args.account} Inbox")
        for p, mtime, size in pending:
            mtime_str = datetime.datetime.fromtimestamp(mtime).strftime("%m-%d %H:%M")
            # 區塊職責：跨 platform 拆 room name (Windows \\ vs Unix /)
            # path: .../ChatTavern/rooms/<ROOM>/inbox/Tim.md
            inbox_dir = os.path.dirname(p)        # .../<ROOM>/inbox
            room = os.path.basename(os.path.dirname(inbox_dir))   # <ROOM>
            print(f"  {mtime_str}  {room:<30}  {size:>5} bytes")

    # ─── Section 5: 提示 ───
    print(f"\n## 💡 提示")
    if hp == max_hp:
        print(f"  - HP 滿血 → healthy_task overflow 全 grant token (Plan C 2:1)")
        print(f"    → 建議：早餐 +8HP→+4token / 喝水 +3HP→+1token")
    elif hp >= 51:
        print(f"  - HP normal 但未滿，補健康行為直接 +HP（不 overflow）")
    else:
        print(f"  - HP {hp_zone(hp)} — 強建議補休息再開工")

    if balance == 0:
        print(f"  - tavern_token 0 餘額 — 派 task 會 hard stop fee；建議 self-grant 或先做健康行為")
    elif balance < 5:
        print(f"  - tavern_token 偏低 ({balance})，派 task 前注意 fee")

    if hour >= 22 or hour < 6:
        print(f"  - ⚠ 進入收費時段 — fee={fee} token / task。考慮收工")

    print()


if __name__ == "__main__":
    main()
