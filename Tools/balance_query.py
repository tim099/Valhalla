#!/usr/bin/env python3
"""
balance_query.py — Treasury ledger balance 查詢工具

職責：
  讀 AgentCommands/Treasury/ledger/<YYYY-MM-DD>/*.json，
  算指定 account 的 (sum credit - sum debit) 真實餘額，
  並列最近 N 筆進出帳 (newest first)。

物理意義：
  Treasury ledger 是 source-of-truth (T41 後雙重保障 webhook 同步 Discord)。
  本工具供「酒保餘額查詢系統」(T68+) 雙路徑共用：
    - CMD path: agent 直接 run python balance_query.py
    - 對話 path: BartenderDaemon spawn 本腳本後將 stdout 貼回 tavern

數值影響：
  純讀檔，無 IO 副作用；不寫 ledger / 不 broadcast / 不 mutate state。

Usage:
  python balance_query.py --account claude-da-xiaojie
  python balance_query.py --account Tim --limit 5
  python balance_query.py --account Tim --format json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Path resolve — 本工具放在 AgentCommands/Tools/, repo root = parent.parent
# ---------------------------------------------------------------------------
_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent.parent
_LEDGER_ROOT = _REPO_ROOT / "AgentCommands" / "Treasury" / "ledger"

# stdout UTF-8 (Windows console fallback)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# ---------------------------------------------------------------------------
# Ledger scan
# ---------------------------------------------------------------------------
def _iter_ledger_entries():
    """
    區塊職責：yield 所有 ledger entry (parsed JSON dict, sorted by date 子資料夾 + 檔名)
    物理意義：ledger 結構 Treasury/ledger/<YYYY-MM-DD>/<HHMMSS_ms_xxx>__(credit|debit).json
              檔名 prefix 為 HHMMSS_ms 確保字典序 = 時間序
    """
    if not _LEDGER_ROOT.is_dir():
        return
    for date_dir in sorted(_LEDGER_ROOT.iterdir()):
        if not date_dir.is_dir():
            continue
        for entry_file in sorted(date_dir.iterdir()):
            if entry_file.suffix != ".json":
                continue
            try:
                yield json.loads(entry_file.read_text(encoding="utf-8")), entry_file.name, date_dir.name
            except (OSError, json.JSONDecodeError):
                continue


def compute_balance_and_history(account_id: str, currency: str = "tavern_token", limit: int = 10):
    """
    回 (balance, history_list)
      balance: int — sum(credit) - sum(debit)
      history_list: list of dict — 最近 N 筆 (newest first)，內容: {ts, type, amount, kind, ref, description, balance_after, uuid}
    """
    total_credit = 0
    total_debit = 0
    matched = []  # 累積後再 reverse + slice
    for entry, fname, date_str in _iter_ledger_entries():
        if entry.get("account_id") != account_id:
            continue
        if entry.get("currency", "tavern_token") != currency:
            continue
        etype = entry.get("type", "?")
        amount = entry.get("amount", 0)
        if etype == "credit":
            total_credit += amount
        elif etype == "debit":
            total_debit += amount
        matched.append({
            "ts": entry.get("ts") or f"{date_str} {fname[:6]}",
            "type": etype,
            "amount": amount,
            "kind": entry.get("source_kind", "?"),
            "ref": entry.get("source_ref", "") or "",
            "description": entry.get("source_description", "") or "",
            "balance_after": entry.get("balance_after"),
            "uuid": (entry.get("uuid") or "")[:8],
        })
    balance = total_credit - total_debit
    history = list(reversed(matched))[:limit]
    return balance, history, total_credit, total_debit, len(matched)


# ---------------------------------------------------------------------------
# Format
# ---------------------------------------------------------------------------
def format_markdown(account: str, balance: int, history: list, total_credit: int, total_debit: int, total_entries: int, limit: int) -> str:
    """區塊職責：產生 markdown 報表 (給酒保 post 用)"""
    lines = []
    lines.append(f"💰 **{account} 帳戶餘額**: `{balance}` tavern_token")
    lines.append(f"📊 累計: +{total_credit} / -{total_debit} (共 {total_entries} 筆 ledger entry)")
    lines.append("")
    if not history:
        lines.append("_(無進出帳記錄)_")
        return "\n".join(lines)
    lines.append(f"**最近 {min(limit, len(history))} 筆進出帳** (newest first):")
    for h in history:
        sign = "↑+" if h["type"] == "credit" else ("↓-" if h["type"] == "debit" else "?")
        ts_disp = h["ts"][:19] if h["ts"] else "?"
        ba_disp = f" → 餘額 {h['balance_after']}" if h["balance_after"] is not None else ""
        desc_disp = f" — {h['description']}" if h["description"] else ""
        ref_disp = f" [ref: `{h['ref']}`]" if h["ref"] else ""
        lines.append(f"- `{ts_disp}` {sign}{h['amount']} `{h['kind']}`{ba_disp}{desc_disp}{ref_disp}")
    return "\n".join(lines)


def format_json(account: str, balance: int, history: list, total_credit: int, total_debit: int, total_entries: int) -> str:
    """區塊職責：機器可讀 JSON (給其他工具 chain)"""
    return json.dumps({
        "account": account,
        "balance": balance,
        "total_credit": total_credit,
        "total_debit": total_debit,
        "total_entries": total_entries,
        "history": history,
    }, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--account", required=True, help="Account ID (e.g. claude-da-xiaojie / Tim)")
    parser.add_argument("--currency", default="tavern_token", help="Currency filter (default: tavern_token)")
    parser.add_argument("--limit", type=int, default=10, help="近期進出帳筆數 (default: 10)")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Output format")
    args = parser.parse_args(argv)

    if args.limit < 0 or args.limit > 100:
        print("[balance_query] --limit must be 0..100", file=sys.stderr)
        return 2

    balance, history, total_c, total_d, total_n = compute_balance_and_history(
        args.account, currency=args.currency, limit=args.limit
    )

    if args.format == "json":
        print(format_json(args.account, balance, history, total_c, total_d, total_n))
    else:
        print(format_markdown(args.account, balance, history, total_c, total_d, total_n, args.limit))
    return 0


if __name__ == "__main__":
    sys.exit(main())
