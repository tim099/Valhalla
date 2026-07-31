#!/usr/bin/env python3
"""treasury_broadcast.py — 主專案 shim → 委派 UCL_Core canonical treasury_ledger (2026-06-06 summit).

# 區塊職責：保留既有 public API (fire_broadcast / _backfill_balance_fields / _compute_balance_from_history),
#          但實作委派給 UCL_Core <Tools~/AgentCommands/_lib/treasury_ledger.py> — 單一真相, 避免兩份邏輯 drift。
# 物理意義：Tim 2026-06-06 拍板「treasury 餘額/廣播功能移進 UCL_Core 當跨專案 canonical」。
#          原 T64/T67 在主專案的等價實作 (compute balance + backfill null + spawn notify) 已上移 UCL_Core;
#          本檔降為 shim，供主專案的 Treasury caller（qa_bug_reward / agent_task / gold_convert 等）共用。
#          import 路徑不變、零改動繼續可用。
# 數值影響：happy path 全走 UCL_Core; UCL_Core 不可達時走本檔 inline fallback (防 regression, 不靜默掉廣播)。

歷史: T64 補 Python filesystem fallback 直寫 ledger 也要 Discord 廣播; T67 補 null balance 回填;
     2026-06-06 root cause 收斂 — UCL_Core fire_salary_credit 原裸 spawn 繞過 backfill 致薪資卡 None→None,
     一併把邏輯上移 UCL_Core 統一。
"""

import glob
import importlib.util as _ilu
import json
import os
import subprocess
import sys
from pathlib import Path


# ===========================================================
# 載入 UCL_Core canonical treasury_ledger (by file path, 避開 package import 問題)
# 物理意義: 主專案在 repo root; UCL_Core lib 在 CardGame/Assets/UCL/UCL_Core/Tools~/AgentCommands/_lib/。
#          treasury_broadcast.py 在 <repo>/AgentCommands/_lib/ → repo_root = parents[2]。
# ===========================================================
def _load_ucl_treasury_ledger():
    try:
        # T-PATH-02: 走 tavern_paths layout-agnostic resolver, 不再寫死 CardGame/Assets/UCL/UCL_Core。
        from . import tavern_paths as _tp
        canonical = _tp.UCL_LIB_DIR / "treasury_ledger.py"
        if not canonical.exists():
            return None
        spec = _ilu.spec_from_file_location("_ucl_treasury_ledger", canonical)
        mod = _ilu.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except Exception:
        return None


_UCL = _load_ucl_treasury_ledger()


# ===========================================================
# Public API — 委派 UCL_Core; 失敗則 inline fallback
# ===========================================================
def fire_broadcast(entry_path: str | Path, *, quiet: bool = True) -> None:
    """先補 null balance, 再 fire-and-forget spawn notify_treasury.py。委派 UCL_Core。"""
    if _UCL is not None:
        _UCL.fire_broadcast(entry_path, quiet=quiet)
        return
    _fallback_fire_broadcast(entry_path, quiet=quiet)


def _backfill_balance_fields(entry_path: str | Path) -> bool:
    """null balance 回填 (back-compat 名稱)。委派 UCL_Core。"""
    if _UCL is not None:
        return _UCL.backfill_balance_fields(entry_path)
    return _fallback_backfill(entry_path)


def _compute_balance_from_history(account_id: str, currency: str,
                                  exclude_uuid: str | None = None) -> int:
    """重放算餘額 (back-compat 名稱)。委派 UCL_Core (ledger_root 從主專案推)。"""
    ledger_root = Path(__file__).resolve().parents[1] / "Treasury" / "ledger"
    if _UCL is not None:
        return _UCL.compute_balance(ledger_root, account_id, currency, exclude_uuid=exclude_uuid)
    return _fallback_compute(ledger_root, account_id, currency, exclude_uuid)


# ===========================================================
# Inline fallback (僅 UCL_Core 不可達時用; 邏輯與 UCL_Core 版等價, 防 regression)
# ===========================================================
def _fallback_compute(ledger_root, account_id, currency, exclude_uuid=None) -> int:
    ledger_root = Path(ledger_root)
    if not ledger_root.exists():
        return 0
    total = 0
    for fpath in glob.glob(str(ledger_root / "*" / "*.json")):
        try:
            with open(fpath, "r", encoding="utf-8") as fp:
                e = json.load(fp)
        except (OSError, json.JSONDecodeError):
            continue
        if e.get("account_id") != account_id or e.get("currency", "tavern_token") != currency:
            continue
        if exclude_uuid and e.get("uuid") == exclude_uuid:
            continue
        amt = e.get("amount", 0)
        total += amt if e.get("type") == "credit" else -amt
    return total


def _fallback_backfill(entry_path) -> bool:
    entry_path = Path(entry_path)
    try:
        with open(entry_path, "r", encoding="utf-8") as f:
            e = json.load(f)
    except (OSError, json.JSONDecodeError):
        return False
    if e.get("balance_before") is not None and e.get("balance_after") is not None:
        return False
    account = e.get("account_id"); entry_type = e.get("type")
    if not account or entry_type not in ("credit", "debit"):
        return False
    currency = e.get("currency", "tavern_token"); amount = e.get("amount", 0)
    ledger_root = entry_path.resolve().parents[1]
    bb = _fallback_compute(ledger_root, account, currency, e.get("uuid"))
    e["balance_before"] = bb
    e["balance_after"] = bb + amount if entry_type == "credit" else bb - amount
    try:
        tmp = entry_path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(e, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, entry_path)
        return True
    except OSError:
        return False


def _fallback_fire_broadcast(entry_path, *, quiet=True) -> None:
    entry_path = Path(entry_path)
    if not entry_path.exists():
        return
    try:
        _fallback_backfill(entry_path)
    except Exception:
        pass
    script_path = Path(__file__).resolve().parents[1] / "PromptQueue" / "notify_treasury.py"
    if not script_path.exists():
        return
    cmd = [sys.executable, str(script_path), "--entry-file", str(entry_path)]
    if quiet:
        cmd.append("--quiet")
    try:
        subprocess.Popen(cmd,
                         stdout=subprocess.DEVNULL if quiet else None,
                         stderr=subprocess.DEVNULL if quiet else None)
    except Exception:
        pass


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="treasury broadcast shim (delegates to UCL_Core)")
    p.add_argument("entry_path")
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()
    fire_broadcast(args.entry_path, quiet=not args.verbose)
    print(f"Fired broadcast for {args.entry_path} (via {'UCL_Core' if _UCL else 'inline fallback'})")
