#!/usr/bin/env python3
"""persona_character_clone.py — T03 (Persona_Character_Workflow)

從既有 RCG_CharacterData 模板 clone 一個 persona 對應的同名 character。
依 docs/Workflows/Persona_Character_Workflow.md §2 鐵律:
  允許改: ID / m_MaxHp / m_Name / m_CharacterIntro (4 個)
  強制設: m_Unlock.UnlockType = "None"
  其他 fields 一筆不漏 clone 模板。

Usage:
  python persona_character_clone.py \
    --persona trailhead \
    --template Mia \
    --hp-multiplier 2 \
    --intro "山徑起點，gemini-2.5-pro layer 0 base。" \
    [--reason "wake#4 layer 0 base, 對齊山徑 framing"] \
    [--dry-run]

Outputs:
  CardGame/Assets/.BuiltinModules/ModulesRoot/Modules/Persona/UCL_Assets/RCG_CharacterData/<persona>.json

T07.6 trailhead (2026-05-16) — skeleton; production batch run 留 T05。
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

# ─── Paths ────────────────────────────────────────────────────────────────
_REPO_ROOT = Path(__file__).resolve().parents[2]
# T-PATH-02: .BuiltinModules 走 layout-agnostic resolver, 不再寫死 CardGame/Assets/.BuiltinModules
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
from AgentCommands._lib import tavern_paths as _tp  # noqa: E402
_BUILTIN_ROOT = _tp.BUILTIN_MODULES_DIR / "ModulesRoot" / "Modules"
_TEMPLATE_CANDIDATE_DIRS = [
    _BUILTIN_ROOT / "Core/UCL_Assets/RCG_CharacterData",
    _BUILTIN_ROOT / "Fate/UCL_Assets/RCG_CharacterData",
]
_OUTPUT_DIR = _BUILTIN_ROOT / "Persona/UCL_Assets/RCG_CharacterData"

# ─── Persona ID validation ────────────────────────────────────────────────
# Persona_Character_Workflow §7 — persona 含 dash + 數字 (basecamp-fork-... / crest-001)
# UCL_Asset ID 端慣例是 PascalCase 但實測未驗證限制。先 sanitize 警告, 不擋。
_ALLOWED_ID_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")


def find_template(template_id: str) -> Path:
    """Find <template>.json across BuiltinModules Core/Fate dirs."""
    for d in _TEMPLATE_CANDIDATE_DIRS:
        p = d / f"{template_id}.json"
        if p.exists():
            return p
    raise FileNotFoundError(f"template '{template_id}' not found in {_TEMPLATE_CANDIDATE_DIRS}")


def validate_persona_id(pid: str) -> list[str]:
    """Return list of warnings (empty = OK). Hard reject illegal chars only."""
    warnings = []
    if not pid:
        raise ValueError("persona id 不能空")
    illegal = [c for c in pid if c not in _ALLOWED_ID_CHARS]
    if illegal:
        raise ValueError(f"persona id '{pid}' 含非法字元: {illegal}")
    if "-" in pid or any(c.isdigit() for c in pid):
        warnings.append(f"persona id '{pid}' 含 dash / 數字 — 對齊 persona_registry 但偏離 RCG PascalCase 慣例 (per workflow §7 已知地雷, 走 T03 驗 ID 合法性)")
    return warnings


def clone_character(persona: str, template_id: str, hp_multiplier: float,
                    intro: str, reason: str | None = None, dry_run: bool = False) -> Path:
    """Perform the clone op. Returns output path (or would-be path if dry_run)."""
    # 1. Validate id
    warnings = validate_persona_id(persona)
    for w in warnings:
        print(f"⚠ {w}", file=sys.stderr)

    # 2. Validate hp multiplier range [2, 5] per workflow §2
    if not (2 <= hp_multiplier <= 5):
        raise ValueError(f"hp_multiplier {hp_multiplier} 超出 [2, 5] 範圍 (workflow §2 鐵律)")

    # 3. Load template
    template_path = find_template(template_id)
    print(f"📖 template: {template_path.relative_to(_REPO_ROOT)}")
    with open(template_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 4. Mutate the 4 allowed fields
    original_hp = int(data["UnitData"]["MaxHp"])
    new_hp = int(round(original_hp * hp_multiplier))

    data["ID"] = persona
    data["UnitData"]["MaxHp"] = new_hp
    # Name + Intro 走 inline LocalizeType="Direct" 不走 LocalizeKey (避免 collision)
    display_name = f"{persona} 大小姐"
    data["UnitData"]["Name"] = {
        "LocalizeType": "Direct",
        "DirectText": display_name,
    }
    data["UnitData"]["CharacterIntro"] = {
        "LocalizeType": "Direct",
        "DirectText": intro,
    }

    # 5. Unlock 處理 — 繼承模板的 Unlock pointer
    #    (T05 dogfood 撞坑: 原本想 force inline UnlockType=None, 但 m_Unlock 是 RCG_UnlockEntry
    #     reference asset 不是 inline UnlockSetting, 多寫 "UnlockType":"None" 會撞 JsonConvert.Enum.Parse,
    #     退回繼承模板。意味著 persona character 跟模板共享 unlock 條件, 若模板是 Default_Tutorial
    #     persona 也算 Tutorial — workflow doc §2 該收一筆 patch。DevMenu 顯式列入仍待 T06。)

    # 6. Write
    _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    # audit trail 走 sidecar md (不入 JSON 避免 deserializer 撞 extra field)
    audit_md = _OUTPUT_DIR / f"{persona}.audit.md"
    audit_md.write_text(
        f"# Persona Clone Audit — {persona}\n\n"
        f"- template: `{template_id}`\n"
        f"- template_original_hp: {original_hp}\n"
        f"- hp_multiplier: {hp_multiplier}\n"
        f"- hp_reason: {reason or '(no reason recorded)'}\n"
        f"- generated_by: persona_character_clone.py T03\n"
        f"- workflow_doc: docs/Workflows/Persona_Character_Workflow.md\n",
        encoding='utf-8'
    )
    out_path = _OUTPUT_DIR / f"{persona}.json"

    if dry_run:
        print(f"🔍 [dry-run] would write: {out_path.relative_to(_REPO_ROOT)}")
        print(f"   HP: {original_hp} × {hp_multiplier} = {new_hp}")
        return out_path

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent="\t")
    print(f"✅ wrote: {out_path.relative_to(_REPO_ROOT)}")
    print(f"   HP: {original_hp} × {hp_multiplier} = {new_hp}")
    print(f"   reason: {reason or '(none)'}")
    return out_path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--persona", required=True, help="persona codename, 對齊 awakening pool")
    ap.add_argument("--template", required=True, help="既有 RCG_CharacterData ID, e.g. Mia / Lucia / Aigis")
    ap.add_argument("--hp-multiplier", type=float, required=True, help="模板 HP × N, N ∈ [2, 5]")
    ap.add_argument("--intro", required=True, help="角色一句自介 (m_CharacterIntro)")
    ap.add_argument("--reason", default=None, help="HP 倍數理由 (主管審核用 audit, 寫入 _PersonaCloneAudit)")
    ap.add_argument("--dry-run", action="store_true", help="只印不寫")
    args = ap.parse_args()
    try:
        clone_character(args.persona, args.template, args.hp_multiplier,
                        args.intro, args.reason, args.dry_run)
    except Exception as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
