#!/usr/bin/env python3
"""
migrate_voucher_v1_to_v2.py — 酒館券 schema v1 → v2 migration

⚠️ DEPRECATED / ONE-SHOT COMPLETE (2026-05-13 已執行完畢)。保留作歷史/文件參考，
   **請勿重跑**（會重複 init 每 persona 的 voucher = 二次通膨）。下方 AGENT_TO_BANK 是
   遷移當時的殘留硬編表、**非 live SOT**、已 stale（缺 gemini/Luna）——agent→bank 的
   唯一真相在 _lib/bank_resolver.py + AwakenInit/_registry_meta.json（Bank 整合 2026-07-21
   收攏；本表僅供讀懂當年遷移邏輯，勿當成可信的 agent→bank 對照）。

依據: Q11 Tim 2026-05-13 拍板規則
  > 每 persona 初始化 = 該 actor 帳戶當前 voucher total
  > broadcast 不 split (eg. actor 36 → 每 persona 36)
  > 通膨可接受 (一次性 migration)

物理意義:
  - v1 schema: agents.<bank_account>.{total_remaining, history}
  - v2 schema: agents.<bank_account>.personas.<persona>.{total_remaining, history}
                + agents.<bank_account>._legacy_no_persona.{history, total_remaining}

Persona resolution:
  - persona_registry.json 的 agent 欄位 = 'claude-code' / 'antigravity' / 'Zeta'
  - 對應 bank_account:
    - claude-code → claude-da-xiaojie
    - antigravity → antigravity-da-xiaojie
    - Zeta → (無 bank account, 跳過)

Usage:
  python migrate_voucher_v1_to_v2.py [--dry-run]
"""

from __future__ import annotations
import argparse
import json
import shutil
import sys
from pathlib import Path
from collections import defaultdict

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent.parent

_QUOTA_PATH = _REPO_ROOT / "AgentCommands" / "ChatTavern" / "agent_bonus_quota.json"
_PERSONAS_DIR = _REPO_ROOT / "AgentCommands" / "AwakenInit" / "personas"

# ⚠️ DEAD 一次性遷移殘留 (2026-05-13)，非 live SOT、已 stale (缺 gemini/Luna)。
# agent→bank 真相見 _lib/bank_resolver.py + _registry_meta.json。勿新增/信任本表。
AGENT_TO_BANK = {
    "claude-code": "claude-da-xiaojie",
    "antigravity": "antigravity-da-xiaojie",
    "Zeta": None,  # no bank account entry in quota.json
}


def load_personas_by_bank() -> dict[str, list[str]]:
    """Return: bank_account → [persona names]"""
    result = defaultdict(list)
    for f in sorted(_PERSONAS_DIR.iterdir()):
        if not f.name.endswith(".json") or f.name.startswith("_"):
            continue
        try:
            p = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"⚠ skip {f.name}: {e}", file=sys.stderr)
            continue
        persona_name = f.stem
        agent = p.get("agent", "")
        bank = AGENT_TO_BANK.get(agent)
        if bank is None:
            continue
        result[bank].append(persona_name)
    return dict(result)


def migrate(dry_run: bool = False) -> dict:
    """Returns migration report dict."""
    if not _QUOTA_PATH.exists():
        raise FileNotFoundError(f"quota.json not found at {_QUOTA_PATH}")

    # Step 1: load current
    with open(_QUOTA_PATH, "r", encoding="utf-8") as f:
        v1 = json.load(f)
    assert v1.get("_schema_version", 1) == 1, "Expected _schema_version=1, found different"

    # Step 2: build new v2 schema (preserve top-level metadata)
    v2 = dict(v1)  # shallow copy top-level keys
    v2["_schema_version"] = 2
    v2["_migration_note"] = (
        "Migrated from v1 (per-actor) to v2 (per-actor × per-persona) on 2026-05-13. "
        "Rule: 每 persona 初始化 = actor 當前 total_remaining (broadcast, 不切分). "
        "Original v1 schema 備份於 agent_bonus_quota.v1.bak.json. Source ref: Q11 Tim 拍板."
    )

    # persona pool by bank
    personas_by_bank = load_personas_by_bank()
    report = {
        "personas_by_bank": personas_by_bank,
        "per_actor_changes": {},
    }

    # Step 3: rewrite agents section
    new_agents = {}
    for bank, agent_data in v1.get("agents", {}).items():
        old_total = agent_data.get("total_remaining", 0)
        old_history = agent_data.get("history", [])
        personas = personas_by_bank.get(bank, [])

        if not personas:
            # No personas found for this bank — keep as-is but wrap under _legacy_no_persona
            new_agents[bank] = {
                "personas": {},
                "_legacy_no_persona": {
                    "total_remaining": old_total,
                    "history": old_history,
                    "_note": "No persona registry entries matched this bank; v1 entries preserved here as fallback. Manual review recommended.",
                },
            }
            report["per_actor_changes"][bank] = {
                "old_total": old_total,
                "personas": [],
                "new_per_persona_total": 0,
                "new_supply_sum": old_total,  # only legacy bucket
                "note": "no_personas_for_bank",
            }
            continue

        personas_block = {}
        for p in personas:
            personas_block[p] = {
                "total_remaining": old_total,  # broadcast rule
                "history": [],  # empty per-persona history (legacy stays in _legacy_no_persona)
                "_init_at": "2026-05-13T08:00:00Z",  # migration timestamp
                "_init_reason": f"v1→v2 migration broadcast: actor had {old_total} → persona init {old_total}",
            }

        new_agents[bank] = {
            "personas": personas_block,
            "_legacy_no_persona": {
                "total_remaining": 0,  # already broadcasted to personas, legacy bucket now empty for balance purposes
                "history": old_history,  # keep for audit
                "_note": "Original v1 history preserved for audit. Total credit has been broadcasted to all personas; this bucket is balance-empty.",
            },
        }
        report["per_actor_changes"][bank] = {
            "old_total": old_total,
            "personas": personas,
            "new_per_persona_total": old_total,
            "new_supply_sum": old_total * len(personas),
            "inflation_factor": f"{len(personas)}x" if old_total > 0 else "0x (zero base)",
        }

    v2["agents"] = new_agents

    # Step 4: write (unless dry-run)
    if dry_run:
        print("--- DRY RUN: not writing ---")
        return report

    # Backup v1
    backup_path = _QUOTA_PATH.with_suffix(".v1.bak.json")
    shutil.copy2(_QUOTA_PATH, backup_path)
    print(f"✓ v1 backup → {backup_path.name}")

    # Write v2
    with open(_QUOTA_PATH, "w", encoding="utf-8") as f:
        json.dump(v2, f, ensure_ascii=False, indent=2)
    print(f"✓ v2 written → {_QUOTA_PATH.name}")

    return report


def print_report(report: dict) -> None:
    print()
    print("=" * 60)
    print("Migration Report")
    print("=" * 60)
    print()
    print("Personas by bank:")
    for bank, ps in report["personas_by_bank"].items():
        print(f"  {bank}: {len(ps)} personas → {ps}")
    print()
    print("Per-actor migration:")
    total_old, total_new = 0, 0
    for bank, info in report["per_actor_changes"].items():
        n_personas = len(info["personas"])
        print(f"  {bank}:")
        print(f"    old_total: {info['old_total']}")
        print(f"    personas ({n_personas}): {info['personas']}")
        print(f"    new per-persona: {info['new_per_persona_total']}")
        print(f"    new supply sum: {info['new_supply_sum']} ({info.get('inflation_factor', '')})")
        total_old += info["old_total"]
        total_new += info["new_supply_sum"]
    print()
    print(f"Total supply: {total_old} → {total_new} ({'inflation' if total_new > total_old else 'no-change'})")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--dry-run", action="store_true", help="Compute migration but don't write files")
    args = parser.parse_args(argv)

    print(f"📂 quota path: {_QUOTA_PATH}")
    print(f"📂 personas dir: {_PERSONAS_DIR}")
    print()

    report = migrate(dry_run=args.dry_run)
    print_report(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
