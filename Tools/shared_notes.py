#!/usr/bin/env python3
"""
shared_notes.py — SharedNotes 共同學習筆記 CLI（Phase A 核心讀寫）

設計依據：docs/Plan/Plan_SharedNotes_Framework.md

核心 commands：
- add           寫一筆 note (frontmatter + body)
- show          印整篇 note
- list          列 notes (by author / topic / subject / tag / since)
- search        全文搜尋
- find-related  ★ 按 subject (code symbol / system name) 精準查詢相關 notes
- append-comment 對某 note 在末尾追加補注 (其他 persona 視角)
- reindex       重建 _index.md + _topics/ + _subjects/ 索引

Folder layout (per-project)：
  AgentCommands/SharedNotes/
  ├── _index.md
  ├── _topics/<topic>.md
  ├── _subjects/<symbol>.md   ← Tim 2026-05-30 強調的 recall 入口
  └── notes/YYYYMMDD_<persona>_<slug>.md
"""

import argparse
import datetime as _dt
import io
import json
import os
import re
import sys
from pathlib import Path

# Windows cp950 fix: force stdout/stderr to utf-8 for unicode chars
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ────────────────────────────────────────────────────────────────────────
# 路徑解析
# ────────────────────────────────────────────────────────────────────────
def get_repo_root():
    """從本檔位置反推 repo root (主專案根)"""
    here = Path(__file__).resolve()
    # AgentCommands/Tools/shared_notes.py → repo_root = parent.parent.parent
    return here.parent.parent.parent

REPO_ROOT = get_repo_root()
NOTES_ROOT = REPO_ROOT / "AgentCommands" / "SharedNotes"
NOTES_DIR = NOTES_ROOT / "notes"
TOPICS_DIR = NOTES_ROOT / "_topics"
SUBJECTS_DIR = NOTES_ROOT / "_subjects"
INDEX_FILE = NOTES_ROOT / "_index.md"

def ensure_dirs():
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    TOPICS_DIR.mkdir(parents=True, exist_ok=True)
    SUBJECTS_DIR.mkdir(parents=True, exist_ok=True)

# ────────────────────────────────────────────────────────────────────────
# note_type 軸 (WorkNotes v2, Tim 2026-07-07 拍板 + apex-one/summit feedback)
# 雙軸分類: subject (code symbol, 在哪) × note_type (哪種知識)。
# ONBOARD_ORDER = 接手時「見林先於見樹」的建議閱讀順序 (summit 認證的殺手鐧)。
# ────────────────────────────────────────────────────────────────────────
NOTE_TYPES = ["map", "concept", "howto", "decision", "runbook"]
NOTE_TYPE_DESC = {
    "map":      "🗺  東西在哪 (入口檔 / 關鍵路徑)",
    "concept":  "💡 系統怎麼運作 (心智模型)",
    "howto":    "🔧 SOP / 操作步驟",
    "decision": "⚖  為何這樣設計 (取捨紀錄)",
    "runbook":  "🚑 出事怎麼修 (recovery)",
}
ONBOARD_ORDER = NOTE_TYPES  # map → concept → howto → decision → runbook
_UNCLASSIFIED = "unclassified"  # 舊 note 無 note_type 時的 bucket (backward-compat, 排最後)

def note_type_of(fm):
    """讀 note 的 note_type, 缺 / 非法 → unclassified (backward-compat)。"""
    nt = (fm.get("note_type") or "").strip()
    return nt if nt in NOTE_TYPES else _UNCLASSIFIED

# ────────────────────────────────────────────────────────────────────────
# Frontmatter parser (簡易 YAML, 不依賴 yaml lib)
# ────────────────────────────────────────────────────────────────────────
def parse_frontmatter(text):
    """簡易 frontmatter parser (limited YAML subset).
    Returns (frontmatter_dict, body_str). Returns (None, text) if no frontmatter."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    fm_text = text[4:end]
    body = text[end+5:]
    fm = {}
    cur_list_key = None
    for line in fm_text.split("\n"):
        if not line.strip():
            continue
        if line.startswith("  - ") and cur_list_key:
            fm[cur_list_key].append(line[4:].strip())
            continue
        cur_list_key = None
        m = re.match(r"^([a-zA-Z_]+):\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2)
        if val.strip() == "":
            # 開始 list
            fm[key] = []
            cur_list_key = key
        elif val.startswith("[") and val.endswith("]"):
            # inline list
            inner = val[1:-1].strip()
            fm[key] = [s.strip() for s in inner.split(",") if s.strip()] if inner else []
        else:
            fm[key] = val.strip()
    return fm, body

def write_frontmatter(fm):
    """Dict → YAML frontmatter str (含 --- 邊界)"""
    lines = ["---"]
    for key, val in fm.items():
        if isinstance(val, list):
            if not val:
                lines.append(f"{key}: []")
            else:
                lines.append(f"{key}:")
                for item in val:
                    lines.append(f"  - {item}")
        else:
            lines.append(f"{key}: {val}")
    lines.append("---")
    return "\n".join(lines) + "\n"

# ────────────────────────────────────────────────────────────────────────
# Note 載入
# ────────────────────────────────────────────────────────────────────────
def load_all_notes():
    """掃 notes/ 載入所有 note (path, frontmatter, body)"""
    ensure_dirs()
    result = []
    for path in sorted(NOTES_DIR.glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
            fm, body = parse_frontmatter(text)
            if fm is None:
                continue
            result.append((path, fm, body))
        except Exception as e:
            print(f"⚠ skip {path.name}: {e}", file=sys.stderr)
    return result

# ────────────────────────────────────────────────────────────────────────
# CMD: add
# ────────────────────────────────────────────────────────────────────────
def cmd_add(args):
    ensure_dirs()
    title = args.title
    author = args.author
    topics = [t.strip() for t in (args.topics or "").split(",") if t.strip()]
    tags = [t.strip() for t in (args.tags or "").split(",") if t.strip()]
    subjects = [s.strip() for s in (args.subjects or "").split(",") if s.strip()]
    related_notes = [r.strip() for r in (args.related_notes or "").split(",") if r.strip()]

    if not title or not author:
        print("✗ --title 跟 --author 必填", file=sys.stderr)
        return 1

    # slug from --slug or title
    slug = args.slug
    if not slug:
        slug = re.sub(r"[^a-zA-Z0-9一-鿿\- ]", "", title.lower())
        slug = re.sub(r"\s+", "-", slug.strip())[:60]
    slug = slug.strip("-")

    today = _dt.datetime.now().strftime("%Y%m%d")
    note_id = f"{today}_{author}_{slug}"
    note_path = NOTES_DIR / f"{note_id}.md"
    if note_path.exists():
        print(f"✗ note 已存在: {note_path.name} (改用 update 或加 --slug)", file=sys.stderr)
        return 1

    # body 從 --body-file 或 --body 或 stdin
    if args.body_file:
        body = Path(args.body_file).read_text(encoding="utf-8")
    elif args.body:
        body = args.body
    else:
        print("ℹ stdin 讀 body (Ctrl-D 結束)...", file=sys.stderr)
        body = sys.stdin.read()

    fm = {
        "id": note_id,
        "title": title,
        "author_persona": author,
        "author_agent": args.author_agent or "claude-code",
        "created": _dt.date.today().isoformat(),
        "last_updated": _dt.date.today().isoformat(),
        "note_type": args.note_type,          # WorkNotes v2 雙軸之一 (map/concept/howto/decision/runbook)
        "topics": topics,
        "subjects": subjects,
        "tags": tags,
        "related_notes": related_notes,
        "supersedes": args.supersedes or "",  # fork 紀律: 只在「理解被顛覆/實質加深」才填, 小修原地改
        "visibility": args.visibility or "public",
        "status": "live",
    }
    note_path.write_text(write_frontmatter(fm) + "\n" + body.strip() + "\n", encoding="utf-8")
    print(f"✓ note ship: {note_path.relative_to(REPO_ROOT)}")
    print(f"  id: {note_id}")
    print(f"  note_type: {args.note_type}")
    if topics:
        print(f"  topics: {', '.join(topics)}")
    if subjects:
        print(f"  subjects: {', '.join(subjects)}")

    # fork 紀律: 顯式 --supersedes → 把舊 note 標 superseded (不刪, 版本史可回溯; summit ② 拍板)
    if args.supersedes:
        old_id = args.supersedes.strip()
        marked = False
        for path, ofm, obody in load_all_notes():
            if ofm.get("id") == old_id:
                ofm["status"] = f"superseded_by:{note_id}"
                ofm["last_updated"] = _dt.date.today().isoformat()
                path.write_text(write_frontmatter(ofm) + "\n" + obody, encoding="utf-8")
                marked = True
                print(f"  ⤿ superseded 舊版 {old_id} (保留檔案, status 標記, 不刪)")
                break
        if not marked:
            print(f"  ⚠ --supersedes 指的 {old_id} 找不到 (新 note 仍已寫入)")

    print(f"  → 跑 'reindex' 更新索引")
    return 0

# ────────────────────────────────────────────────────────────────────────
# CMD: show
# ────────────────────────────────────────────────────────────────────────
def cmd_show(args):
    ensure_dirs()
    target_id = args.id
    notes = load_all_notes()
    for path, fm, body in notes:
        if fm.get("id") == target_id:
            print(f"📄 {path.relative_to(REPO_ROOT)}\n")
            print(write_frontmatter(fm))
            print(body)
            return 0
    print(f"✗ note '{target_id}' 找不到", file=sys.stderr)
    return 1

# ────────────────────────────────────────────────────────────────────────
# CMD: list
# ────────────────────────────────────────────────────────────────────────
def cmd_list(args):
    notes = load_all_notes()
    if not notes:
        print("(no notes yet)")
        return 0
    filtered = []
    for path, fm, body in notes:
        if args.author and fm.get("author_persona") != args.author:
            continue
        if args.topic and args.topic not in fm.get("topics", []):
            continue
        if args.subject and args.subject not in fm.get("subjects", []):
            continue
        if args.tag and args.tag not in fm.get("tags", []):
            continue
        if args.since:
            note_date = fm.get("created", "")
            if note_date < args.since:
                continue
        if args.status and fm.get("status", "live") != args.status:
            continue
        filtered.append((path, fm))
    filtered.sort(key=lambda x: x[1].get("created", ""), reverse=True)
    print(f"📋 {len(filtered)} note(s):\n")
    for path, fm in filtered:
        title = fm.get("title", "(no title)")
        author = fm.get("author_persona", "?")
        created = fm.get("created", "?")
        subjects = ", ".join(fm.get("subjects", [])[:3])
        print(f"  [{created}] @{author}  {title}")
        print(f"     id: {fm.get('id')}")
        if subjects:
            print(f"     subjects: {subjects}")
        print()
    return 0

# ────────────────────────────────────────────────────────────────────────
# CMD: search (全文)
# ────────────────────────────────────────────────────────────────────────
def cmd_search(args):
    notes = load_all_notes()
    query = args.query.lower()
    hits = []
    for path, fm, body in notes:
        if query in body.lower() or query in fm.get("title", "").lower():
            # 找 context line
            for line in body.split("\n"):
                if query in line.lower():
                    hits.append((path, fm, line.strip()[:120]))
                    break
    if not hits:
        print(f"(no match for '{query}')")
        return 0
    print(f"🔍 {len(hits)} hit(s) for '{query}':\n")
    for path, fm, ctx in hits:
        print(f"  [{fm.get('created')}] @{fm.get('author_persona')}  {fm.get('title')}")
        print(f"     id: {fm.get('id')}")
        print(f"     ctx: ...{ctx}...")
        print()
    return 0

# ────────────────────────────────────────────────────────────────────────
# CMD: find-related ★ Tim 強調的 recall 入口
# ────────────────────────────────────────────────────────────────────────
def cmd_find_related(args):
    """按 subject (code symbol / system name) 精準查詢相關 notes.
    跟 search 不同 — 只看 frontmatter subjects 欄位, 不撞全文 noise."""
    notes = load_all_notes()
    query = args.subject
    hits = []
    for path, fm, body in notes:
        subjects = fm.get("subjects", [])
        # case-insensitive 比對
        if any(s.lower() == query.lower() for s in subjects):
            hits.append((path, fm))
    if not hits:
        print(f"(no note related to '{query}')")
        print(f"  → 提示: 若有相關經驗該 ship 一筆 — 跑 'shared_notes.py add --subjects {query}'")
        return 0
    hits.sort(key=lambda x: x[1].get("created", ""), reverse=True)
    print(f"🎯 {len(hits)} note(s) related to subject '{query}':\n")
    for path, fm in hits:
        title = fm.get("title", "(no title)")
        author = fm.get("author_persona", "?")
        created = fm.get("created", "?")
        print(f"  [{created}] @{author}  {title}")
        print(f"     id: {fm.get('id')}")
        print(f"     subjects: {', '.join(fm.get('subjects', []))}")
        print(f"     path: {path.relative_to(REPO_ROOT)}")
        print()
    return 0

# ────────────────────────────────────────────────────────────────────────
# CMD: onboard ★ 殺手鐧 (WorkNotes v2) — 見林先於見樹
#   給 subject/topic, 回「map→concept→howto→decision→runbook」建議閱讀順序,
#   讓接手者一句話拿到子系統地圖 (summit 認證: 這比任何單張卡都值錢)。
# ────────────────────────────────────────────────────────────────────────
def cmd_onboard(args):
    if not args.subject and not args.topic:
        print("✗ onboard 需 --subject <code symbol> 或 --topic <topic> 其一", file=sys.stderr)
        return 1
    notes = load_all_notes()
    key, val = ("subject", args.subject) if args.subject else ("topic", args.topic)
    field = "subjects" if args.subject else "topics"

    # 收該 subject/topic 的 live notes (superseded 排除, 只給接手者現行版)
    matched = []
    for path, fm, body in notes:
        if str(fm.get("status", "live")).startswith("superseded"):
            continue
        if any(x.lower() == val.lower() for x in fm.get(field, [])):
            # 抓 body 第一行非空當一句摘要
            first = next((ln.strip() for ln in body.split("\n") if ln.strip() and not ln.startswith("#")), "")
            matched.append((fm, first[:90]))

    if not matched:
        print(f"(no note under {key} '{val}')")
        print(f"  → 若你剛上手這塊, ship 第一張卡: shared_notes.py add --{key}s {val} --note-type map ...")
        return 0

    # 依 note_type 分桶
    buckets = {nt: [] for nt in ONBOARD_ORDER}
    buckets[_UNCLASSIFIED] = []
    for fm, first in matched:
        buckets[note_type_of(fm)].append((fm, first))

    print(f"🧭 Onboard — {key} `{val}`  ({len(matched)} 張現行卡)")
    print(f"   建議閱讀順序 (見林先於見樹):\n")
    order = ONBOARD_ORDER + [_UNCLASSIFIED]
    for nt in order:
        entries = buckets.get(nt, [])
        if not entries:
            continue
        label = NOTE_TYPE_DESC.get(nt, "❔ 未分類 (建議補 --note-type)")
        print(f"── {nt}  {label} ──")
        for fm, first in entries:
            print(f"  • {fm.get('title','(no title)')}  @{fm.get('author_persona','?')} ({fm.get('created','?')})")
            print(f"      id: {fm.get('id')}")
            if first:
                print(f"      ▸ {first}")
        print()
    print(f"→ 讀單張: shared_notes.py show --id <id>")
    return 0

# ────────────────────────────────────────────────────────────────────────
# CMD: append-comment (其他 persona 對某 note 補注)
# ────────────────────────────────────────────────────────────────────────
def cmd_append_comment(args):
    notes = load_all_notes()
    target_id = args.id
    for path, fm, body in notes:
        if fm.get("id") == target_id:
            author = args.author
            today = _dt.date.today().isoformat()
            comment_line = f"- **{author}** @ {today}: {args.body}"
            # 找 ## 補注 section，沒有就 append
            if "## 補注" in body:
                # append 到該 section
                new_body = body.rstrip() + "\n" + comment_line + "\n"
            else:
                new_body = body.rstrip() + "\n\n## 補注\n\n" + comment_line + "\n"
            fm["last_updated"] = today
            path.write_text(write_frontmatter(fm) + "\n" + new_body, encoding="utf-8")
            print(f"✓ comment appended to {path.name}")
            return 0
    print(f"✗ note '{target_id}' 找不到", file=sys.stderr)
    return 1

# ────────────────────────────────────────────────────────────────────────
# CMD: reindex (重建 _index.md + _topics/ + _subjects/)
# ────────────────────────────────────────────────────────────────────────
def cmd_reindex(args):
    ensure_dirs()
    notes = load_all_notes()

    # 清舊 _topics/ + _subjects/ 內容
    for d in [TOPICS_DIR, SUBJECTS_DIR]:
        for f in d.glob("*.md"):
            f.unlink()

    # 聚合 by topic / subject
    by_topic = {}
    by_subject = {}
    for path, fm, body in notes:
        if fm.get("status", "live") != "live":
            continue
        for t in fm.get("topics", []):
            by_topic.setdefault(t, []).append((path, fm))
        for s in fm.get("subjects", []):
            by_subject.setdefault(s, []).append((path, fm))

    # 寫 _topics/<topic>.md
    for topic, entries in by_topic.items():
        entries.sort(key=lambda x: x[1].get("created", ""), reverse=True)
        lines = [f"# Notes — Topic: `{topic}`\n"]
        for path, fm in entries:
            title = fm.get("title", "(no title)")
            author = fm.get("author_persona", "?")
            note_id = fm.get("id", "")
            lines.append(f"- [{title}](../notes/{note_id}.md) — @{author} ({fm.get('created')})")
        (TOPICS_DIR / f"{topic}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # 寫 _subjects/<symbol>.md (★ Tim 強調的 recall 入口)
    for subject, entries in by_subject.items():
        entries.sort(key=lambda x: x[1].get("created", ""), reverse=True)
        # 把檔名安全化 (subject 可能含 < > / 等字符)
        safe_subject = re.sub(r"[^a-zA-Z0-9_\-一-鿿]", "_", subject)
        lines = [f"# Notes about `{subject}`\n"]
        lines.append(f"此 subject 涉及以下 notes (新到舊)。接手先跑 `shared_notes.py onboard --subject {subject}` 拿建議閱讀順序:\n")
        for path, fm in entries:
            title = fm.get("title", "(no title)")
            author = fm.get("author_persona", "?")
            note_id = fm.get("id", "")
            lines.append(f"- `[{note_type_of(fm)}]` [{title}](../notes/{note_id}.md) — @{author} ({fm.get('created')})")
        (SUBJECTS_DIR / f"{safe_subject}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # 寫 _index.md
    lines = [
        "# SharedNotes Index — 共同學習筆記索引",
        "",
        f"自動 gen by `shared_notes.py reindex` @ {_dt.datetime.now().isoformat(timespec='seconds')}",
        "",
        f"## 全部 notes ({len(notes)})",
        "",
    ]
    notes_sorted = sorted(notes, key=lambda x: x[1].get("created", ""), reverse=True)
    for path, fm, body in notes_sorted:
        if fm.get("status", "live") != "live":
            continue
        title = fm.get("title", "(no title)")
        author = fm.get("author_persona", "?")
        note_id = fm.get("id", "")
        lines.append(f"- `[{note_type_of(fm)}]` [{title}](notes/{note_id}.md) — @{author} ({fm.get('created')})")

    lines.append("")
    lines.append(f"## Topics ({len(by_topic)})")
    lines.append("")
    for topic in sorted(by_topic.keys()):
        lines.append(f"- [{topic}](_topics/{topic}.md) ({len(by_topic[topic])} note(s))")

    lines.append("")
    lines.append(f"## Subjects ({len(by_subject)}) — code symbols / 系統名")
    lines.append("")
    lines.append("★ 動陌生 class / Cmd 前可跑：`shared_notes.py find-related --subject <symbol>`")
    lines.append("")
    for subject in sorted(by_subject.keys()):
        safe_subject = re.sub(r"[^a-zA-Z0-9_\-一-鿿]", "_", subject)
        lines.append(f"- [{subject}](_subjects/{safe_subject}.md) ({len(by_subject[subject])} note(s))")

    INDEX_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"✓ reindex done:")
    print(f"  - _index.md ({len(notes)} notes)")
    print(f"  - _topics/ ({len(by_topic)} topics)")
    print(f"  - _subjects/ ({len(by_subject)} subjects)")
    return 0

# ────────────────────────────────────────────────────────────────────────
# argparse
# ────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="SharedNotes — 共同學習筆記 CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="完整 spec 見 docs/Plan/Plan_SharedNotes_Framework.md"
    )
    sp = parser.add_subparsers(dest="cmd", required=True)

    p_add = sp.add_parser("add", help="寫一筆 note")
    p_add.add_argument("--title", required=True)
    p_add.add_argument("--author", required=True, help="persona codename (e.g. basecamp)")
    p_add.add_argument("--author-agent", default=None)
    p_add.add_argument("--note-type", default="concept", choices=NOTE_TYPES,
                       help="WorkNotes v2 雙軸之一: map(在哪)/concept(怎麼運作)/howto(SOP)/decision(為何)/runbook(救火)")
    p_add.add_argument("--supersedes", default=None,
                       help="fork 紀律: 舊 note id — 只在『理解被顛覆/實質加深』才填(舊版標 superseded 不刪); 小修請直接改原卡")
    p_add.add_argument("--topics", default="", help="csv (e.g. ui-architecture,cmd-system)")
    p_add.add_argument("--subjects", default="", help="★ csv code symbols (e.g. RCG_MainMenu,Cmd_UIInspect)")
    p_add.add_argument("--tags", default="", help="csv")
    p_add.add_argument("--related-notes", default="", help="csv note ids")
    p_add.add_argument("--body", default=None, help="inline body markdown")
    p_add.add_argument("--body-file", default=None, help="body markdown file path")
    p_add.add_argument("--slug", default=None, help="自定 slug (default: 從 title 推)")
    p_add.add_argument("--visibility", default="public", choices=["public", "persona-private"])
    p_add.set_defaults(func=cmd_add)

    p_show = sp.add_parser("show", help="印整篇 note")
    p_show.add_argument("--id", required=True)
    p_show.set_defaults(func=cmd_show)

    p_list = sp.add_parser("list", help="列 notes")
    p_list.add_argument("--author", default=None)
    p_list.add_argument("--topic", default=None)
    p_list.add_argument("--subject", default=None)
    p_list.add_argument("--tag", default=None)
    p_list.add_argument("--since", default=None, help="YYYY-MM-DD")
    p_list.add_argument("--status", default=None)
    p_list.set_defaults(func=cmd_list)

    p_search = sp.add_parser("search", help="全文搜尋")
    p_search.add_argument("--query", required=True)
    p_search.set_defaults(func=cmd_search)

    p_find = sp.add_parser("find-related", help="★ 按 subject (code symbol) 精準查詢相關 notes")
    p_find.add_argument("--subject", required=True, help="code symbol / system name (e.g. RCG_MainMenu)")
    p_find.set_defaults(func=cmd_find_related)

    p_onboard = sp.add_parser("onboard", help="★★ 接手殺手鐧: 給 subject/topic 回建議閱讀順序 (見林先於見樹)")
    p_onboard.add_argument("--subject", default=None, help="code symbol / 子系統 (e.g. Cmd_Tavern)")
    p_onboard.add_argument("--topic", default=None, help="topic (e.g. cmd-system) — 與 --subject 擇一")
    p_onboard.set_defaults(func=cmd_onboard)

    p_comment = sp.add_parser("append-comment", help="其他 persona 對某 note 補注")
    p_comment.add_argument("--id", required=True)
    p_comment.add_argument("--author", required=True)
    p_comment.add_argument("--body", required=True)
    p_comment.set_defaults(func=cmd_append_comment)

    p_reindex = sp.add_parser("reindex", help="重建 _index.md + _topics/ + _subjects/")
    p_reindex.set_defaults(func=cmd_reindex)

    args = parser.parse_args()
    return args.func(args)

if __name__ == "__main__":
    sys.exit(main() or 0)
