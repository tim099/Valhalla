#!/usr/bin/env python3
"""plan_index.py — Plan 文檔整理 / 大綱掃描工具 (2026-05-23 basecamp, Tim task).

# 區塊職責：給 agent 一個「不吃全文」的 Plan 盤點工具 — 只抽 frontmatter +
#          各級標題(大綱) + 一句話摘要, 絕不把正文灌進 context。
# 物理意義：純 file system 串流讀取, 逐行掃描時只保留標題行 / frontmatter /
#          首句摘要, 不累積 body; 對每個 Plan 的 context footprint = O(標題數)。
# 數值影響：read-only, 不寫不改任何 Plan 檔, 對運行系統零副作用 (catalog --out 除外)。

解決問題: docs/Plan 有 50+ 份 Plan, agent 要盤點得逐份 Read = context 爆炸。
本工具掃出每份的標題/狀態/大綱, 讓 agent 用一次工具輸出就掌握全貌。

掃描根 (PLAN_ROOTS):
  - docs/Plan/                                         (英勇紋章 EOV)
  - CardGame/Assets/UCL/UCL_Core/Docs~/zh-Hant/Plan/   (UCL_Core 跨專案共用)

五個 op:
  list      — 一行一份: [status] name — title (H:標題數 / L:行數)
  outline   — 印某份(或全部)的標題樹大綱 (Tim 要的「掃出 Plan 大綱」)
  catalog   — 分組 markdown 目錄 (--out 可寫檔, 預設 stdout)
  search    — 只比對 title + 各級標題 (不碰正文) 的關鍵字搜尋
  lint      — 列出尚未採用 Plan frontmatter 格式的檔 (格式採用率追蹤)

使用範例:
  python plan_index.py list
  python plan_index.py list --root eov           # 只看 EOV
  python plan_index.py outline Plan_Work_Session_Mechanism
  python plan_index.py outline all --max-level 2  # 全部, 只到 ## 層
  python plan_index.py catalog --out docs/Plan/INDEX.generated.md
  python plan_index.py search tavern
  python plan_index.py lint

── 提議的 Plan frontmatter 格式 (之後採用; 工具讀得到, 沒有時 graceful degrade) ──
  ---
  title:   <一句話標題>
  status:  draft | active | done | superseded | abandoned
  theme:   <主題標籤, e.g. tavern / economy / awakening>
  owner:   <persona / Tim>
  created: YYYY-MM-DD
  updated: YYYY-MM-DD
  summary: <一句話摘要>
  supersedes: <被本 Plan 取代的舊 Plan 檔名>   # optional
  ---
採用後 list/catalog 會自動用 status/theme/summary; 未採用則從 H1/blockquote 推斷。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import NamedTuple, Optional

# Windows console cp950 → UTF-8 避免中文印錯
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = Path(__file__).resolve().parent
# 推斷 project root: 本工具在 AgentCommands/Tools/, repo = parent.parent
REPO_ROOT = HERE.parent.parent

# T-PATH-02: UCL_Core Docs~ 走 layout-agnostic resolver, 不再寫死 CardGame/Assets/UCL/UCL_Core。
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from AgentCommands._lib import tavern_paths as _tp  # noqa: E402
try:
    _ucl_plan_rel = _tp.UCL_CORE_DIR.resolve().relative_to(REPO_ROOT.resolve()) / "Docs~" / "zh-Hant" / "Plan"
except ValueError:
    # UCL_Core 不在 repo root 下 (罕見) → 退回舊 CardGame 布局字面值
    _ucl_plan_rel = Path("CardGame/Assets/UCL/UCL_Core/Docs~/zh-Hant/Plan")

# 區塊職責：Plan 掃描根定義
# 物理意義：(label, 相對 repo root 的路徑) — label 給 --root 過濾用
# 數值影響：新增掃描根只要在此 append 一筆
PLAN_ROOTS = [
    ("eov", Path("docs/Plan")),
    ("ucl", _ucl_plan_rel),
]

# frontmatter 認得的欄位 (提議格式; 缺了不報錯)
FM_KEYS = {"title", "status", "theme", "owner", "created", "updated", "summary", "supersedes", "related"}

# 非 Plan 的特殊檔名 (索引檔本身), enumerate 時標註但不當成 Plan 內容
INDEX_NAMES = {"INDEX.md", "INDEX.generated.md"}


class PlanInfo(NamedTuple):
    """單份 Plan 抽取出的輕量 metadata (絕不含正文)。"""
    root_label: str                  # 'eov' / 'ucl'
    path: Path                       # 絕對路徑
    rel: str                         # 相對 repo root 的顯示路徑
    name: str                        # 檔名 (含 .md)
    title: str                       # frontmatter title / 首個 H1 / 檔名 stem
    status: str                      # frontmatter status / '—'
    theme: str                       # frontmatter theme / '—'
    summary: str                     # frontmatter summary / 首句 blockquote / 首段 / ''
    headings: list                   # [(level:int, text:str), ...] 全文標題樹
    line_count: int                  # 總行數
    has_frontmatter: bool            # 是否有 YAML frontmatter (格式採用判定)
    is_index: bool                   # 是否為 INDEX 檔


def _parse_plan(root_label: str, path: Path) -> PlanInfo:
    """串流解析單份 Plan — 只留標題 / frontmatter / 首句摘要, 不累積正文。

    物理意義: 逐行掃, fenced code block 內的 '#' 不算標題;
              frontmatter 僅限「檔案第一行為 ---」才認。
    """
    fm: dict = {}                    # frontmatter key→value
    headings: list = []              # (level, text)
    title_h1: Optional[str] = None   # 首個 H1 文字
    first_quote: Optional[str] = None  # 首句 blockquote (> ...)
    first_para: Optional[str] = None   # 首個普通段落行
    in_fm = False                    # 是否在 frontmatter 區
    has_fm = False                   # 是否偵測到 frontmatter
    in_code = False                  # 是否在 ``` 圍籬內
    line_count = 0

    with open(path, encoding="utf-8", errors="replace") as f:
        for i, raw in enumerate(f):
            line_count += 1
            line = raw.rstrip("\n")

            # frontmatter: 僅當「第一行就是 ---」才開啟
            if i == 0 and line.strip() == "---":
                in_fm = True
                has_fm = True
                continue
            if in_fm:
                if line.strip() in ("---", "..."):
                    in_fm = False
                    continue
                # 簡易 key: value 解析 (不依賴 yaml lib)
                if ":" in line:
                    k, _, v = line.partition(":")
                    k = k.strip().lower()
                    if k in FM_KEYS:
                        fm[k] = v.strip()
                continue

            # code fence 切換 (圍籬內的 # 不是標題)
            stripped = line.lstrip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_code = not in_code
                continue
            if in_code:
                continue

            # ATX 標題: #..###### + 空白 + 文字
            if stripped.startswith("#"):
                hashes = len(stripped) - len(stripped.lstrip("#"))
                if 1 <= hashes <= 6 and stripped[hashes:hashes + 1] in (" ", "\t"):
                    text = stripped[hashes:].strip().rstrip("#").strip()
                    if text:
                        headings.append((hashes, text))
                        if title_h1 is None and hashes == 1:
                            title_h1 = text
                    continue

            # 摘要候選: 首句 blockquote / 首段普通行
            s = line.strip()
            if not s:
                continue
            if s.startswith(">") and first_quote is None:
                first_quote = s.lstrip(">").strip()
            elif first_para is None and not s.startswith(("-", "*", "|", ">", "<!--")):
                first_para = s

    name = path.name
    title = fm.get("title") or title_h1 or path.stem
    summary = fm.get("summary") or first_quote or first_para or ""
    # 摘要去掉粗體/標記雜訊 + 截斷
    summary = summary.replace("**", "").strip()
    if len(summary) > 110:
        summary = summary[:107] + "…"

    return PlanInfo(
        root_label=root_label,
        path=path,
        rel=str(path.relative_to(REPO_ROOT)).replace("\\", "/"),
        name=name,
        title=title,
        status=fm.get("status", "—"),
        theme=fm.get("theme", "—"),
        summary=summary,
        headings=headings,
        line_count=line_count,
        has_frontmatter=has_fm,
        is_index=name in INDEX_NAMES,
    )


def _collect(root_filter: Optional[str] = None) -> list:
    """掃所有 (或指定) 根下的 *.md → list[PlanInfo], 依檔名排序。"""
    out: list = []
    for label, rel in PLAN_ROOTS:
        if root_filter and label != root_filter:
            continue
        root = REPO_ROOT / rel
        if not root.is_dir():
            continue
        for p in sorted(root.glob("*.md")):
            out.append(_parse_plan(label, p))
    return out


def _root_title(label: str) -> str:
    return {"eov": "英勇紋章 (EOV) — docs/Plan", "ucl": "UCL_Core — Docs~/zh-Hant/Plan"}.get(label, label)


# ─────────────────────────── ops ───────────────────────────

def cmd_list(args) -> int:
    """一行一份: [status] name — title (H:標題數 / L:行數)。"""
    plans = _collect(args.root)
    cur_root = None
    n_plan = 0
    for pi in plans:
        if pi.root_label != cur_root:
            cur_root = pi.root_label
            print(f"\n## {_root_title(cur_root)}")
        tag = "📑" if pi.is_index else "•"
        st = f"[{pi.status}]" if pi.status != "—" else "[—]"
        print(f"  {tag} {st:>12} {pi.name}")
        if pi.title and pi.title != pi.name and pi.title != pi.name[:-3]:
            print(f"        ↳ {pi.title}   (H:{len(pi.headings)} / L:{pi.line_count})")
        else:
            print(f"        ↳ (H:{len(pi.headings)} / L:{pi.line_count})")
        if not pi.is_index:
            n_plan += 1
    print(f"\n— 共 {n_plan} 份 Plan (跨 {len({p.root_label for p in plans})} 個根){' [僅 ' + args.root + ']' if args.root else ''}")
    return 0


def cmd_outline(args) -> int:
    """印某份(或 all)的標題樹大綱。"""
    plans = _collect(args.root)
    target = args.name
    if target and target.lower() != "all":
        key = target.lower().removesuffix(".md")
        plans = [p for p in plans if key in p.name.lower() or key in p.title.lower()]
        if not plans:
            print(f"❌ 找不到符合 '{target}' 的 Plan", file=sys.stderr)
            return 1
    for pi in plans:
        meta = f"status={pi.status} theme={pi.theme}" if (pi.status != "—" or pi.theme != "—") else "(無 frontmatter)"
        print(f"\n━━ {pi.name}  [{meta}]")
        if pi.title and pi.title != pi.name[:-3]:
            print(f"   {pi.title}")
        for lvl, text in pi.headings:
            if lvl > args.max_level:
                continue
            print(f"   {'  ' * (lvl - 1)}{'#' * lvl} {text}")
        if not pi.headings:
            print("   (無標題 — 可能是純段落 Plan)")
    return 0


def cmd_catalog(args) -> int:
    """分組 markdown 目錄 (預設 stdout; --out 寫檔)。"""
    plans = _collect(args.root)
    lines: list = ["# Plan 目錄 (plan_index.py 自動生成)", ""]
    lines.append(f"> 自動掃描生成, 勿手改。重生: `python AgentCommands/Tools/plan_index.py catalog --out <file>`")
    lines.append("")
    cur_root = None
    n_plan = 0
    for pi in plans:
        if pi.is_index:
            continue
        if pi.root_label != cur_root:
            cur_root = pi.root_label
            lines.append(f"\n## {_root_title(cur_root)}\n")
        st = "" if pi.status == "—" else f" `[{pi.status}]`"
        desc = f" — {pi.summary}" if pi.summary else (f" — {pi.title}" if pi.title != pi.name[:-3] else "")
        lines.append(f"- **{pi.name}**{st}{desc}")
        n_plan += 1
    lines.append(f"\n---\n_共 {n_plan} 份 Plan。_")
    body = "\n".join(lines) + "\n"
    if args.out:
        out_path = REPO_ROOT / args.out
        out_path.write_text(body, encoding="utf-8")
        print(f"✓ 目錄已寫入 {out_path.relative_to(REPO_ROOT)} ({n_plan} 份 Plan)")
    else:
        print(body)
    return 0


def cmd_search(args) -> int:
    """只比對 title + 各級標題 (不碰正文)。"""
    kw = args.keyword.lower()
    plans = _collect(args.root)
    hits = 0
    for pi in plans:
        title_hit = kw in pi.name.lower() or kw in pi.title.lower()
        head_hits = [(lvl, t) for lvl, t in pi.headings if kw in t.lower()]
        if title_hit or head_hits:
            hits += 1
            print(f"\n📄 {pi.name}  [{pi.status}]")
            if title_hit:
                print(f"   title: {pi.title}")
            for lvl, t in head_hits:
                print(f"   {'#' * lvl} {t}")
    print(f"\n— {hits} 份 Plan 命中 '{args.keyword}' (僅比對 title/標題, 未碰正文)")
    return 0


def cmd_lint(args) -> int:
    """列出尚未採用 Plan frontmatter 格式的檔 (採用率追蹤)。"""
    plans = _collect(args.root)
    have = [p for p in plans if p.has_frontmatter and not p.is_index]
    miss = [p for p in plans if not p.has_frontmatter and not p.is_index]
    total = len(have) + len(miss)
    print(f"=== Plan frontmatter 採用率: {len(have)}/{total} ===\n")
    if have:
        print("✅ 已採用:")
        for p in have:
            print(f"   {p.name}  (status={p.status} theme={p.theme})")
        print()
    print("⬜ 未採用 (從 H1/blockquote 推斷 title/summary):")
    for p in miss:
        print(f"   {p.name}")
    print(f"\n— 提議格式見本工具 --help / 模組 docstring 頂部")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Plan 整理 / 大綱掃描工具 (不吃全文)")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_root(sp):
        sp.add_argument("--root", choices=[lbl for lbl, _ in PLAN_ROOTS], default=None,
                        help="只掃指定根 (eov / ucl); 省略=全掃")

    pl = sub.add_parser("list", help="一行一份摘要清單")
    add_root(pl)
    pl.set_defaults(func=cmd_list)

    po = sub.add_parser("outline", help="印標題樹大綱 (某份 / all)")
    po.add_argument("name", nargs="?", default="all", help="Plan 名 (substring) 或 all")
    po.add_argument("--max-level", type=int, default=6, help="只到第 N 級標題 (預設 6)")
    add_root(po)
    po.set_defaults(func=cmd_outline)

    pc = sub.add_parser("catalog", help="分組 markdown 目錄")
    pc.add_argument("--out", default=None, help="寫入檔案 (相對 repo root); 省略=印 stdout")
    add_root(pc)
    pc.set_defaults(func=cmd_catalog)

    ps = sub.add_parser("search", help="只比對 title/標題的關鍵字搜尋")
    ps.add_argument("keyword", help="關鍵字 (case-insensitive)")
    add_root(ps)
    ps.set_defaults(func=cmd_search)

    pn = sub.add_parser("lint", help="frontmatter 格式採用率追蹤")
    add_root(pn)
    pn.set_defaults(func=cmd_lint)

    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
