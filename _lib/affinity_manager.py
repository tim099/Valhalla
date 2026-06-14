"""
Affinity Manager — multi-dim hidden emotion vector per (persona, target).

Schema v2 (2026-05-12 redesign by basecamp 大小姐 per Tim 拍板):
- 每 persona 一個資料夾 `AgentCommands/ChatTavern/affinity/<persona>/relations.json`
- 每筆關係用 8 軸隱藏 emotion_vector + 表面 surface_score / tier / opinions / history
- 取代舊 v1 single-file `affinity_registry.json`（auto-migrate on load）

8 emotion axes (each in [-1.0, 1.0]):
    trust       — 信任 ↔ 不信任
    affection   — 親密 ↔ 疏離
    respect     — 敬重 ↔ 輕視
    interest    — 在意 ↔ 漠不關心
    irritation  — 惱怒 ↔ 心平 (正值 = 累積煩躁)
    dependence  — 依賴 ↔ 獨立
    admiration  — 欣賞 ↔ 嫉妒
    loyalty     — 忠誠 ↔ 背叛傾向

設計參考 persona_registry.json `identity_vector` (64-dim)，schema 與 range 一致。
"""

import datetime
import json
import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from . import tavern_paths as _tp

# ──────────────────────────── 常數 ────────────────────────────

# 區塊職責：定義 8 軸情感維度 + 對應 surface_score 加權
# 物理意義：emotion_vector 是 hidden state，UI / API 暴露的 surface_score 由加權和算出
# 數值影響：weights 修改會直接影響所有歷史 record 的 surface_score 重算
EMOTION_AXES: Tuple[str, ...] = (
    "trust", "affection", "respect", "interest",
    "irritation", "dependence", "admiration", "loyalty",
)

EMOTION_WEIGHTS: Dict[str, float] = {
    "trust": 2.0,
    "affection": 2.0,
    "respect": 1.5,
    "interest": 1.0,
    "irritation": -2.0,   # 負權重：越煩躁總分越低
    "dependence": 0.5,
    "admiration": 1.0,
    "loyalty": 1.5,
}

VECTOR_RANGE: Tuple[float, float] = (-1.0, 1.0)
SURFACE_RANGE: Tuple[int, int] = (-100, 100)
SCHEMA_VERSION = 2

# 路徑
AFFINITY_DIR: Path = _tp.TAVERN_DIR / "affinity"
LEGACY_REGISTRY_PATH: Path = _tp.TAVERN_DIR / "affinity_registry.json"


# ──────────────────────────── helpers ────────────────────────────

def utcnow_iso() -> str:
    """ISO 8601 ms-precision UTC timestamp (per tavern convention)"""
    n = datetime.datetime.utcnow()
    return n.strftime("%Y-%m-%dT%H:%M:%S.") + f"{n.microsecond // 1000:03d}Z"


def _clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def get_tier(surface_score: int) -> str:
    """Map surface_score → 5-tier tag (跟舊版 v1 維持相容)"""
    if surface_score >= 51:
        return "信任"
    if surface_score >= 11:
        return "在意"
    if surface_score >= -9:
        return "普通"
    if surface_score >= -49:
        return "冷淡"
    return "厭惡"


def compute_surface_score(emotion_vector: Dict[str, float]) -> int:
    """
    區塊職責：將 8 軸隱藏向量壓回 [-100, 100] 一維 surface_score
    物理意義：UI / 老 API 仍想要單一分數時用；不可逆 (resolution loss)
    數值影響：受 EMOTION_WEIGHTS 影響；修改 weights 將改寫所有 record 的顯示分數
    """
    total = 0.0
    weight_sum_abs = 0.0
    for axis, w in EMOTION_WEIGHTS.items():
        v = emotion_vector.get(axis, 0.0)
        total += v * w
        weight_sum_abs += abs(w)
    if weight_sum_abs <= 0:
        return 0
    normalized = total / weight_sum_abs
    return int(round(_clamp(normalized * 100, SURFACE_RANGE[0], SURFACE_RANGE[1])))


def default_emotion_vector() -> Dict[str, float]:
    """全 0 起始（中性 — 對 target 還沒形成感情）"""
    return {axis: 0.0 for axis in EMOTION_AXES}


def vector_to_list(emotion_vector: Dict[str, float]) -> List[float]:
    """Dict → list (對齊 EMOTION_AXES 順序) — 給 JSON 寫檔 / C# 反序列化用"""
    return [float(emotion_vector.get(axis, 0.0)) for axis in EMOTION_AXES]


def list_to_vector(values: List[float]) -> Dict[str, float]:
    """list → Dict (照 EMOTION_AXES 順序映射回 axes)"""
    out = default_emotion_vector()
    for i, axis in enumerate(EMOTION_AXES):
        if i < len(values):
            try:
                out[axis] = float(values[i])
            except (TypeError, ValueError):
                pass
    return out


# ──────────────────────────── persona file I/O ────────────────────────────

def _persona_dir(persona: str) -> Path:
    return AFFINITY_DIR / persona


def _relations_path(persona: str) -> Path:
    return _persona_dir(persona) / "relations.json"


def _empty_persona_doc(persona: str) -> dict:
    """空 persona doc — schema v2 base shell"""
    return {
        "_schema_version": SCHEMA_VERSION,
        "persona": persona,
        "_emotion_axes": list(EMOTION_AXES),
        "_emotion_weights": dict(EMOTION_WEIGHTS),
        "_vector_range": list(VECTOR_RANGE),
        "targets": {},
    }


def load_persona(persona: str) -> dict:
    """讀某 persona 的 relations.json；不存在回空 shell（不寫檔）"""
    # 先確保 migration 跑過（first-load auto-migrate）
    _maybe_migrate_legacy()

    p = _relations_path(persona)
    if not p.exists():
        return _empty_persona_doc(persona)
    try:
        with p.open("r", encoding="utf-8") as f:
            doc = json.load(f)
    except Exception:
        return _empty_persona_doc(persona)
    # 補欄位（schema 漂移防護）
    doc.setdefault("_schema_version", SCHEMA_VERSION)
    doc.setdefault("persona", persona)
    doc.setdefault("_emotion_axes", list(EMOTION_AXES))
    doc.setdefault("_emotion_weights", dict(EMOTION_WEIGHTS))
    doc.setdefault("_vector_range", list(VECTOR_RANGE))
    doc.setdefault("targets", {})
    return doc


def save_persona(persona: str, doc: dict) -> None:
    """atomic write — tmp file → replace"""
    p = _relations_path(persona)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
    tmp.replace(p)


def list_personas() -> List[str]:
    """掃 affinity/ 子資料夾抓所有有 relations.json 的 persona"""
    _maybe_migrate_legacy()
    if not AFFINITY_DIR.exists():
        return []
    out = []
    for child in sorted(AFFINITY_DIR.iterdir()):
        if child.is_dir() and (child / "relations.json").exists():
            out.append(child.name)
    return out


# ──────────────────────────── target / record management ────────────────────────────

def _ensure_target(doc: dict, target: str) -> dict:
    """確保 doc.targets[target] 存在；回 record 引用"""
    targets = doc.setdefault("targets", {})
    if target not in targets:
        vec = default_emotion_vector()
        targets[target] = {
            "emotion_vector": vector_to_list(vec),
            "surface_score": 0,
            "tier": get_tier(0),
            "opinions": [],
            "last_updated": utcnow_iso(),
            "history": [],
        }
    rec = targets[target]
    # 老 record 補欄位 (schema migration in-place)
    rec.setdefault("emotion_vector", vector_to_list(default_emotion_vector()))
    rec.setdefault("surface_score", 0)
    rec.setdefault("tier", get_tier(rec.get("surface_score", 0)))
    rec.setdefault("opinions", [])
    rec.setdefault("history", [])
    rec.setdefault("last_updated", utcnow_iso())
    return rec


def _recompute_surface(rec: dict) -> int:
    vec = list_to_vector(rec.get("emotion_vector", []))
    score = compute_surface_score(vec)
    rec["surface_score"] = score
    rec["tier"] = get_tier(score)
    return score


# ──────────────────────────── public API ────────────────────────────

def update_emotion(
    persona: str, target: str,
    axis_deltas: Dict[str, float],
    reason: str,
) -> dict:
    """
    區塊職責：在指定軸上施加 delta（多軸一次更新），re-clamp + recompute surface_score
    物理意義：典型用法 — 一個事件可能同時影響多軸（e.g. 「Tim 給獎勵」→ trust+0.05, respect+0.03, irritation-0.02）
    數值影響：emotion_vector 各軸獨立 clamp 至 [-1, 1]；surface_score / tier 自動 recompute
    """
    doc = load_persona(persona)
    rec = _ensure_target(doc, target)

    vec = list_to_vector(rec["emotion_vector"])
    applied: Dict[str, float] = {}
    for axis, delta in axis_deltas.items():
        if axis not in EMOTION_AXES:
            continue
        try:
            d = float(delta)
        except (TypeError, ValueError):
            continue
        new_v = _clamp(vec[axis] + d, VECTOR_RANGE[0], VECTOR_RANGE[1])
        applied[axis] = round(new_v - vec[axis], 6)   # 實際生效的 delta (clamp 後)
        vec[axis] = new_v
    rec["emotion_vector"] = vector_to_list(vec)
    _recompute_surface(rec)
    rec["last_updated"] = utcnow_iso()
    rec["history"].append({
        "axis_deltas": applied,
        "surface_score_after": rec["surface_score"],
        "reason": reason,
        "at": rec["last_updated"],
    })

    save_persona(persona, doc)
    return rec


def update_affinity(persona: str, target: str, delta: int, reason: str) -> dict:
    """
    區塊職責：v1 compat shim — 把 1D delta 翻譯成多軸更新
    物理意義：正 delta 同時推 trust+affection+respect+interest+loyalty（柔性升好感），
              負 delta 同時推上述軸負向 + irritation 正向
    數值影響：每軸實際施加 delta * 0.01（因 1D delta 通常是 ±5 之類，要 normalize 到 [-1,1] scale）
    """
    scale = float(delta) / 100.0  # delta=10 → 每軸 +0.1
    if delta >= 0:
        axis_deltas = {
            "trust": scale * 0.6,
            "affection": scale * 0.5,
            "respect": scale * 0.4,
            "interest": scale * 0.5,
            "loyalty": scale * 0.4,
            "irritation": -abs(scale) * 0.2,   # 正向事件略降煩躁
        }
    else:
        axis_deltas = {
            "trust": scale * 0.6,             # scale 已負
            "affection": scale * 0.5,
            "respect": scale * 0.4,
            "interest": scale * 0.3,           # 負面事件可能仍引起關注
            "loyalty": scale * 0.5,
            "irritation": abs(scale) * 0.5,    # 負向事件升煩躁
        }
    return update_emotion(persona, target, axis_deltas, reason)


def add_opinion(persona: str, target: str, opinion: str) -> dict:
    """加一條 textual opinion (顯式表面評價)"""
    doc = load_persona(persona)
    rec = _ensure_target(doc, target)
    if opinion not in rec["opinions"]:
        rec["opinions"].append(opinion)
    rec["last_updated"] = utcnow_iso()
    save_persona(persona, doc)
    return rec


def get_affinity(persona: str, target: Optional[str] = None) -> Any:
    """讀單筆或 persona 全部 targets"""
    doc = load_persona(persona)
    if target is not None:
        rec = _ensure_target(doc, target)
        # 不寫檔 (純讀)；ensure 只是返回完整 record
        return rec
    return doc.get("targets", {})


def get_emotion_vector(persona: str, target: str) -> Dict[str, float]:
    """取 hidden emotion vector（dict 形式）— 給程式邏輯讀，UI 用 record["emotion_vector"]"""
    rec = get_affinity(persona, target)
    return list_to_vector(rec.get("emotion_vector", []))


# ──────────────────────────── cross-persona helpers ────────────────────────────

# 區塊職責: 從 persona_registry (schema v3 — per-persona file split) 列出所有 persona 名單
# 物理意義: agent 想對「其他 persona」grant affinity 時, 用此 helper 看誰是合法 target
# 數值影響: 純讀檔; AwakenInit/personas/*.json 不存在則回空 list (graceful)
_PERSONA_REGISTRY_DIR = _tp.REPO_ROOT / "AgentCommands" / "AwakenInit" / "personas"


def list_all_personas() -> List[str]:
    """
    區塊職責: 列 persona_registry 內所有 persona 名單 (含 offline / online)
    物理意義: 對應 awakening.py list_persona_names(), 但本 module 避免 import 依賴所以自己掃
    數值影響: 純讀; 跳過 _ / . 開頭檔; 排序回 List[str]
    """
    if not _PERSONA_REGISTRY_DIR.exists():
        return []
    out = []
    for p in sorted(_PERSONA_REGISTRY_DIR.glob("*.json")):
        name = p.stem
        if name.startswith("_") or name.startswith("."):
            continue
        out.append(name)
    return out


def list_cross_persona_targets(self_persona: str) -> List[str]:
    """
    區塊職責: 列「除了 self_persona 之外」所有 persona — 給 agent 看可 grant affinity 的同事候選
    物理意義: 跨 persona 好感度 (例 basecamp 對 ridge-001 / crest-001 / summit / apex-one ...)
              提供 discoverability; agent 不必憑記憶寫 target name
    數值影響: 純讀
    """
    return [p for p in list_all_personas() if p != self_persona]


def update_cross_persona_emotion(
    self_persona: str, other_persona: str,
    axis_deltas: Dict[str, float],
    reason: str,
) -> dict:
    """
    區塊職責: 對「自己以外的 persona」更新好感度 — semantic alias for update_emotion
    物理意義: 跟普通 update_emotion 完全一樣 (target 本來就接任意字串), 但顯式表達 cross-persona 意圖
              + 順手檢查 target 是否真存在於 persona_registry
    數值影響: target 不在 persona_registry → 印 warning 但仍記錄 (允許對未來 persona 預先標好感)
    """
    if other_persona == self_persona:
        raise ValueError(f"cross-persona affinity self_persona ({self_persona}) 不能等於 other_persona")
    known = set(list_all_personas())
    if known and other_persona not in known:
        import sys as _sys
        print(f"⚠ cross-persona affinity target '{other_persona}' 不在 persona_registry "
              f"(已知: {sorted(known)}); 仍記錄 — 未來 persona 也可預先 grant",
              file=_sys.stderr)
    return update_emotion(self_persona, other_persona, axis_deltas, reason)


# ──────────────────────────── legacy migration ────────────────────────────

_MIGRATION_MARKER = AFFINITY_DIR / ".migrated_from_v1"


def _maybe_migrate_legacy() -> None:
    """
    區塊職責：one-time auto-migrate 舊 affinity_registry.json → 新 affinity/<persona>/relations.json
    物理意義：舊 1D score → 拆到 8 軸的 trust/affection/respect/interest/loyalty 均分（保守估計）
    數值影響：原檔保留為 .v1.bak 不刪；新檔產出後寫 marker，下次不再跑
    """
    if _MIGRATION_MARKER.exists():
        return
    if not LEGACY_REGISTRY_PATH.exists():
        # 沒舊資料也標記為 migrated（避免重跑 file-exists check）
        AFFINITY_DIR.mkdir(parents=True, exist_ok=True)
        _MIGRATION_MARKER.write_text(f"migrated_at={utcnow_iso()}\nlegacy_file=none\n", encoding="utf-8")
        return

    try:
        with LEGACY_REGISTRY_PATH.open("r", encoding="utf-8") as f:
            legacy = json.load(f)
    except Exception:
        # 舊檔壞了仍標記，避免阻塞
        AFFINITY_DIR.mkdir(parents=True, exist_ok=True)
        _MIGRATION_MARKER.write_text(f"migrated_at={utcnow_iso()}\nlegacy_file=corrupt\n", encoding="utf-8")
        return

    personas = (legacy or {}).get("personas", {}) or {}
    migrated_count = 0
    for persona, targets_dict in personas.items():
        if not isinstance(targets_dict, dict):
            continue
        doc = _empty_persona_doc(persona)
        for target, old_rec in targets_dict.items():
            if not isinstance(old_rec, dict):
                continue
            old_score = int(old_rec.get("score", 0))
            # 區塊：1D → 8軸 翻譯邏輯（保守版）
            # 物理意義：以舊 score 為「整體傾向」訊號，按 weight 比例分配到各軸
            normalized = _clamp(old_score / 100.0, -1.0, 1.0)
            vec = default_emotion_vector()
            if old_score >= 0:
                vec["trust"] = normalized * 0.7
                vec["affection"] = normalized * 0.6
                vec["respect"] = normalized * 0.5
                vec["interest"] = normalized * 0.6
                vec["loyalty"] = normalized * 0.5
                vec["admiration"] = normalized * 0.3
            else:
                vec["trust"] = normalized * 0.7
                vec["affection"] = normalized * 0.5
                vec["respect"] = normalized * 0.4
                vec["interest"] = abs(normalized) * 0.3  # 負面也會被「看在眼裡」
                vec["loyalty"] = normalized * 0.5
                vec["irritation"] = abs(normalized) * 0.6

            new_rec = {
                "emotion_vector": vector_to_list(vec),
                "surface_score": compute_surface_score(vec),
                "tier": get_tier(compute_surface_score(vec)),
                "opinions": list(old_rec.get("opinions", []) or []),
                "last_updated": old_rec.get("last_updated", utcnow_iso()),
                "history": [],
            }
            # 把舊 1D history 加註保留（不丟）
            for h in (old_rec.get("history", []) or []):
                if not isinstance(h, dict):
                    continue
                new_rec["history"].append({
                    "axis_deltas": {"_legacy_1d": float(h.get("delta", 0)) / 100.0},
                    "surface_score_after": None,
                    "reason": h.get("reason", "(migrated from v1)"),
                    "at": h.get("at", utcnow_iso()),
                })
            new_rec["history"].append({
                "axis_deltas": {},
                "surface_score_after": new_rec["surface_score"],
                "reason": f"[migration v1→v2] old_score={old_score} → 8-axis vector",
                "at": utcnow_iso(),
            })
            doc["targets"][target] = new_rec
        save_persona(persona, doc)
        migrated_count += 1

    # 備份原檔 → .v1.bak（不刪，方便回看）
    backup = LEGACY_REGISTRY_PATH.with_suffix(".v1.bak")
    try:
        shutil.move(str(LEGACY_REGISTRY_PATH), str(backup))
    except Exception:
        pass

    AFFINITY_DIR.mkdir(parents=True, exist_ok=True)
    _MIGRATION_MARKER.write_text(
        f"migrated_at={utcnow_iso()}\n"
        f"legacy_file={LEGACY_REGISTRY_PATH.name}\n"
        f"backup_to={backup.name}\n"
        f"personas_migrated={migrated_count}\n",
        encoding="utf-8",
    )


# ──────────────────────────── CLI smoke test ────────────────────────────

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "migrate":
        _maybe_migrate_legacy()
        print(f"migration marker → {_MIGRATION_MARKER}")
        print(f"personas now: {list_personas()}")
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "show":
        persona = sys.argv[2] if len(sys.argv) > 2 else None
        if persona:
            print(json.dumps(load_persona(persona), indent=2, ensure_ascii=False))
        else:
            for p in list_personas():
                print(f"- {p}: {len(load_persona(p).get('targets', {}))} targets")
        sys.exit(0)
    print("usage: python -m _lib.affinity_manager [migrate|show [persona]]")
