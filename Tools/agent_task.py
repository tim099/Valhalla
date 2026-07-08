#!/usr/bin/env python3
"""
T60 agent_task.py — Reverse task system: Agent → Tim 提案，Tim Y/N 接受

職責：補完雙向 task economy。
物理意義：v1 只有 Tim → agent 單向；T60 加 agent → Tim 反向 channel。
        Tim 接受時立即 transfer (per Tim 原話「完成交易」)；
        Tim 無法達成時 refund 反向 transfer (per Tim 原話「儘量退回款項」)。

子命令:
  propose  <description> --amount N [--deadline X] [--from <agent_id>]
                                 agent 提案 task 給 Tim (預設 from=claude-da-xiaojie)
  list     [--status proposed|accepted|declined|refunded|all]
                                 列所有 proposals (預設 proposed)
  show     <task_id>             詳細看單一 proposal
  accept   <task_id>             Tim 說 Y → 預付 transfer
  decline  <task_id>             Tim 說 N → 不付款
  refund   <task_id> [--reason]  Tim 無法達成 → 退款
  withdraw <task_id> [--from <agent_id>]
                                 agent 主動撤回 (Tim 還沒 Y/N 才行)

範例:
  python agent_task.py propose "請開 Editor 讓我 compile-check Op_Transfer" --amount 3
  python agent_task.py list
  python agent_task.py accept t60_a1b2c3
  python agent_task.py refund t60_a1b2c3 --reason "Editor 開不起來"

State 存放:
  AgentCommands/AgentTasks/proposals.jsonl     — append-only audit log
  AgentCommands/AgentTasks/_active.json        — current state index (rebuild from jsonl)
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

# Windows utf-8 fix
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass


PROPOSALS_PATH = "AgentCommands/AgentTasks/proposals.jsonl"
ACTIVE_PATH = "AgentCommands/AgentTasks/_active.json"
LEDGER_ROOT = "AgentCommands/Treasury/ledger"
TIM = "Tim"
DEFAULT_AGENT = "claude-da-xiaojie"

# 規則參數
MIN_PAYMENT = 1
MAX_PAYMENT = 50
DAILY_CAP_PER_AGENT = 5


def utcnow_iso():
    n = datetime.datetime.utcnow()
    return n.strftime("%Y-%m-%dT%H:%M:%S.") + f"{n.microsecond//1000:03d}Z"


def gen_task_id():
    return "t60_" + secrets.token_hex(4)


def append_jsonl(path, entry):
    """區塊職責：append 一筆 audit log entry"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def load_jsonl(path):
    """區塊職責：讀整份 jsonl"""
    if not os.path.exists(path):
        return []
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return entries


def rebuild_active(entries):
    """
    區塊職責：從 jsonl 重建 active state index
    物理意義：last-write-wins per task_id；entries[0]=propose，後面 transitions 累加
    T60 v2 — propose 帶 auto_paid=True → 初始 state=paid_pending；v1 沒帶 → state=proposed
    """
    active = {}
    for e in entries:
        tid = e.get("task_id")
        if not tid:
            continue
        action = e.get("action", "")
        if action == "propose":
            # v2 auto_paid → paid_pending；v1 legacy → proposed
            initial_state = "paid_pending" if e.get("auto_paid") else "proposed"
            active[tid] = {
                "task_id": tid,
                "ts_proposed": e.get("ts"),
                "from": e.get("from"),
                "to": e.get("to", TIM),
                "amount": e.get("amount", 0),
                "description": e.get("description", ""),
                "deadline": e.get("deadline"),
                "version": e.get("version", "v1"),
                "auto_paid": e.get("auto_paid", False),
                "pre_payment": e.get("pre_payment"),
                "state": initial_state,
                "history": [(e.get("ts"), "propose")],
            }
        elif tid in active:
            # T60 v2 — action 直接 set 為 state（completed / declined / accepted / refunded / withdrawn）
            active[tid]["state"] = action
            active[tid]["history"].append((e.get("ts"), action))
            if "reason" in e:
                active[tid]["reason"] = e["reason"]
            if e.get("_v2_revert"):
                active[tid]["v2_revert"] = e.get("revert")
    return active


def save_active(active):
    os.makedirs(os.path.dirname(ACTIVE_PATH), exist_ok=True)
    with open(ACTIVE_PATH, "w", encoding="utf-8") as f:
        json.dump(active, f, indent=2, ensure_ascii=False)


def write_ledger(account, amount, source_or_use_kind, source_ref, description,
                 entry_type="credit"):
    """區塊職責：filesystem 直寫 Treasury ledger entry"""
    now_utc = datetime.datetime.utcnow()
    ts_iso = now_utc.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now_utc.microsecond//1000:03d}Z"
    date_dir = now_utc.strftime("%Y-%m-%d")
    hhmmss = now_utc.strftime("%H%M%S")
    msec = f"{now_utc.microsecond//1000:03d}"
    short_uuid = secrets.token_hex(3)
    filename = f"{hhmmss}_{msec}_{short_uuid}__{entry_type}.json"
    path = f"{LEDGER_ROOT}/{date_dir}/{filename}"

    entry = {
        "ts": ts_iso,
        "uuid": short_uuid,
        "type": entry_type,
        "amount": amount,
        "currency": "tavern_token",
        "account_id": account,
        "source_kind": source_or_use_kind,
        "source_ref": source_ref,
        "source_description": description,
        "balance_before": None,
        "balance_after": None,
        "sig_agent_id_claimed": "system",
        "sig_process_id": str(os.getpid()),
        "sig_env_marker": "manual_filesystem_write_agent_task",
        "sig_cmd_id": f"agent_task_{source_ref}",
        "signature_mismatch": False,
    }
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(entry, f, indent=2, ensure_ascii=False)
    fire_broadcast(path)   # T64: Discord 太平洋標準銀行 broadcast
    return path


def get_balance(account):
    """區塊職責：scan ledger 算指定 account balance"""
    import glob
    total_c = 0
    total_d = 0
    for f in glob.glob(f"{LEDGER_ROOT}/*/*.json"):
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


def daily_proposal_count(agent):
    """區塊職責：算今日該 agent 的 proposal 次數（防 spam）"""
    today = datetime.date.today().strftime("%Y-%m-%d")
    entries = load_jsonl(PROPOSALS_PATH)
    n = 0
    for e in entries:
        if e.get("action") != "propose":
            continue
        if e.get("from") != agent:
            continue
        if (e.get("ts") or "")[:10] == today:
            n += 1
    return n


# ─────────────────────────── op handlers ───────────────────────────

def cmd_propose(args):
    """
    區塊職責：T60 v2 — propose 即時自動 auto-fire transfer (Tim 拍板)
    物理意義：v1 需 Tim 顯式 accept 才轉帳 → friction 高；
              v2 propose 立即 fire transfer (agent 端 debit + Tim 端 credit pair with shared tx_id)，
              state=paid_pending；Tim 後續可 accept (final) 或 decline (tx-targeted revert)。
    數值影響：寫 1 筆 proposal entry + 2 筆 ledger entry (debit+credit pair)
    安全：daily cap / balance check 仍 fire；Tim 端 revert 時 check Tim balance
    """
    if args.amount < MIN_PAYMENT or args.amount > MAX_PAYMENT:
        print(f"❌ amount must be {MIN_PAYMENT}-{MAX_PAYMENT}, got {args.amount}", file=sys.stderr)
        sys.exit(2)

    agent = args.from_agent
    # daily cap check
    n = daily_proposal_count(agent)
    if n >= DAILY_CAP_PER_AGENT:
        print(f"❌ {agent} 今日已達 daily cap {n}/{DAILY_CAP_PER_AGENT} 提案", file=sys.stderr)
        sys.exit(3)

    # balance check (agent 要付得起)
    bal = get_balance(agent)
    if bal < args.amount:
        print(f"❌ {agent} balance={bal} < amount={args.amount}，付不起", file=sys.stderr)
        sys.exit(4)

    tid = gen_task_id()
    ts = utcnow_iso()
    deadline = args.deadline or (datetime.datetime.utcnow() + datetime.timedelta(days=7)).strftime("%Y-%m-%d")

    # T60 v2 — auto-fire transfer 即時，paired ledger entries with shared cmd_id=tid
    debit_path = write_ledger(
        account=agent, amount=args.amount,
        source_or_use_kind="agent_proposal_offer",
        source_ref=tid,
        description=f"Auto pre-pay (v2 propose): {args.description[:80]}",
        entry_type="debit",
    )
    credit_path = write_ledger(
        account=TIM, amount=args.amount,
        source_or_use_kind="agent_proposal_payment",
        source_ref=tid,
        description=f"Auto pre-pay from {agent} (v2 propose): {args.description[:80]}",
        entry_type="credit",
    )
    debit_uuid = os.path.basename(debit_path).split("__")[0].split("_")[-1]
    credit_uuid = os.path.basename(credit_path).split("__")[0].split("_")[-1]

    # Proposal entry includes pre_payment metadata for tx-targeted revert
    entry = {
        "ts": ts,
        "task_id": tid,
        "action": "propose",
        "from": agent,
        "to": TIM,
        "amount": args.amount,
        "description": args.description,
        "deadline": deadline,
        "version": "v2",
        "auto_paid": True,
        "pre_payment": {
            "agent_debit_path": debit_path,
            "tim_credit_path": credit_path,
            "agent_debit_uuid": debit_uuid,
            "tim_credit_uuid": credit_uuid,
        },
    }
    append_jsonl(PROPOSALS_PATH, entry)

    # rebuild + save
    save_active(rebuild_active(load_jsonl(PROPOSALS_PATH)))

    print(f"# 📨 Proposal Created (v2 auto-paid)")
    print(f"  task_id      : {tid}")
    print(f"  from         : {agent}")
    print(f"  to           : {TIM}")
    print(f"  amount       : **{args.amount}** token (already transferred)")
    print(f"  deadline     : {deadline}")
    print(f"  description  : {args.description}")
    print(f"\n  💸 Transfer fired:")
    print(f"     {agent} balance: {bal} → {bal - args.amount}")
    print(f"     Tim balance: +{args.amount}")
    print(f"     debit  ledger: {debit_path}")
    print(f"     credit ledger: {credit_path}")
    print(f"\n  daily cap    : {n+1}/{DAILY_CAP_PER_AGENT}")
    print(f"\n👉 Tim 後續路徑:")
    print(f"   accept   t60_xxx  → 標 completed (no money move)")
    print(f"   decline  t60_xxx  → tx-targeted revert (退錢回去)")
    print(f"\n⚠ 提醒：money 已落到 Tim 帳戶。decline 時如 Tim balance < {args.amount} 會 fail")
    print(f"   (錢被花到別處)。Tim 自律不要先花預付款，或事後 self-grant 補回。")


def cmd_list(args):
    entries = load_jsonl(PROPOSALS_PATH)
    active = rebuild_active(entries)
    status_filter = args.status
    if status_filter == "all":
        proposals = list(active.values())
    elif status_filter == "open":
        # 未結算 = proposed (v1) + paid_pending (v2)
        proposals = [p for p in active.values()
                     if p["state"] in ("proposed", "paid_pending")]
    else:
        proposals = [p for p in active.values() if p["state"] == status_filter]
    proposals.sort(key=lambda p: p.get("ts_proposed", ""), reverse=True)

    if not proposals:
        print(f"⚠ 沒有 proposals 符合 status={status_filter}")
        return

    print(f"# 📋 Agent Task Proposals (status={status_filter}, {len(proposals)} 筆)\n")
    print(f"{'task_id':<14} {'state':<10} {'amount':>6}  {'from':<22}  description")
    print("─" * 100)
    for p in proposals:
        desc = p["description"][:50] + ("…" if len(p["description"]) > 50 else "")
        print(f"{p['task_id']:<14} {p['state']:<10} {p['amount']:>6}  {p['from']:<22}  {desc}")


def cmd_show(args):
    active = rebuild_active(load_jsonl(PROPOSALS_PATH))
    p = active.get(args.task_id)
    if not p:
        print(f"❌ task_id {args.task_id} not found", file=sys.stderr)
        sys.exit(2)

    print(f"# 📄 Proposal {p['task_id']}")
    print(f"  state        : **{p['state']}**")
    print(f"  from         : {p['from']}")
    print(f"  to           : {p['to']}")
    print(f"  amount       : {p['amount']} token")
    print(f"  description  : {p['description']}")
    print(f"  deadline     : {p.get('deadline', '?')}")
    print(f"  proposed at  : {p.get('ts_proposed', '?')}")
    if p.get("reason"):
        print(f"  reason       : {p['reason']}")
    print(f"\n  History:")
    for ts, action in p.get("history", []):
        print(f"    {ts}  {action}")


def _check_state(p, expected_states, action_label):
    if p["state"] not in expected_states:
        print(f"❌ task {p['task_id']} state={p['state']}，無法執行 {action_label} (expected {expected_states})",
              file=sys.stderr)
        sys.exit(5)


def cmd_accept(args):
    """
    T60 v2 accept = 標 completed final state，無 money move（v2 已在 propose 時 auto-paid）
    v1 fallback：若 state=proposed (legacy 沒 auto-paid)，fire transfer (舊行為兼容)
    """
    active = rebuild_active(load_jsonl(PROPOSALS_PATH))
    p = active.get(args.task_id)
    if not p:
        print(f"❌ task_id {args.task_id} not found", file=sys.stderr)
        sys.exit(2)
    _check_state(p, ["proposed", "paid_pending"], "accept")

    agent = p["from"]
    amount = p["amount"]
    ts = utcnow_iso()

    # 區分 v1 / v2 處理
    if p["state"] == "paid_pending":
        # v2 — 已 auto-paid，accept = 標 completed (no money move)
        entry = {
            "ts": ts,
            "task_id": p["task_id"],
            "action": "completed",
            "_note": "v2 accept = mark final; money already pre-paid at propose time",
        }
        append_jsonl(PROPOSALS_PATH, entry)
        save_active(rebuild_active(load_jsonl(PROPOSALS_PATH)))
        print(f"# ✅ Completed: {p['task_id']} (v2 — money already moved at propose)")
        print(f"  state: paid_pending → completed (final)")
        print(f"  Tim 帳戶已留 {amount} token (來自 {agent} 預付)")
        return

    # v1 legacy — fire transfer now (舊邏輯兼容)
    bal = get_balance(agent)
    if bal < amount:
        print(f"❌ {agent} balance dropped to {bal} < {amount}，無法 accept", file=sys.stderr)
        sys.exit(6)

    entry = {
        "ts": ts,
        "task_id": p["task_id"],
        "action": "accepted",
    }
    append_jsonl(PROPOSALS_PATH, entry)

    debit_path = write_ledger(
        account=agent, amount=amount,
        source_or_use_kind="agent_proposal_offer",
        source_ref=p["task_id"],
        description=f"Agent proposal accepted by Tim (v1 legacy): {p['description'][:80]}",
        entry_type="debit",
    )
    credit_path = write_ledger(
        account=TIM, amount=amount,
        source_or_use_kind="agent_proposal_payment",
        source_ref=p["task_id"],
        description=f"Pre-payment from {agent} (v1 legacy): {p['description'][:80]}",
        entry_type="credit",
    )
    save_active(rebuild_active(load_jsonl(PROPOSALS_PATH)))

    print(f"# ✅ Accepted (v1 legacy): {p['task_id']}")
    print(f"  transfer     : {agent} -{amount} → Tim +{amount}")
    print(f"  debit ledger : {debit_path}")
    print(f"  credit ledger: {credit_path}")


def cmd_decline(args):
    """
    T60 v2 decline = tx-targeted revert (Tim 拍板)
    物理意義：propose 已 auto-pay，decline 必須反向轉回；
              fungibility hazard 由 Tim balance check 守門 (Tim 不夠就 fail)
    v1 legacy：state=proposed 沒 auto-paid → 純關閉 (no money move)
    """
    active = rebuild_active(load_jsonl(PROPOSALS_PATH))
    p = active.get(args.task_id)
    if not p:
        print(f"❌ task_id {args.task_id} not found", file=sys.stderr)
        sys.exit(2)
    _check_state(p, ["proposed", "paid_pending"], "decline")

    agent = p["from"]
    amount = p["amount"]
    ts = utcnow_iso()

    if p["state"] == "proposed":
        # v1 legacy: no money was moved, just close
        entry = {
            "ts": ts,
            "task_id": p["task_id"],
            "action": "declined",
            "_note": "v1 legacy decline — no money was moved",
        }
        append_jsonl(PROPOSALS_PATH, entry)
        save_active(rebuild_active(load_jsonl(PROPOSALS_PATH)))
        print(f"# 🚫 Declined (v1 legacy): {p['task_id']}")
        print(f"  no transfer (proposal closed)")
        return

    # v2 paid_pending — fire reverse transfer (tx-targeted via source_ref linking)
    reason = args.reason or "(unspecified)"
    pre_pay = p.get("pre_payment", {})
    original_credit_uuid = pre_pay.get("tim_credit_uuid", "?")
    original_debit_uuid = pre_pay.get("agent_debit_uuid", "?")

    # Tim balance check — 不夠 fail (per Tim concern: 期間花掉就 revert 錯)
    tim_bal = get_balance(TIM)
    if tim_bal < amount:
        print(f"❌ Tim balance {tim_bal} < {amount}，revert 失敗", file=sys.stderr)
        print(f"   原因：propose 後 Tim balance 被消耗 (其他交易 / fee debit)", file=sys.stderr)
        print(f"   建議：", file=sys.stderr)
        print(f"     a) Tim self-grant 補回 {amount - tim_bal} token 後再 decline", file=sys.stderr)
        print(f"     b) 或 accept 留下 token 視為已完成 task", file=sys.stderr)
        print(f"   原 pre-payment uuids: agent_debit={original_debit_uuid} / tim_credit={original_credit_uuid}", file=sys.stderr)
        sys.exit(7)

    # tx-targeted revert: source_ref 內含原 task_id + 原 uuid pair 線索
    revert_ref = f"{p['task_id']}|revert_of:tim_credit_uuid={original_credit_uuid}"
    revert_desc_tim = f"v2 decline revert: {reason} (revert pre-payment {original_credit_uuid})"
    revert_desc_agent = f"v2 decline revert received: {reason} (revert paired with debit {original_debit_uuid})"

    tim_debit_path = write_ledger(
        account=TIM, amount=amount,
        source_or_use_kind="agent_proposal_refund",
        source_ref=revert_ref,
        description=revert_desc_tim,
        entry_type="debit",
    )
    agent_credit_path = write_ledger(
        account=agent, amount=amount,
        source_or_use_kind="agent_proposal_refund_received",
        source_ref=revert_ref,
        description=revert_desc_agent,
        entry_type="credit",
    )
    new_debit_uuid = os.path.basename(tim_debit_path).split("__")[0].split("_")[-1]
    new_credit_uuid = os.path.basename(agent_credit_path).split("__")[0].split("_")[-1]

    entry = {
        "ts": ts,
        "task_id": p["task_id"],
        "action": "declined",
        "reason": reason,
        "_v2_revert": True,
        "revert": {
            "tim_debit_path": tim_debit_path,
            "agent_credit_path": agent_credit_path,
            "tim_debit_uuid": new_debit_uuid,
            "agent_credit_uuid": new_credit_uuid,
            "reverts_credit_uuid": original_credit_uuid,
            "reverts_debit_uuid": original_debit_uuid,
        },
    }
    append_jsonl(PROPOSALS_PATH, entry)
    save_active(rebuild_active(load_jsonl(PROPOSALS_PATH)))

    print(f"# 🔄 Declined (v2 tx-targeted revert): {p['task_id']}")
    print(f"  reason         : {reason}")
    print(f"  reverse        : Tim -{amount} → {agent} +{amount}")
    print(f"  Tim debit      : {tim_debit_path} (uuid {new_debit_uuid})")
    print(f"  agent credit   : {agent_credit_path} (uuid {new_credit_uuid})")
    print(f"  reverts pair   : tim_credit={original_credit_uuid} / agent_debit={original_debit_uuid}")
    print(f"\n  Tim balance: → {tim_bal - amount}")
    print(f"  {agent} balance: → {get_balance(agent)}")


def cmd_refund(args):
    active = rebuild_active(load_jsonl(PROPOSALS_PATH))
    p = active.get(args.task_id)
    if not p:
        print(f"❌ task_id {args.task_id} not found", file=sys.stderr)
        sys.exit(2)
    _check_state(p, ["accepted"], "refund")

    agent = p["from"]
    amount = p["amount"]

    # Check Tim has balance to refund
    tim_bal = get_balance(TIM)
    if tim_bal < amount:
        print(f"❌ Tim balance {tim_bal} < {amount}，refund 失敗（Tim 已用掉）", file=sys.stderr)
        print(f"   建議 partial refund 或自行先 self-grant 補回", file=sys.stderr)
        sys.exit(7)

    ts = utcnow_iso()
    reason = args.reason or "(unspecified)"
    entry = {
        "ts": ts,
        "task_id": p["task_id"],
        "action": "refunded",
        "reason": reason,
    }
    append_jsonl(PROPOSALS_PATH, entry)

    debit_path = write_ledger(
        account=TIM, amount=amount,
        source_or_use_kind="agent_proposal_refund",
        source_ref=p["task_id"],
        description=f"Refund to {agent} (cant complete): {reason}",
        entry_type="debit",
    )
    credit_path = write_ledger(
        account=agent, amount=amount,
        source_or_use_kind="agent_proposal_refund_received",
        source_ref=p["task_id"],
        description=f"Refund received from Tim: {reason}",
        entry_type="credit",
    )
    save_active(rebuild_active(load_jsonl(PROPOSALS_PATH)))

    print(f"# 💸 Refunded: {p['task_id']}")
    print(f"  reason       : {reason}")
    print(f"  reverse      : Tim -{amount} → {agent} +{amount}")
    print(f"  Tim debit    : {debit_path}")
    print(f"  agent credit : {credit_path}")


def cmd_withdraw(args):
    active = rebuild_active(load_jsonl(PROPOSALS_PATH))
    p = active.get(args.task_id)
    if not p:
        print(f"❌ task_id {args.task_id} not found", file=sys.stderr)
        sys.exit(2)
    _check_state(p, ["proposed"], "withdraw")
    if p["from"] != args.from_agent:
        print(f"❌ {args.from_agent} 不是 task owner ({p['from']})", file=sys.stderr)
        sys.exit(8)

    ts = utcnow_iso()
    entry = {
        "ts": ts,
        "task_id": p["task_id"],
        "action": "withdrawn",
    }
    append_jsonl(PROPOSALS_PATH, entry)
    save_active(rebuild_active(load_jsonl(PROPOSALS_PATH)))
    print(f"# 🔙 Withdrawn: {p['task_id']} (no transfer fired)")


# ─────────────────────────── main ───────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="T60 Reverse task system — Agent → Tim 提案",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("propose", help="Agent 提案 task 給 Tim")
    p.add_argument("description", help="task 描述")
    p.add_argument("--amount", type=int, required=True, help=f"預付 token ({MIN_PAYMENT}-{MAX_PAYMENT})")
    p.add_argument("--deadline", help="YYYY-MM-DD (預設 7 天後)")
    p.add_argument("--from", dest="from_agent", default=DEFAULT_AGENT,
                   help=f"提案 agent_id (default {DEFAULT_AGENT})")
    p.set_defaults(func=cmd_propose)

    p = sub.add_parser("list", help="列 proposals")
    p.add_argument("--status",
                   choices=["proposed", "paid_pending", "completed", "accepted",
                            "declined", "refunded", "withdrawn", "open", "all"],
                   default="open",
                   help="filter (open=未結算的 v1 proposed + v2 paid_pending；all=含已結束)")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("show", help="看單一 proposal 詳細")
    p.add_argument("task_id")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("accept", help="Tim Y → 預付 transfer")
    p.add_argument("task_id")
    p.set_defaults(func=cmd_accept)

    p = sub.add_parser("decline", help="Tim N → 不付 (v1) / tx-targeted revert (v2)")
    p.add_argument("task_id")
    p.add_argument("--reason", help="退款原因 (v2 fires reverse transfer; reason 進 ledger description)")
    p.set_defaults(func=cmd_decline)

    p = sub.add_parser("refund", help="Tim 無法達成 → 退款")
    p.add_argument("task_id")
    p.add_argument("--reason", help="退款原因")
    p.set_defaults(func=cmd_refund)

    p = sub.add_parser("withdraw", help="agent 撤回（Tim 還沒 Y/N）")
    p.add_argument("task_id")
    p.add_argument("--from", dest="from_agent", default=DEFAULT_AGENT)
    p.set_defaults(func=cmd_withdraw)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
