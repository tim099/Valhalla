---
asset_type: EffectPresetAsset
asset_id: NewFx1
verdict: SchemaDiff
generated: 2026-09-02T14:04:19
original_path: Assets/.BuiltinModules/ModulesRoot/Modules/Core/UCL_Assets/EffectPresetAsset/NewFx1.json
fixed_path: AgentCommands/asset_format_check_EffectPresetAsset_NewFx1.fixed.json
field_diff:
  removed: 1  # original 有，loader 不認識（被丟棄）
  added: 7  # loader 補了預設（原檔可能漏寫）
captured_error_count: 0
reference_check: Skipped
---

# Asset Format Validation: `EffectPresetAsset` / `NewFx1`

**Verdict**: `SchemaDiff`

Canonical forms differ — there is at least one schema-level difference (added / removed field, or changed value). See diff below.

## Files

- Original (read-only): [`Assets/.BuiltinModules/ModulesRoot/Modules/Core/UCL_Assets/EffectPresetAsset/NewFx1.json`](../Assets/.BuiltinModules/ModulesRoot/Modules/Core/UCL_Assets/EffectPresetAsset/NewFx1.json)
- Roundtrip output (loader's view): [`AgentCommands/asset_format_check_EffectPresetAsset_NewFx1.fixed.json`](../AgentCommands/asset_format_check_EffectPresetAsset_NewFx1.fixed.json)

## Recommended Action

⚠️ **Schema differences detected** — the loader's view differs from the source file.

Common causes:

- `removed` lines (in original, not in roundtrip) → loader did **not recognise** the field. Likely a typo or stale schema. Fix the field name in source.
- `added` lines (in roundtrip, not in original) → loader **filled in defaults**. Likely a missing required field in source. Add it explicitly to ensure intentional values.
- value changes → enum / type conversion failed and fell back to default. Check enum spelling, numeric type, null vs empty string.

Inspect the diff below and `AgentCommands/asset_format_check_EffectPresetAsset_NewFx1.fixed.json` to decide which values are correct, then patch the original. If you trust the loader fully, you may overwrite original with `AgentCommands/asset_format_check_EffectPresetAsset_NewFx1.fixed.json` — but be aware that unrecognised fields will be permanently lost.

## Canonical Diff

Unified diff between **canonicalized original** (left, `-`) and **canonicalized roundtrip** (right, `+`). Both forms have keys deep-sorted and 4-space indent so only schema differences remain.

```diff
--- original (canonical)
+++ roundtrip (canonical)
@@ -1,9 +1,15 @@
 {
 	"AliveTime":2,
+	"ClearTrackDelay":2,
 	"ClickCD":0.20000000298023224,
+	"ClimaxIterateAll":"False",
+	"ClimaxProbability":60,
+	"DisplayCountClimax":3,
+	"DisplayCountLV1":1,
+	"DisplayCountLV2":2,
+	"DisplayCountLV3":2,
 	"ExcludeLast":"True",
-	"MaxAlive":1,
 	"Probability":50,
 	"SameForAllLevels":"False",
 	"StaggerCD":0.10000000149011612
 }

```

