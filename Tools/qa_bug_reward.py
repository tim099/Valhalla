#!/usr/bin/env python3
"""
T68 qa_bug_reward.py — Tim QA 工作確認 bug 獎勵 CLI (Tim 08:34 拍板)

職責：當 Tim 完成 QA 工作確認真 bug 時，agent 拍板 grant reward token 給 Tim。
物理意義：勞動所得 — system mint，不從 agent 帳戶扣（gift pattern, like 招待券 / hp_overflow）。
        agent 自由意志決定是否真 bug vs feature request / spec 誤解。

子命令:
  grant --severity {trivial|normal|critical|catastrophic} --description "..." [--bug-ref X]
                                          給 Tim mint reward (agent 拍板用)
  list [--limit N]                         列今日 grant 過的 reward (audit)
  severity-table                           印 severity tier 對照 + 範例

範例:
  # 確認真 bug + grant normal severity (3 token)
  python qa_bug_reward.py grant --severity normal \
    --description "T67 Discord 餘額顯示 None → None" \
    --bug-ref "T67"

  # 嚴重 bug
  python qa_bug_reward.py grant --severity critical \
    --description "Treasury cmd race condition 導致 ledger 寫雙重 entry" \
    --bug-ref "T75"

  # 看今天 grant 過的
  python qa_bug_reward.py list

⚠ 重要:
  - 由 agent 拍板使用，不是 Tim 自己跑 (Tim 跑 = mint farm)
  - 每筆 grant 進 ledger + 廣播至 Discord 太平洋標準銀行
  - severity 對應額度 per rules.json income_sources.qa_bug_confirmed._severity_tiers
"""

import argparse
import datetime
import glob
import json
import os
import secrets
import sys

# Windows utf-8 fix
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

# T64: 補 T41 跨 path broadcast 缺口
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _lib.treasury_broadcast import fire_broadcast  # noqa: E402


LEDGER_ROOT = "AgentCommands/Treasury/ledger"
RULES_PATH = "AgentCommands/Treasury/rules.json"
TIM = "Tim"

# 同 rules.json income_sources.qa_bug_confirmed._severity_tiers
SEVERITY_TIERS = {
    "trivial": 1,
    "normal": 3,
    "critical": 5,
    "catastrophic": 10,
}

SEVERITY_EXAMPLES = {
    "trivial": "typo / cosmetic / minor display issue / 內部 path bug",
    "normal": "functional issue / UX bug / ledger 錯漏 / broadcast 失敗",
    "critical": "data loss / security / crash / 跨 session 影響",
    "catastrophic": "major economic state corruption / repo-wide breakage",
}


def utcnow_iso():
    n = datetime.datetime.utcnow()
    return n.strftime("%Y-%m-%dT%H:%M:%S.") + f"{n.microsecond//1000:03d}Z"


def write_reward_ledger(amount: int, severity: str, description: str,
                        bug_ref: str = "", account_id: str = TIM) -> str:
    """區塊職責：filesystem 直寫 qa_bug_confirmed credit
    參數 account_id (T+ 2026-05-12): 預設 Tim, 可指定其他 actor (e.g. Zeta agent 觀察報 bug)
    語意: Tim 顯式指令時可 grant 給其他 actor (覆寫 skill 預設「不互相 grant」規則)
    """
    now_utc = datetime.datetime.utcnow()
    ts_iso = utcnow_iso()
    date_dir = now_utc.strftime("%Y-%m-%d")
    hhmmss = now_utc.strftime("%H%M%S")
    msec = f"{now_utc.microsecond//1000:03d}"
    short_uuid = secrets.token_hex(3)
    filename = f"{hhmmss}_{msec}_{short_uuid}__credit.json"
    path = f"{LEDGER_ROOT}/{date_dir}/{filename}"

    full_desc = f"QA bug reward [{severity}] to {account_id}: {description}"
    if bug_ref:
        full_desc += f" (ref: {bug_ref})"

    entry = {
        "ts": ts_iso,
        "uuid": short_uuid,
        "type": "credit",
        "amount": amount,
        "currency": "tavern_token",
        "account_id": account_id,
        "source_kind": "qa_bug_confirmed",
        "source_ref": bug_ref or f"qa-bug-{short_uuid}",
        "source_description": full_desc,
        "balance_before": None,
        "balance_after": None,
        "sig_agent_id_claimed": "system",
        "sig_process_id": str(os.getpid()),
        "sig_env_marker": "manual_filesystem_write_qa_bug_reward",
        "sig_cmd_id": f"qa_bug_reward_{short_uuid}",
        "signature_mismatch": False,
        "_severity": severity,
    }
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(entry, f, indent=2, ensure_ascii=False)
    return path


# ─────────────────────────── op handlers ───────────────────────────

def cmd_grant(args):
    severity = args.severity.lower()
    if severity not in SEVERITY_TIERS:
        print(f"❌ unknown severity: {severity}; use {list(SEVERITY_TIERS.keys())}",
              file=sys.stderr)
        sys.exit(2)

    amount = SEVERITY_TIERS[severity]
    desc = args.description
    bug_ref = args.bug_ref or ""
    account = getattr(args, "account", None) or TIM

    if not desc:
        print("❌ --description required", file=sys.stderr)
        sys.exit(3)

    path = write_reward_ledger(amount, severity, desc, bug_ref, account_id=account)
    fire_broadcast(path)   # T64 helper → Discord 太平洋標準銀行

    print(f"# 🏅 QA Bug Reward Granted")
    print(f"  Account     : {account} +{amount} tavern_token")
    print(f"  severity    : **{severity}** ({SEVERITY_TIERS[severity]} token)")
    print(f"  description : {desc}")
    if bug_ref:
        print(f"  bug_ref     : {bug_ref}")
    print(f"  ledger      : {path}")
    print(f"  📡 Discord broadcast fired (太平洋標準銀行 channel)")


def cmd_list(args):
    today = datetime.date.today().strftime("%Y-%m-%d")
    today_path = f"{LEDGER_ROOT}/{today}"
    if not os.path.isdir(today_path):
        print(f"⚠ 今日無 ledger 目錄 ({today})")
        return

    rewards = []
    for fname in sorted(os.listdir(today_path)):
        if not fname.endswith(".json"):
            continue
        try:
            with open(os.path.join(today_path, fname), "r", encoding="utf-8") as f:
                e = json.load(f)
        except (OSError, json.JSONDecodeError):
            continue
        if e.get("source_kind") != "qa_bug_confirmed":
            continue
        rewards.append(e)

    rewards.sort(key=lambda e: e.get("ts", ""), reverse=True)
    if args.limit > 0:
        rewards = rewards[:args.limit]

    if not rewards:
        print(f"⚠ 今日無 qa_bug_confirmed 獎勵")
        return

    total = sum(e.get("amount", 0) for e in rewards)
    print(f"# 🏅 QA Bug Rewards Today ({today}) — {len(rewards)} 筆 / 共 {total} token\n")
    print(f"{'ts':<20} {'sev':<14} {'amt':>4}  ref / description")
    print("─" * 90)
    for e in rewards:
        ts = (e.get("ts") or "")[:19]
        sev = e.get("_severity", "?")[:14]
        amt = e.get("amount", 0)
        ref = e.get("source_ref", "")[:18]
        desc = (e.get("source_description") or "")[:50]
        print(f"{ts:<20} {sev:<14} {amt:>4}  {ref} | {desc}")


def cmd_severity_table(args):
    print("# QA Bug Severity Tiers (T68)\n")
    print(f"{'severity':<14} {'amount':>7}  範例")
    print("─" * 80)
    for sev, amt in SEVERITY_TIERS.items():
        ex = SEVERITY_EXAMPLES.get(sev, "")
        print(f"{sev:<14} {amt:>7}  {ex}")
    print()
    print("Agent 自由意志判定原則:")
    print("  ✅ 確認真 bug (code 不符 spec / 預期外行為 / 影響 audit/UX/data)")
    print("  ✅ 可重現 (清楚 repro steps)")
    print("  ✅ 非重複既有 bug")
    print("  ❌ Feature request / improvement (非 bug)")
    print("  ❌ Spec 誤解 (Tim 沒讀 docs / 規則理解錯)")
    print("  ❌ Phase B 已知未實作 (不算 bug 算 backlog)")


def main():
    parser = argparse.ArgumentParser(
        description="T68 Tim QA bug confirmed reward CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("grant", help="Agent 拍板 grant reward 給 Tim")
    p.add_argument("--severity", required=True,
                   choices=list(SEVERITY_TIERS.keys()),
                   help=f"嚴重度 ({list(SEVERITY_TIERS.keys())})")
    p.add_argument("--description", required=True, help="bug 描述")
    p.add_argument("--bug-ref", default="", help="bug 參考 (e.g. T67 / commit hash)")
    p.add_argument("--account", default=TIM,
                   help=f"受 grant 帳戶 (預設 {TIM}; Tim 顯式指令可指定其他 actor e.g. zeta-da-xiaojie)")
    p.set_defaults(func=cmd_grant)

    p = sub.add_parser("list", help="列今日 grant 過的 rewards")
    p.add_argument("--limit", type=int, default=20, help="筆數上限")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("severity-table", help="印 severity tier 對照 + 範例")
    p.set_defaults(func=cmd_severity_table)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
