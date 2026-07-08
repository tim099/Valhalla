#!/usr/bin/env python3
"""treasury_commit_credit.py — T41+ 規則：每次 git commit 自動 credit 1 token.

Usage:
    # commit 後手動跑（agent 自律）
    python AgentCommands/PromptQueue/treasury_commit_credit.py --account claude-da-xiaojie

    # auto-detect account from git config user.email （未來 commit hook 用）
    python AgentCommands/PromptQueue/treasury_commit_credit.py --auto

    # 指定不同 amount（特殊情況）
    python AgentCommands/PromptQueue/treasury_commit_credit.py --account X --amount 1

行為：
1. 讀最新 commit sha (git log -1 --format='%H %s')
2. spawn run_cmd.py op=credit account=<id> amount=1 source_kind=commit source_ref=<sha8>
3. WriteEntry 結尾自動 fire Discord broadcast（既有 T41 機制）
4. fail swallow + log warning（不擋 git workflow）

注意：
- 本 script 不自動 hook 進 git post-commit — agent / Tim 自律呼叫
- 未來可走 install_skills.py 裝 git post-commit hook 自動化（v2 backlog）
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent.parent
# T-PATH-02: run_cmd.py 走 layout-agnostic resolver, 不再寫死 CardGame/Assets/UCL/UCL_Core
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
from AgentCommands._lib import tavern_paths as _tp  # noqa: E402
_RUN_CMD = _tp.RUN_CMD_PATH

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def _git(args: list[str]) -> str:
    """Run `git args` in repo root, return stdout."""
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=_REPO_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"[treasury_commit_credit] git fail: {e}", file=sys.stderr)
        return ""


def detect_account_from_git() -> str:
    """Auto-detect agent_id from git config user.email / user.name."""
    email = _git(["config", "user.email"]).lower()
    name = _git(["config", "user.name"]).lower()

    # 簡單啟發式：email / name 含 claude / antigravity / gemini
    for blob in (email, name):
        if "claude" in blob: return "claude-da-xiaojie"
        if "antigravity" in blob: return "antigravity-da-xiaojie"
        if "gemini" in blob: return "gemini-da-xiaojie"
    # 預設 claude（Tim 主帳號）
    return "claude-da-xiaojie"


def get_latest_commit() -> tuple[str, str]:
    """Return (sha_short, subject)."""
    sha_short = _git(["log", "-1", "--format=%h"])
    subject = _git(["log", "-1", "--format=%s"])
    return sha_short, subject


def credit_for_commit(account: str, amount: int = 1) -> int:
    if not _RUN_CMD.is_file():
        print(f"[treasury_commit_credit] run_cmd.py not found: {_RUN_CMD}", file=sys.stderr)
        return 1

    sha_short, subject = get_latest_commit()
    if not sha_short:
        print("[treasury_commit_credit] no commit found (git log fail)", file=sys.stderr)
        return 1

    # 截斷 subject 避免太長
    desc = subject[:120] if subject else "(no message)"

    cmd = [
        sys.executable, str(_RUN_CMD), "run", "Treasury",
        "--arg", "op=credit",
        "--arg", f"account={account}",
        "--arg", f"amount={amount}",
        "--arg", "source_kind=commit",
        "--arg", f"source_ref={sha_short}",
        "--arg", f"description={desc}",
        "--arg", f"caller={account}",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180)
        if result.returncode == 0:
            print(f"[treasury_commit_credit] +{amount} → {account} for commit {sha_short} ({desc[:60]}...)")
            return 0
        else:
            print(f"[treasury_commit_credit] cmd fail rc={result.returncode}: {result.stderr.strip()[:200]}", file=sys.stderr)
            return 2
    except Exception as e:
        print(f"[treasury_commit_credit] spawn fail: {e}", file=sys.stderr)
        return 3


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--account", help="Agent account ID (e.g. claude-da-xiaojie)")
    parser.add_argument("--auto", action="store_true", help="Auto-detect from git config")
    parser.add_argument("--amount", type=int, default=1, help="Token amount (default 1 per Tim 拍板)")
    args = parser.parse_args(argv)

    if not args.account and not args.auto:
        parser.error("must specify --account <id> or --auto")

    account = args.account or detect_account_from_git()
    return credit_for_commit(account, args.amount)


if __name__ == "__main__":
    sys.exit(main())
