#!/usr/bin/env python3
"""
workflow_patch.py — Workflow 補丁機制 CLI (Proposal #31)

職責: workflow QA 確認錯誤後, 修正錯誤的同時 register 一筆 patch entry,
      累積 ≥ 3 個 patch 自動警示該 refactor (anti-rot 機制)。

物理意義: 防 workflow 累積 ad-hoc patches 變 spaghetti — 3 patch 上限強制 rethink。

子命令:
  register --workflow <slug> --root-cause "..." --patch-summary "..."
           --applied-by <agent_id> [--qa-bug-ref <X>] [--ucl-core]
                                          register 新 patch (auto-increment id)
  list --workflow <slug>                   列該 workflow 所有 patches
  status --workflow <slug>                 印當前 counter + 是否需 refactor
  status-all                               跨所有 workflow scan, 列需 refactor 的
  refactor --workflow <slug> --refactor-summary "..." --refactored-by <id>
                                          標 refactor done, archive 舊 patches
                                          到 refactor_history.md, counter reset

範例:
  # workflow 出錯, QA confirm bug 後 register patch
  python workflow_patch.py register \\
    --workflow commit-workflow \\
    --root-cause "三層 bump 中 UCL submodule 未切 Dev 分支 → detached HEAD" \\
    --patch-summary "commit 前必先 git -C UCL checkout Dev" \\
    --applied-by claude-da-xiaojie \\
    --qa-bug-ref CommitDetachedHEAD

  # 看狀態
  python workflow_patch.py status --workflow commit-workflow

  # 達 3 patch → refactor
  python workflow_patch.py refactor \\
    --workflow commit-workflow \\
    --refactor-summary "重寫 ucl-commit skill: 加 pre-flight check (branch state / submodule head)" \\
    --refactored-by claude-da-xiaojie

⚠ 設計:
  - 補丁 ≥ 3 → register 第 4 個 reject (強制 refactor)
  - refactor 後 archive 舊 patches 到 refactor_history.md, patch counter reset 為 0
  - storage: docs/Workflows/_patches/<workflow-slug>/
  - cross-link qa-bug-reward: qa-bug-ref 欄位連到 qa_bug_confirmed ledger entry
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys

# Windows console UTF-8 fallback
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def _project_root() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            stderr=subprocess.DEVNULL, text=True,
        ).strip()
    except Exception:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


PROJECT_ROOT = _project_root()
WORKFLOWS_DIR = os.path.join(PROJECT_ROOT, "docs", "Workflows")
PATCHES_ROOT = os.path.join(WORKFLOWS_DIR, "_patches")

PATCH_LIMIT = 3   # 補丁 ≥ 3 → 強制 refactor


def _slug(name: str) -> str:
    """Normalize workflow name to file-safe slug."""
    s = name.strip().lower()
    s = re.sub(r"[^a-z0-9_-]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "unnamed"


def _patches_dir(slug: str) -> str:
    return os.path.join(PATCHES_ROOT, slug)


def _index_path(slug: str) -> str:
    return os.path.join(_patches_dir(slug), "_index.json")


def _history_path(slug: str) -> str:
    return os.path.join(_patches_dir(slug), "refactor_history.md")


def _utc_now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_index(slug: str) -> dict:
    p = _index_path(slug)
    if not os.path.exists(p):
        return {"workflow_slug": slug, "patch_count": 0, "patches": [], "last_refactor_at": None, "refactor_count": 0}
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def _save_index(slug: str, idx: dict) -> None:
    os.makedirs(_patches_dir(slug), exist_ok=True)
    with open(_index_path(slug), "w", encoding="utf-8") as f:
        json.dump(idx, f, indent=2, ensure_ascii=False)


# ---------------- register ----------------
def cmd_register(args):
    slug = _slug(args.workflow)
    idx = _load_index(slug)

    if idx["patch_count"] >= PATCH_LIMIT:
        print(
            f"❌ workflow `{slug}` 已累積 {idx['patch_count']} patches (上限 {PATCH_LIMIT}) — "
            f"必須先 refactor 再 register 新 patch。\n"
            f"   走: python workflow_patch.py refactor --workflow {slug} --refactor-summary \"...\" --refactored-by <id>",
            file=sys.stderr,
        )
        return 3

    patch_id = idx["patch_count"] + 1
    short_name = _slug(args.patch_summary[:40])
    filename = f"{patch_id:03d}_{short_name}.md"
    patch_path = os.path.join(_patches_dir(slug), filename)
    os.makedirs(_patches_dir(slug), exist_ok=True)

    ts = _utc_now()
    fm = (
        f"---\n"
        f"patch_id: {patch_id:03d}\n"
        f"workflow_slug: {slug}\n"
        f"applied_at: {ts}\n"
        f"applied_by: {args.applied_by}\n"
        f"qa_bug_ref: {args.qa_bug_ref or '(none)'}\n"
        f"patch_summary: {json.dumps(args.patch_summary, ensure_ascii=False)}\n"
        f"---\n\n"
        f"# Patch {patch_id:03d}: {args.patch_summary}\n\n"
        f"## 起因 (Root Cause)\n\n{args.root_cause}\n\n"
        f"## 修法 (Patch)\n\n_(請寫入詳細修法 — 加什麼 if-then-else / 在 SKILL/Workflow doc 哪段)_\n\n"
        f"## QA Bug ref\n\n{args.qa_bug_ref or '_(無對應 qa_bug_reward ledger entry)_'}\n\n"
        f"## 適用範圍 / 邊界\n\n_(列出邊界 case + anti-pattern)_\n"
    )
    with open(patch_path, "w", encoding="utf-8") as f:
        f.write(fm)

    idx["patch_count"] = patch_id
    idx["patches"].append({
        "id": patch_id,
        "filename": filename,
        "applied_at": ts,
        "applied_by": args.applied_by,
        "qa_bug_ref": args.qa_bug_ref,
        "summary": args.patch_summary,
    })
    _save_index(slug, idx)

    print(f"[ok] patch {patch_id:03d} registered for workflow `{slug}`")
    print(f"     path: docs/Workflows/_patches/{slug}/{filename}")
    print(f"     applied_by: {args.applied_by}")
    if args.qa_bug_ref:
        print(f"     qa_bug_ref: {args.qa_bug_ref}")
    remaining = PATCH_LIMIT - idx["patch_count"]
    if remaining == 0:
        print(f"⚠ patch count = {PATCH_LIMIT} (上限). 下次 register 會 reject — 該 refactor 了。")
    elif remaining == 1:
        print(f"⚠ patch count = {idx['patch_count']}/{PATCH_LIMIT}, 還剩 1 個 quota — 接近 refactor 警戒。")
    return 0


# ---------------- list ----------------
def cmd_list(args):
    slug = _slug(args.workflow)
    idx = _load_index(slug)
    print(f"# Workflow `{slug}` — patches")
    print(f"- patch_count: {idx['patch_count']} / {PATCH_LIMIT}")
    print(f"- refactor_count: {idx.get('refactor_count', 0)}")
    print(f"- last_refactor_at: {idx.get('last_refactor_at') or '(never)'}")
    print()
    if not idx["patches"]:
        print("_(no patches)_")
        return 0
    print("| ID | Applied By | At | QA Ref | Summary |")
    print("|---|---|---|---|---|")
    for p in idx["patches"]:
        print(f"| {p['id']:03d} | {p['applied_by']} | {p['applied_at']} | {p.get('qa_bug_ref') or '—'} | {p['summary']} |")
    return 0


# ---------------- status ----------------
def cmd_status(args):
    slug = _slug(args.workflow)
    idx = _load_index(slug)
    needs_refactor = idx["patch_count"] >= PATCH_LIMIT
    icon = "🔴" if needs_refactor else ("🟡" if idx["patch_count"] >= 2 else "🟢")
    print(f"{icon} workflow=`{slug}` patches={idx['patch_count']}/{PATCH_LIMIT}")
    if needs_refactor:
        print("    → NEEDS REFACTOR (next register will reject)")
    elif idx["patch_count"] >= 2:
        print(f"    → 接近 refactor 警戒 (還剩 {PATCH_LIMIT - idx['patch_count']} quota)")
    return 0


# ---------------- status-all ----------------
def cmd_status_all(args):
    if not os.path.exists(PATCHES_ROOT):
        print("_(no patches dir yet)_")
        return 0
    summaries = []
    for slug in sorted(os.listdir(PATCHES_ROOT)):
        d = _patches_dir(slug)
        if not os.path.isdir(d): continue
        idx = _load_index(slug)
        summaries.append((slug, idx["patch_count"], idx.get("refactor_count", 0)))
    if not summaries:
        print("_(no workflows under patch tracking)_")
        return 0
    print("# Cross-workflow patch status")
    print()
    print("| Workflow | Patches | Refactors | Status |")
    print("|---|---|---|---|")
    for slug, pc, rc in summaries:
        icon = "🔴" if pc >= PATCH_LIMIT else ("🟡" if pc >= 2 else "🟢")
        status_text = "**NEEDS REFACTOR**" if pc >= PATCH_LIMIT else "ok"
        print(f"| `{slug}` | {pc}/{PATCH_LIMIT} | {rc} | {icon} {status_text} |")
    return 0


# ---------------- refactor ----------------
def cmd_refactor(args):
    slug = _slug(args.workflow)
    idx = _load_index(slug)
    if idx["patch_count"] == 0:
        print(f"⚠ workflow `{slug}` 沒 patches, 為何 refactor? (允許但無意義)", file=sys.stderr)

    # Append 進 refactor_history.md
    hpath = _history_path(slug)
    ts = _utc_now()
    block = f"## Refactor @ {ts}\n\n"
    block += f"- refactored_by: {args.refactored_by}\n"
    block += f"- summary: {args.refactor_summary}\n"
    block += f"- archived patches: {idx['patch_count']}\n\n"
    if idx["patches"]:
        block += "### Archived patch list\n\n"
        for p in idx["patches"]:
            block += f"- {p['id']:03d}_{p.get('filename','')}: {p['summary']} (by {p['applied_by']} @ {p['applied_at']})\n"
        block += "\n"

    os.makedirs(_patches_dir(slug), exist_ok=True)
    mode = "a" if os.path.exists(hpath) else "w"
    if mode == "w":
        with open(hpath, "w", encoding="utf-8") as f:
            f.write(f"# Refactor History — Workflow `{slug}`\n\n")
            f.write("---\n\n")
    with open(hpath, "a", encoding="utf-8") as f:
        f.write(block)

    # Archive 舊 patch md → 加 `_archived_R<refactor_count>` prefix (不刪, 留 audit)
    archived_count = idx.get("refactor_count", 0) + 1
    archived_patches_count = len(idx["patches"])
    for p in idx["patches"]:
        old_path = os.path.join(_patches_dir(slug), p["filename"])
        if os.path.exists(old_path):
            new_path = os.path.join(_patches_dir(slug), f"_archived_R{archived_count:02d}_{p['filename']}")
            try:
                os.rename(old_path, new_path)
            except Exception as e:
                print(f"[warn] archive rename fail for {p['filename']}: {e}", file=sys.stderr)

    # Reset index
    idx["patches"] = []
    idx["patch_count"] = 0
    idx["last_refactor_at"] = ts
    idx["refactor_count"] = archived_count
    _save_index(slug, idx)

    print(f"[ok] workflow `{slug}` refactored (refactor #{archived_count})")
    print(f"     archive: {archived_patches_count} 個舊 patches 已加 _archived_R{archived_count:02d}_ prefix")
    print(f"     counter reset to 0/{PATCH_LIMIT}")
    print(f"     refactor_history: docs/Workflows/_patches/{slug}/refactor_history.md")
    return 0


def main():
    parser = argparse.ArgumentParser(
        prog="workflow_patch.py",
        description="Workflow 補丁機制 CLI (Proposal #31) — register / list / status / refactor",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_reg = sub.add_parser("register", help="register 新 patch")
    p_reg.add_argument("--workflow", required=True, help="workflow slug (e.g. commit-workflow / session-init)")
    p_reg.add_argument("--root-cause", required=True, help="bug root cause")
    p_reg.add_argument("--patch-summary", required=True, help="一句修法 (filename 用)")
    p_reg.add_argument("--applied-by", required=True)
    p_reg.add_argument("--qa-bug-ref", default=None, help="對應 qa_bug_reward ledger entry ref")
    p_reg.set_defaults(func=cmd_register)

    p_list = sub.add_parser("list", help="列 workflow 所有 patches")
    p_list.add_argument("--workflow", required=True)
    p_list.set_defaults(func=cmd_list)

    p_st = sub.add_parser("status", help="印 workflow refactor 警戒狀態")
    p_st.add_argument("--workflow", required=True)
    p_st.set_defaults(func=cmd_status)

    p_sta = sub.add_parser("status-all", help="跨 workflow scan")
    p_sta.set_defaults(func=cmd_status_all)

    p_ref = sub.add_parser("refactor", help="標記 refactor done, archive 舊 patches")
    p_ref.add_argument("--workflow", required=True)
    p_ref.add_argument("--refactor-summary", required=True)
    p_ref.add_argument("--refactored-by", required=True)
    p_ref.set_defaults(func=cmd_refactor)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
