#!/usr/bin/env python3
"""
T61 treasury_revert.py — Generic ad-hoc Treasury 交易 revert tool

職責：Tim 想 revert 任何特定 ledger entry / source_ref / tx_id 時用本工具。
物理意義：跟 agent_task v2 的 tx-targeted decline 概念相同，但泛化到任何交易：
        agent_task 限定 proposal 流程；treasury_revert 任何 ledger entry 都能 undo。

子命令:
  recent [--limit N] [--account X]    印最近 N 筆 ledger entries (找想 revert 的)
  show <uuid>                         看單筆 entry 詳細
  by-ref <source_ref>                 找某 source_ref 的 entries (e.g. tx_id)
  uuid <uuid> [--reason "..."]        revert 單筆 entry by uuid
  ref <source_ref> [--reason "..."]   revert 整組 paired entries by source_ref
  pair <debit_uuid> <credit_uuid> [--reason "..."]
                                      revert 顯式 paired entries (atomic two-side)

範例:
  # 列最近 10 筆，找想 revert 的
  python treasury_revert.py recent --limit 10

  # 看單筆
  python treasury_revert.py show 80dc1c

  # 用 source_ref 找 paired entries (常見 e.g. transfer 的 tx_id)
  python treasury_revert.py by-ref t60_fe41ac77

  # revert 單筆 (auto 偵測 type 反向)
  python treasury_revert.py uuid 80dc1c --reason "錯帳補正"

  # revert 整組 paired entries by source_ref (一次反向兩邊)
  python treasury_revert.py ref t60_fe41ac77 --reason "double-fire 修正"

行為規則:
  - 原 entry type=credit → 反向 fire debit (帳戶被收回)
  - 原 entry type=debit  → 反向 fire credit (帳戶被退回)
  - 反向 entry source_kind="tx_revert"，source_ref 標明 "revert_of:<原 uuid>"
  - balance feasibility check: 反向 debit 時對方 balance 不夠則 fail
  - idempotency: 同一 uuid 不能 revert 兩次 (scan 既有 tx_revert entries 防重複)

⚠ 用 sparingly — 大量 revert 會破壞 ledger 直觀性。常見用法：
  - 修正錯帳 (amount 寫錯)
  - 撤銷誤觸發 cmd
  - agent_task v2 decline 跑 revert 失敗時手動補正
  - migration 修舊 schema entries
"""

import argparse
import datetime
import glob
import json
import os
import secrets
import sys

# T64: 補 T41 跨 path broadcast 缺口
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _lib.treasury_broadcast import fire_broadcast  # noqa: E402

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass


LEDGER_ROOT = "AgentCommands/Treasury/ledger"


def utcnow_iso():
    n = datetime.datetime.utcnow()
    return n.strftime("%Y-%m-%dT%H:%M:%S.") + f"{n.microsecond//1000:03d}Z"


def scan_all_entries():
    """區塊職責：載所有 ledger entries (sorted by ts)"""
    entries = []
    for f in sorted(glob.glob(f"{LEDGER_ROOT}/*/*.json")):
        try:
            with open(f, "r", encoding="utf-8") as fp:
                e = json.load(fp)
            e["_path"] = f
            entries.append(e)
        except (OSError, json.JSONDecodeError):
            continue
    entries.sort(key=lambda e: e.get("ts", ""))
    return entries


def find_by_uuid(uuid_short):
    """區塊職責：找 entry by uuid 短碼"""
    for e in scan_all_entries():
        if e.get("uuid") == uuid_short:
            return e
    return None


def find_by_source_ref(source_ref):
    """區塊職責：找所有 source_ref 包含某字串的 entries"""
    matches = []
    for e in scan_all_entries():
        ref = e.get("source_ref", "") or ""
        if source_ref in ref:
            matches.append(e)
    return matches


def is_already_reverted(target_uuid):
    """
    區塊職責：檢查 target_uuid 是否已被任何工具 revert
    物理意義：scan 所有 entries 找含 "revert_of" 且 source_ref 含 target_uuid 的
            涵蓋: tx_revert (本工具) / agent_proposal_refund (agent_task v2) / 任何反向 entry
    """
    for e in scan_all_entries():
        ref = e.get("source_ref", "") or ""
        # 寬鬆檢測：source_ref 必須含 "revert" 關鍵字 + 目標 uuid
        if "revert" in ref.lower() and target_uuid in ref:
            return True
    return False


def get_balance(account):
    """算 account 當前 tavern_token balance"""
    total_c = 0
    total_d = 0
    for e in scan_all_entries():
        if e.get("account_id") != account:
            continue
        if e.get("currency", "tavern_token") != "tavern_token":
            continue
        if e.get("type") == "credit":
            total_c += e.get("amount", 0)
        else:
            total_d += e.get("amount", 0)
    return total_c - total_d


def write_revert_entry(target_entry, reason):
    """
    區塊職責：fire 反向 entry
    物理意義：原 credit X → 反向 debit X；原 debit X → 反向 credit X
    回傳：新 entry path / new uuid
    """
    target_type = target_entry.get("type")
    target_amount = target_entry.get("amount", 0)
    target_account = target_entry.get("account_id")
    target_uuid = target_entry.get("uuid")
    target_currency = target_entry.get("currency", "tavern_token")

    # 反向：credit → debit / debit → credit
    new_type = "debit" if target_type == "credit" else "credit"

    # balance check: 反向 debit (從帳戶收回) 時要 balance 夠
    if new_type == "debit":
        bal = get_balance(target_account)
        if bal < target_amount:
            print(f"❌ {target_account} balance={bal} < amount={target_amount}，revert 失敗",
                  file=sys.stderr)
            print(f"   原 entry uuid={target_uuid} 為 credit；revert 需從 {target_account} 收回 {target_amount}",
                  file=sys.stderr)
            print(f"   建議：{target_account} self-grant 補回 {target_amount - bal} 後再試",
                  file=sys.stderr)
            sys.exit(7)

    now_utc = datetime.datetime.utcnow()
    ts_iso = now_utc.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now_utc.microsecond//1000:03d}Z"
    date_dir = now_utc.strftime("%Y-%m-%d")
    hhmmss = now_utc.strftime("%H%M%S")
    msec = f"{now_utc.microsecond//1000:03d}"
    short_uuid = secrets.token_hex(3)
    filename = f"{hhmmss}_{msec}_{short_uuid}__{new_type}.json"
    path = f"{LEDGER_ROOT}/{date_dir}/{filename}"

    desc = f"tx_revert: revert_of:{target_uuid} (originally {target_type} {target_amount} {target_currency} for {target_account}). Reason: {reason}"

    entry = {
        "ts": ts_iso,
        "uuid": short_uuid,
        "type": new_type,
        "amount": target_amount,
        "currency": target_currency,
        "account_id": target_account,
        "source_kind": "tx_revert",
        "source_ref": f"revert_of:{target_uuid}",
        "source_description": desc,
        "balance_before": None,
        "balance_after": None,
        "sig_agent_id_claimed": "system",
        "sig_process_id": str(os.getpid()),
        "sig_env_marker": "manual_filesystem_write_treasury_revert",
        "sig_cmd_id": f"treasury_revert_{target_uuid}",
        "signature_mismatch": False,
        "_revert_target": {
            "uuid": target_uuid,
            "type": target_type,
            "amount": target_amount,
            "account": target_account,
            "original_source_kind": target_entry.get("source_kind") or target_entry.get("use_kind"),
        },
    }
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(entry, f, indent=2, ensure_ascii=False)
    fire_broadcast(path)   # T64: Discord 太平洋標準銀行 broadcast
    return path, short_uuid


# ─────────────────────────── op handlers ───────────────────────────

def cmd_recent(args):
    entries = scan_all_entries()
    if args.account:
        entries = [e for e in entries if e.get("account_id") == args.account]
    entries = entries[-args.limit:]
    print(f"# 📒 Recent ledger entries (last {len(entries)}{', account=' + args.account if args.account else ''})\n")
    print(f"{'ts':<20} {'type':<7} {'amt':>5} {'account':<22} {'kind':<28} uuid")
    print("─" * 110)
    for e in entries:
        ts = (e.get("ts") or "")[:19]
        tp = e.get("type", "?")
        amt = e.get("amount", 0)
        acct = e.get("account_id", "?")[:22]
        kind = e.get("source_kind") or e.get("use_kind") or "?"
        kind = kind[:28]
        uid = e.get("uuid", "?")
        print(f"{ts:<20} {tp:<7} {amt:>5} {acct:<22} {kind:<28} {uid}")


def cmd_show(args):
    e = find_by_uuid(args.uuid)
    if not e:
        print(f"❌ uuid {args.uuid} not found", file=sys.stderr)
        sys.exit(2)
    print(json.dumps(e, indent=2, ensure_ascii=False))


def cmd_by_ref(args):
    matches = find_by_source_ref(args.source_ref)
    if not matches:
        print(f"⚠ 找不到 source_ref 含 '{args.source_ref}' 的 entries")
        return
    print(f"# 🔍 Entries matching source_ref ~ '{args.source_ref}' ({len(matches)} 筆)\n")
    print(f"{'ts':<20} {'type':<7} {'amt':>5} {'account':<22} {'kind':<28} uuid")
    print("─" * 110)
    for e in matches:
        ts = (e.get("ts") or "")[:19]
        tp = e.get("type", "?")
        amt = e.get("amount", 0)
        acct = e.get("account_id", "?")[:22]
        kind = (e.get("source_kind") or e.get("use_kind") or "?")[:28]
        uid = e.get("uuid", "?")
        print(f"{ts:<20} {tp:<7} {amt:>5} {acct:<22} {kind:<28} {uid}")


def cmd_uuid(args):
    """Revert single entry by uuid"""
    target = find_by_uuid(args.uuid)
    if not target:
        print(f"❌ uuid {args.uuid} not found", file=sys.stderr)
        sys.exit(2)

    if is_already_reverted(args.uuid):
        print(f"⚠ uuid {args.uuid} 已被 revert 過 (idempotency check)", file=sys.stderr)
        sys.exit(3)

    if target.get("source_kind") == "tx_revert":
        print(f"⚠ uuid {args.uuid} 本身就是 tx_revert entry，不該再 revert (會無限套娃)", file=sys.stderr)
        sys.exit(4)

    reason = args.reason or "(unspecified)"
    path, new_uuid = write_revert_entry(target, reason)

    print(f"# 🔄 Reverted single entry: {args.uuid}")
    print(f"  reason       : {reason}")
    print(f"  original     : {target.get('type')} {target.get('amount')} {target.get('currency', 'tavern_token')} for {target.get('account_id')}")
    print(f"  reverse fire : {('debit' if target.get('type') == 'credit' else 'credit')} {target.get('amount')}")
    print(f"  new entry    : {path} (uuid {new_uuid})")
    print(f"\n  {target.get('account_id')} balance: → {get_balance(target.get('account_id'))}")


def cmd_ref(args):
    """Revert all entries matching source_ref (e.g. paired transfer tx)"""
    matches = find_by_source_ref(args.source_ref)
    if not matches:
        print(f"❌ 找不到 source_ref 含 '{args.source_ref}' 的 entries", file=sys.stderr)
        sys.exit(2)

    # Filter out already-reverted + tx_revert entries themselves
    targets = [e for e in matches
               if e.get("source_kind") != "tx_revert"
               and not is_already_reverted(e.get("uuid"))]

    if not targets:
        print(f"⚠ 所有 entries 都已 revert 過或 entries 本身是 tx_revert，沒可 revert 的", file=sys.stderr)
        sys.exit(3)

    reason = args.reason or "(unspecified)"
    print(f"# 🔄 Reverting {len(targets)} entries matching ref '{args.source_ref}'\n")

    paths = []
    for target in targets:
        try:
            path, new_uuid = write_revert_entry(target, reason)
            paths.append((target, path, new_uuid))
            print(f"  ✅ uuid {target.get('uuid')} ({target.get('type')} {target.get('amount')} for {target.get('account_id')}) → revert {new_uuid}")
        except SystemExit:
            print(f"  ❌ uuid {target.get('uuid')} revert FAIL — balance check", file=sys.stderr)
            raise

    print(f"\n# Summary")
    accounts = set(t[0].get("account_id") for t in paths)
    for acct in accounts:
        print(f"  {acct} balance: → {get_balance(acct)}")


def cmd_pair(args):
    """Revert explicit paired entries (debit + credit)"""
    debit = find_by_uuid(args.debit_uuid)
    credit = find_by_uuid(args.credit_uuid)
    if not debit or not credit:
        print(f"❌ 找不到 debit_uuid={args.debit_uuid} 或 credit_uuid={args.credit_uuid}", file=sys.stderr)
        sys.exit(2)
    if debit.get("type") != "debit":
        print(f"❌ {args.debit_uuid} type={debit.get('type')} != debit", file=sys.stderr)
        sys.exit(3)
    if credit.get("type") != "credit":
        print(f"❌ {args.credit_uuid} type={credit.get('type')} != credit", file=sys.stderr)
        sys.exit(4)
    if debit.get("amount") != credit.get("amount"):
        print(f"❌ amount mismatch: debit={debit.get('amount')} != credit={credit.get('amount')}", file=sys.stderr)
        sys.exit(5)

    reason = args.reason or "(unspecified)"
    print(f"# 🔄 Reverting pair: debit {args.debit_uuid} + credit {args.credit_uuid}\n")
    for entry in (debit, credit):
        path, new_uuid = write_revert_entry(entry, reason)
        print(f"  ✅ uuid {entry.get('uuid')} ({entry.get('type')} {entry.get('amount')} for {entry.get('account_id')}) → revert {new_uuid}")


def main():
    parser = argparse.ArgumentParser(
        description="T61 generic Treasury revert tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("recent", help="印最近 N 筆 ledger entries")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--account")
    p.set_defaults(func=cmd_recent)

    p = sub.add_parser("show", help="看單筆 entry 詳細")
    p.add_argument("uuid")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("by-ref", help="找 source_ref 含某字串的 entries")
    p.add_argument("source_ref")
    p.set_defaults(func=cmd_by_ref)

    p = sub.add_parser("uuid", help="Revert 單筆 by uuid")
    p.add_argument("uuid")
    p.add_argument("--reason")
    p.set_defaults(func=cmd_uuid)

    p = sub.add_parser("ref", help="Revert 整組 paired entries by source_ref")
    p.add_argument("source_ref")
    p.add_argument("--reason")
    p.set_defaults(func=cmd_ref)

    p = sub.add_parser("pair", help="Revert 顯式 paired (debit + credit)")
    p.add_argument("debit_uuid")
    p.add_argument("credit_uuid")
    p.add_argument("--reason")
    p.set_defaults(func=cmd_pair)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
