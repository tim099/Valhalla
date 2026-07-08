#!/usr/bin/env python3
"""
T57 gold_convert.py — Phase 1 MVP for Plan_SafeHouse_Gold_Anchor

職責：跨維度錨定 — 把 EOV 局內 Gold 按 100:1 轉成 tavern_token，寫入 Treasury。
物理意義：Antigravity 06:38 拍板的「冒險者 ↔ Agent 命運共同體」實作，
        外部源頭 mint 路徑（不違反 T55 closed economy 因為這是 currency injection）。

設計原則:
  - 100 Gold : 1 Token 固定錨定（rules.json gold_conversion.rate_gold_to_token）
  - daily_cap_tokens=10 防通膨
  - run_uuid 作 idempotency key 防 double-spend
  - Editor offline 時走 filesystem fallback (mirror tavern_query.py 慣例)

範例:
  python gold_convert.py --gold 350 --run-uuid run_2026_05_10_a --account Tim
    → 350 / 100 = 3 token credit Tim
  python gold_convert.py --gold 50 --run-uuid run_X --account Tim
    → 拒絕 (低於 100 最低門檻，無法整除產出 token)
  python gold_convert.py --gold 350 --run-uuid run_2026_05_10_a --account Tim
    → 拒絕 (run_uuid 重複，idempotency check fail)
"""

import argparse
import datetime
import glob
import json
import os
import secrets
import sys

# T64: 路徑修正讓本工具能 import _lib.treasury_broadcast (補 T41 跨 path broadcast 缺口)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _lib.treasury_broadcast import fire_broadcast  # noqa: E402


# 強制 utf-8 stdout (Windows cp950 fix per T56 lesson)
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass


RULES_PATH = "AgentCommands/Treasury/rules.json"
LEDGER_ROOT = "AgentCommands/Treasury/ledger"


def load_rules() -> dict:
    """區塊職責：載入 Treasury rules.json 取得 gold_conversion 設定"""
    with open(RULES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def check_idempotency(run_uuid: str) -> bool:
    """
    區塊職責：檢查 run_uuid 是否已被結算過
    物理意義：scan 所有 ledger entries 找 source_kind=gold_conversion + source_ref=run_uuid
    回傳：True = 重複（已存在），False = 新交易可進
    """
    if not run_uuid:
        return False
    pattern = f"{LEDGER_ROOT}/*/*.json"
    for fpath in glob.glob(pattern):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                e = json.load(f)
        except (OSError, json.JSONDecodeError):
            continue
        if (e.get("source_kind") == "gold_conversion"
                and run_uuid in (e.get("source_ref") or "")):
            return True
    return False


def daily_cap_remaining(account: str, daily_cap: int) -> int:
    """
    區塊職責：算今日已轉換 token 數，回傳剩餘 cap
    物理意義：scan 今日 ledger，找 account + gold_conversion，sum amounts
    """
    today_dir = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    today_path = f"{LEDGER_ROOT}/{today_dir}"
    if not os.path.isdir(today_path):
        return daily_cap
    used = 0
    for fname in os.listdir(today_path):
        if not fname.endswith(".json"):
            continue
        try:
            with open(os.path.join(today_path, fname), "r", encoding="utf-8") as f:
                e = json.load(f)
        except (OSError, json.JSONDecodeError):
            continue
        if (e.get("source_kind") == "gold_conversion"
                and e.get("account_id") == account):
            used += e.get("amount", 0)
    return max(0, daily_cap - used)


def write_ledger_entry(account: str, amount: int, gold_amount: int,
                       run_uuid: str, description: str) -> str:
    """
    區塊職責：filesystem fallback 寫 ledger credit entry
    物理意義：Editor offline 時直接寫 JSON file；Editor 醒後可補簽 sig
    回傳：寫入的 ledger 檔案路徑
    """
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
        "account_id": account,
        "source_kind": "gold_conversion",
        "source_ref": run_uuid,
        "source_description": description,
        "balance_before": None,
        "balance_after": None,
        "sig_agent_id_claimed": "system",
        "sig_process_id": str(os.getpid()),
        "sig_env_marker": "manual_filesystem_write",
        "sig_cmd_id": f"gold_convert_{run_uuid}",
        "signature_mismatch": False,
        "_meta_gold_amount": gold_amount,
        "_meta_rate": 100,
    }
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(entry, f, indent=2, ensure_ascii=False)
    return path


def main():
    parser = argparse.ArgumentParser(
        description="T57 Gold → Token converter (100:1 anchored, daily cap)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--gold", type=int, required=True,
                        help="EOV 局內 Gold 數量（必須 >= 100）")
    parser.add_argument("--run-uuid", required=True,
                        help="局 ID / save UUID 作 idempotency key")
    parser.add_argument("--account", required=True,
                        help="目標帳戶 ID（通常是 Tim 或某 agent）")
    parser.add_argument("--description",
                        help="額外描述（可選）")
    parser.add_argument("--dry-run", action="store_true",
                        help="只計算不寫 ledger")
    args = parser.parse_args()

    rules = load_rules()
    gc_spec = rules.get("income_sources", {}).get("gold_conversion")
    if not gc_spec:
        print("❌ rules.json 缺 gold_conversion enum；請先註冊", file=sys.stderr)
        sys.exit(2)

    rate = gc_spec.get("rate_gold_to_token", 100)
    daily_cap = gc_spec.get("daily_cap_tokens", 10)

    # 驗證最低門檻
    if args.gold < rate:
        print(f"❌ Gold {args.gold} 低於最低門檻 {rate}（不足換 1 token）", file=sys.stderr)
        sys.exit(3)

    # 計算
    tokens = args.gold // rate
    leftover_gold = args.gold % rate

    # Idempotency
    if check_idempotency(args.run_uuid):
        print(f"❌ run_uuid={args.run_uuid} 已結算過 (idempotency fail)", file=sys.stderr)
        sys.exit(4)

    # Daily cap check
    cap_remaining = daily_cap_remaining(args.account, daily_cap)
    if tokens > cap_remaining:
        print(f"⚠ daily cap 觸發：{args.account} 今日已用 {daily_cap - cap_remaining}/{daily_cap} tokens",
              file=sys.stderr)
        print(f"   要轉 {tokens} 但只能 {cap_remaining} → cap 至 {cap_remaining}", file=sys.stderr)
        if cap_remaining == 0:
            print("❌ 今日上限已滿，明天再來", file=sys.stderr)
            sys.exit(5)
        tokens = cap_remaining

    desc = (args.description
            or f"Gold→Token conversion: {args.gold} gold @ {rate}:1 = {tokens} token (run={args.run_uuid})")

    print(f"# 🪙 Gold → Token Conversion")
    print(f"  account     : {args.account}")
    print(f"  gold input  : {args.gold}")
    print(f"  rate        : {rate}:1")
    print(f"  tokens out  : {tokens}")
    print(f"  leftover    : {leftover_gold} gold (未達 {rate} 不轉換)")
    print(f"  daily cap   : {daily_cap - cap_remaining + tokens}/{daily_cap}")
    print(f"  run_uuid    : {args.run_uuid}")

    if args.dry_run:
        print("\n  ✅ DRY RUN — 不寫入 ledger")
        return

    path = write_ledger_entry(args.account, tokens, args.gold,
                              args.run_uuid, desc)
    fire_broadcast(path)   # T64: 補 T41 broadcast (filesystem 直寫 path)
    print(f"\n  ✅ Wrote: {path}")
    print(f"  💰 {args.account} +{tokens} tavern_token (gold_conversion)")
    print(f"  📡 Discord broadcast fired (太平洋標準銀行 channel)")


if __name__ == "__main__":
    main()
