#!/usr/bin/env python3
"""debuglog_query.py — DebugLog 結構化查詢 MVP (T03, 2026-05-16 basecamp).

# 區塊職責：給 agent 一個結構化 + 過濾噪音的 DebugLog 查詢工具，避免每次
#          手動 grep 4 個 log 檔被 spine warning / CS0XXX / asset processor 淹沒。
# 物理意義：純 file system 讀取，不依賴 Unity Editor state；自動找最新 log,
#          內建噪音過濾，輸出結構化 markdown 給 agent 讀。
# 數值影響：read-only, 不寫 log/不改檔, 對運行系統零副作用。

設計依據: docs/Plan/Plan_Cmd_DebugLog_Design.md

三個 MVP op:
  tail       — 看最新 N 行 (過濾噪音後)
  component  — 撈特定 [TagName] 組件 trace (如 DiscordInbound / Tavern)
  errors     — 純 ERROR + 重要 WARNING

預設過濾噪音 (--exclude-noise=false 可關掉):
  - Spine / Premultiply alpha / Texture warning
  - CS0XXX compile warnings
  - RCG_AssetModificationProcessor OnWillSaveAssets
  - Build asset version error SourceAssetDB

使用範例:
  python debuglog_query.py tail --limit 30
  python debuglog_query.py component --tag DiscordInbound
  python debuglog_query.py errors --since 10:30
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Windows console cp950 → UTF-8 避免中文印錯
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = Path(__file__).resolve().parent
# 推斷 project root: tools 通常在 AgentCommands/Tools/, repo 為其 parent.parent
REPO_ROOT = HERE.parent.parent
# T-PATH-02: DebugLogs 布局 per-project — LY 在 repo root/DebugLogs, CardGame 在 CardGame/Assets/DebugLogs。
# 取第一個實際存在的候選; 都不在則退回 repo root/DebugLogs (由 caller 報清楚的路徑)。
DEBUG_LOG_DIR = next(
    (c for c in (
        REPO_ROOT / "DebugLogs",
        REPO_ROOT / "CardGame" / "Assets" / "DebugLogs",
        REPO_ROOT / "Assets" / "DebugLogs",
    ) if c.is_dir()),
    REPO_ROOT / "DebugLogs",
)

# 區塊職責：噪音過濾 regex
# 物理意義：這些 pattern 命中 = log line 視為「不感興趣的固定噪音」, 預設過濾掉
# 數值影響：可用 --exclude-noise=false 關掉; --noise-extra 加自訂
NOISE_PATTERNS = [
    re.compile(r"`?Assets/Sprites/Units/.*\.png`?\s*:\s*Problematic Texture"),
    re.compile(r"Premultiply alpha|Straight Alpha Texture|Generate Mip Maps|sRGB \(Color Texture\)"),
    re.compile(r"warning CS\d{4}:"),
    re.compile(r"RCG_AssetModificationProcessor.*OnWillSaveAssets"),
    re.compile(r"Build asset version error.*SourceAssetDB"),
    re.compile(r"Import Error Code:\(4\)"),
    re.compile(r"\(You can disable this warning in `Edit - Preferences - Spine`\)"),
]

# 區塊職責：Log 行的時間戳 + level 解析 regex
# 物理意義：DebugLogs/*.log 行格式為 "N.[LEVEL][HH:MM:SS] body" — 解出三欄
ENTRY_RE = re.compile(r"^(?P<num>\d+)\.\[(?P<level>WARNING|ERROR|INFO|LOG)\]\[(?P<time>\d{2}:\d{2}:\d{2})\]\s+(?P<body>.*)$")


def find_logs(session: str = "latest"):
    """找出 log 檔案路徑.

    Args:
        session: 'latest' / 'previous' / 'all_recent_3' / 具體檔名

    Returns:
        list[Path] — 排序後（newest first）的 log 檔
    """
    if not DEBUG_LOG_DIR.exists():
        return []
    all_logs = sorted(
        [p for p in DEBUG_LOG_DIR.glob("Simulation_*.log") if not p.name.endswith(".meta")],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not all_logs:
        return []
    if session == "latest":
        return all_logs[:1]
    if session == "previous":
        return all_logs[1:2] if len(all_logs) >= 2 else []
    if session.startswith("all_recent_"):
        try:
            n = int(session.split("_")[-1])
            return all_logs[:n]
        except ValueError:
            return all_logs[:3]
    # 具體檔名
    for p in all_logs:
        if p.name == session:
            return [p]
    return []


def parse_time(s: str) -> Optional[int]:
    """HH:MM 或 HH:MM:SS → 當天 0 點起的秒數. Return None if 解析失敗."""
    parts = s.split(":")
    if len(parts) < 2 or len(parts) > 3:
        return None
    try:
        h = int(parts[0])
        m = int(parts[1])
        sec = int(parts[2]) if len(parts) == 3 else 0
        return h * 3600 + m * 60 + sec
    except ValueError:
        return None


def is_noise(line: str, extra_patterns=None) -> bool:
    """判斷單行 log 是否為噪音 (預設 patterns + 額外 patterns)."""
    for p in NOISE_PATTERNS:
        if p.search(line):
            return True
    if extra_patterns:
        for p in extra_patterns:
            if p.search(line):
                return True
    return False


def read_log_entries(log_path: Path, exclude_noise: bool = True, noise_extra=None):
    """讀 log 檔案, 每筆 entry 一個 dict.

    Entry schema:
        {
            'num': int, 'level': str, 'time': 'HH:MM:SS',
            'body': str (multi-line continuation also joined),
            'raw': str (整個原始片段),
        }

    處理 multi-line continuation: 一筆 entry 從 ENTRY_RE 開始, 後續不符合 ENTRY_RE
    的行視為前一筆的續行 (stacktrace / message body 換行).
    """
    if not log_path.exists():
        return []
    try:
        with log_path.open("r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except OSError:
        return []

    entries = []
    current = None
    extra_patterns = [re.compile(p) for p in (noise_extra or [])]

    for line in lines:
        m = ENTRY_RE.match(line)
        if m:
            # 新 entry 開始, push 前一筆
            if current is not None:
                entries.append(current)
            current = {
                "num": int(m.group("num")),
                "level": m.group("level"),
                "time": m.group("time"),
                "body": m.group("body"),
                "raw": line.rstrip("\n"),
            }
        else:
            # Continuation line
            if current is not None:
                current["body"] += "\n" + line.rstrip("\n")
                current["raw"] += "\n" + line.rstrip("\n")

    if current is not None:
        entries.append(current)

    if exclude_noise:
        entries = [e for e in entries if not is_noise(e["raw"], extra_patterns)]

    return entries


def filter_by_time(entries, since: Optional[int], until: Optional[int]):
    """按時間範圍過濾 (since/until 為當天秒數)."""
    if since is None and until is None:
        return entries
    out = []
    for e in entries:
        t = parse_time(e["time"])
        if t is None:
            continue
        if since is not None and t < since:
            continue
        if until is not None and t > until:
            continue
        out.append(e)
    return out


def _tag_variants(tag: str):
    """產生 tag 的常見命名變體 (CamelCase ↔ kebab-case ↔ snake_case ↔ lowercase).

    例: 'DiscordInbound' → ['DiscordInbound', 'discord-inbound', 'discord_inbound', 'discordinbound']

    為何: Tim 2026-05-16 看到的 log 同時有 [DiscordInbound] (C# 端) 跟 [discord-inbound] (Python 端).
    使用者輸入單一 tag 應能 match 任何變體, 否則跨層 daemon trace 漏抓.
    """
    seen = {tag}
    variants = [tag]
    # CamelCase → kebab-case (DiscordInbound → discord-inbound)
    kebab = re.sub(r'(?<!^)(?=[A-Z])', '-', tag).lower()
    if kebab not in seen:
        seen.add(kebab)
        variants.append(kebab)
    # CamelCase → snake_case
    snake = kebab.replace('-', '_')
    if snake not in seen:
        seen.add(snake)
        variants.append(snake)
    # Pure lowercase (no separator)
    lower = tag.lower().replace('-', '').replace('_', '')
    if lower not in seen:
        seen.add(lower)
        variants.append(lower)
    return variants


def filter_by_tag(entries, tag: str):
    """撈含 [Tag] 的 entry. 自動 fallback 嘗試 CamelCase / kebab / snake 變體.

    Case insensitive. 例: tag='DiscordInbound' 也會 match '[discord-inbound]' / '[discord_inbound]'.
    """
    variants = _tag_variants(tag)
    # 組合成 alternation regex: \[(DiscordInbound|discord-inbound|...)\]
    escaped = "|".join(re.escape(v) for v in variants)
    pat = re.compile(r"\[(" + escaped + r")\]", re.IGNORECASE)
    return [e for e in entries if pat.search(e["raw"])]


def filter_by_level(entries, level: str):
    """level: 'WARNING+' / 'ERROR' / 'WARNING' / 'INFO' / 'ALL'."""
    level = level.upper()
    if level == "ALL":
        return entries
    if level == "WARNING+":
        return [e for e in entries if e["level"] in ("WARNING", "ERROR")]
    return [e for e in entries if e["level"] == level]


def format_markdown(entries, log_path: Path, op: str, args_dict: dict, total_scanned: int, total_filtered: int):
    """輸出結構化 markdown 報告."""
    out = []
    args_str = ", ".join(f"{k}={v}" for k, v in args_dict.items() if v is not None)
    out.append(f"=== Cmd_DebugLog ({op}, {args_str}) ===")
    out.append(f"Session: {log_path.name}")
    try:
        mtime = datetime.fromtimestamp(log_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        out.append(f"Last modified: {mtime}")
    except OSError:
        pass
    out.append("")
    out.append("## Meta")
    out.append(f"- Total entries scanned: {total_scanned}")
    out.append(f"- Filtered out (noise): {total_scanned - total_filtered}")
    out.append(f"- Matches: {len(entries)}")
    out.append("")

    if not entries:
        out.append("## Matches: 0")
        out.append("")
        out.append("⚠ No matches found. Possible reasons:")
        out.append("- Component / pattern truly absent (e.g. daemon didn't load)")
        out.append("- Filter too narrow (try --exclude-noise=false)")
        out.append("- Wrong session (try --session previous or all_recent_3)")
        return "\n".join(out)

    out.append("## Matches")
    out.append("")
    for e in entries:
        out.append(f"### [{e['time']}] {e['level']}")
        # body 印前 500 字, 太長截斷
        body = e["body"]
        if len(body) > 500:
            body = body[:500] + "\n    ... (truncated)"
        out.append("```")
        out.append(body)
        out.append("```")
        out.append("")
    return "\n".join(out)


# ===========================================================
# Ops
# ===========================================================

def cmd_tail(args):
    logs = find_logs(args.session)
    if not logs:
        print("ERROR: no logs found")
        return 1
    log = logs[0]
    all_entries = read_log_entries(log, exclude_noise=args.exclude_noise, noise_extra=args.noise_extra)
    total_scanned = len(read_log_entries(log, exclude_noise=False))
    entries = all_entries[-args.limit:] if args.limit else all_entries

    md = format_markdown(
        entries, log, "tail",
        {"session": args.session, "limit": args.limit, "exclude_noise": args.exclude_noise},
        total_scanned, len(all_entries),
    )
    print(md)
    return 0


def cmd_component(args):
    logs = find_logs(args.session)
    if not logs:
        print("ERROR: no logs found")
        return 1

    all_matched = []
    total_scanned = 0
    total_filtered = 0
    for log in logs:
        entries = read_log_entries(log, exclude_noise=args.exclude_noise, noise_extra=args.noise_extra)
        total_scanned += len(read_log_entries(log, exclude_noise=False))
        total_filtered += len(entries)
        matched = filter_by_tag(entries, args.tag)
        for e in matched:
            e["_source_log"] = log.name
        all_matched.extend(matched)

    all_matched = all_matched[:args.limit] if args.limit else all_matched

    # 多 log 輸出時, 顯示 source
    log_display = logs[0] if len(logs) == 1 else logs[0]
    md = format_markdown(
        all_matched, log_display, "component",
        {"session": args.session, "tag": args.tag, "limit": args.limit},
        total_scanned, total_filtered,
    )
    if len(logs) > 1:
        md = md.replace(f"Session: {logs[0].name}", f"Searched {len(logs)} logs (latest: {logs[0].name})")
    # Diagnostic hints
    if not all_matched and args.tag:
        md += "\n\n## Diagnostic Hints\n"
        md += f"- 完全沒看到 [{args.tag}] tag — 可能該組件未載入 / 編譯失敗 / 從未啟動\n"
        md += f"- 嘗試 --session all_recent_3 跨多 session 搜尋\n"
        md += f"- 嘗試 --exclude-noise=false 看是否被誤過濾\n"
    print(md)
    return 0


def cmd_errors(args):
    logs = find_logs(args.session)
    if not logs:
        print("ERROR: no logs found")
        return 1
    log = logs[0]
    all_entries = read_log_entries(log, exclude_noise=args.exclude_noise, noise_extra=args.noise_extra)
    total_scanned = len(read_log_entries(log, exclude_noise=False))

    # ERROR + WARNING (不分 plus/single)
    filtered = filter_by_level(all_entries, "WARNING+")
    since_sec = parse_time(args.since) if args.since else None
    until_sec = parse_time(args.until) if args.until else None
    filtered = filter_by_time(filtered, since_sec, until_sec)
    filtered = filtered[-args.limit:] if args.limit else filtered

    md = format_markdown(
        filtered, log, "errors",
        {"session": args.session, "since": args.since, "until": args.until, "limit": args.limit},
        total_scanned, len(all_entries),
    )
    print(md)
    return 0


def cmd_search(args):
    """op=search: 跨 session 用 regex 搜尋 log entries.

    用途: 找特定 error message / pattern across 多個 session, 不限定 tag 格式.
    跟 op=component 差別: component 限定 [Tag] 包裝, search 接任意 regex.
    """
    logs = find_logs(args.session)
    if not logs:
        print("ERROR: no logs found")
        return 1

    try:
        pat = re.compile(args.pattern, re.IGNORECASE if args.case_insensitive else 0)
    except re.error as e:
        print(f"ERROR: invalid regex pattern: {e}")
        return 1

    all_matched = []
    total_scanned = 0
    total_filtered = 0
    for log in logs:
        entries = read_log_entries(log, exclude_noise=args.exclude_noise, noise_extra=args.noise_extra)
        total_scanned += len(read_log_entries(log, exclude_noise=False))
        total_filtered += len(entries)
        for e in entries:
            if pat.search(e["raw"]):
                e["_source_log"] = log.name
                all_matched.append(e)

    # 時間範圍過濾 (optional)
    since_sec = parse_time(args.since) if args.since else None
    until_sec = parse_time(args.until) if args.until else None
    all_matched = filter_by_time(all_matched, since_sec, until_sec)
    # Level 過濾 (optional)
    if args.level and args.level.upper() != "ALL":
        all_matched = filter_by_level(all_matched, args.level)

    all_matched = all_matched[:args.limit] if args.limit else all_matched

    log_display = logs[0]
    md = format_markdown(
        all_matched, log_display, "search",
        {"pattern": args.pattern, "session": args.session, "level": args.level,
         "since": args.since, "until": args.until, "limit": args.limit},
        total_scanned, total_filtered,
    )
    if len(logs) > 1:
        md = md.replace(f"Session: {logs[0].name}", f"Searched {len(logs)} logs (latest: {logs[0].name})")
    if not all_matched:
        md += "\n\n## Diagnostic Hints\n"
        md += f"- pattern `{args.pattern}` 在 {len(logs)} 個 session 都沒命中\n"
        md += f"- 嘗試 --case-insensitive 或拓展 regex (e.g. `.*foo.*`)\n"
        md += f"- 嘗試 --exclude-noise=false 看是否被誤過濾掉了\n"
        md += f"- 嘗試 --session all_recent_5 / all_recent_10 擴大範圍\n"
    print(md)
    return 0


def cmd_summary(args):
    """op=summary: 一個 log 的健康度概覽 — 各組件出現次數 / 噪音佔比 / 錯誤統計.

    用途: 快速判斷 Editor session 整體狀態, 看哪些 daemon 在跑 / 哪些缺席.
    """
    logs = find_logs(args.session)
    if not logs:
        print("ERROR: no logs found")
        return 1
    log = logs[0]

    all_entries = read_log_entries(log, exclude_noise=False)  # 不過濾, 算噪音比例
    noise_entries = [e for e in all_entries if is_noise(e["raw"])]
    clean_entries = [e for e in all_entries if not is_noise(e["raw"])]

    # 從 clean entries 統計各組件出現次數
    # Tag 提取 regex: 抓 [Tag] 開頭 (entry body 第一個方括號)
    # T07: 加 hyphen 支援抓 [discord-inbound] 之類 kebab-case tag
    tag_pat = re.compile(r"\[([A-Za-z_][A-Za-z0-9_-]*)\]")
    component_counts = {}
    component_last_seen = {}
    for e in clean_entries:
        # 抓 body 內第一個 [Tag] (跳過 [WARNING][HH:MM:SS] 那兩個已被 entry_re 消化掉)
        body = e["body"]
        m = tag_pat.search(body)
        if m:
            tag = m.group(1)
            component_counts[tag] = component_counts.get(tag, 0) + 1
            component_last_seen[tag] = e["time"]

    # Level 統計
    level_counts = {"INFO": 0, "WARNING": 0, "ERROR": 0, "LOG": 0}
    for e in clean_entries:
        level_counts[e["level"]] = level_counts.get(e["level"], 0) + 1

    # 編譯 warning 統計 (CS\d{4})
    cs_warning_count = sum(1 for e in all_entries if re.search(r"warning CS\d{4}:", e["raw"]))

    # 預期應出現的 daemon tags
    expected_daemons = ["DiscordInbound", "Tavern", "LoginStatus", "BartenderDaemon", "AgentSkillManager", "UCL_AgentCmd"]
    missing_daemons = [d for d in expected_daemons if d not in component_counts]
    present_daemons = [d for d in expected_daemons if d in component_counts]

    # 輸出
    out = []
    out.append(f"=== Cmd_DebugLog summary (session={args.session}) ===")
    out.append(f"Session: {log.name}")
    try:
        mtime = datetime.fromtimestamp(log.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        out.append(f"Last modified: {mtime}")
    except OSError:
        pass
    out.append("")
    out.append(f"## Totals")
    out.append(f"- Total entries: {len(all_entries)}")
    out.append(f"- Noise (auto-filtered): {len(noise_entries)} ({len(noise_entries) * 100 // max(1, len(all_entries))}%)")
    out.append(f"- Signal (non-noise): {len(clean_entries)}")
    out.append(f"- Compile warnings (CS####): {cs_warning_count}")
    out.append("")
    out.append("## Level breakdown (non-noise)")
    for lv, cnt in level_counts.items():
        if cnt > 0:
            out.append(f"- {lv}: {cnt}")
    out.append("")
    out.append("## Components seen")
    if component_counts:
        # 排序 by count desc
        sorted_comps = sorted(component_counts.items(), key=lambda x: -x[1])
        for tag, cnt in sorted_comps[:20]:
            last = component_last_seen.get(tag, "?")
            out.append(f"- [{tag}]: {cnt} entries (last @ {last})")
    else:
        out.append("- (none — non-noise entries 沒有 [Tag] 開頭格式)")
    out.append("")
    out.append("## Expected daemons health check")
    if present_daemons:
        out.append(f"- ✅ Present: {', '.join(present_daemons)}")
    if missing_daemons:
        out.append(f"- ⚠ Missing: {', '.join(missing_daemons)}")
        out.append(f"  → 這些 daemon 預期該在 Editor 啟動時印 log. 缺席 = 可能編譯失敗 / 未載入 / 被 disabled")
    out.append("")
    out.append("## Quick suggested next steps")
    if missing_daemons:
        out.append(f"- 跑 `debuglog_query component --tag {missing_daemons[0]} --session all_recent_3` 確認跨 session 都缺")
    if level_counts.get("ERROR", 0) > 0:
        out.append(f"- 跑 `debuglog_query errors --session {args.session}` 看 {level_counts['ERROR']} 條 ERROR 細節")
    if cs_warning_count > 50:
        out.append(f"- 大量 compile warning ({cs_warning_count} 條) — 可能需 .csproj cleanup")
    print("\n".join(out))
    return 0


# ===========================================================
# Main
# ===========================================================

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="op", required=True)

    # tail
    p_tail = sub.add_parser("tail", help="看最新 N 條 (過濾噪音後)")
    p_tail.add_argument("--session", default="latest", help="latest / previous / all_recent_3 / <filename>")
    p_tail.add_argument("--limit", type=int, default=30, help="最多回 N 條")
    p_tail.add_argument("--exclude-noise", type=lambda x: x.lower() != "false", default=True)
    p_tail.add_argument("--noise-extra", nargs="*", default=None, help="額外噪音 regex")
    p_tail.set_defaults(func=cmd_tail)

    # component
    p_comp = sub.add_parser("component", help="撈 [TagName] 組件 trace")
    p_comp.add_argument("--tag", required=True, help="組件 tag (auto-wrap []), 如 DiscordInbound")
    p_comp.add_argument("--session", default="latest", help="預設 latest, 可加 all_recent_3")
    p_comp.add_argument("--limit", type=int, default=50)
    p_comp.add_argument("--exclude-noise", type=lambda x: x.lower() != "false", default=True)
    p_comp.add_argument("--noise-extra", nargs="*", default=None)
    p_comp.set_defaults(func=cmd_component)

    # errors
    p_err = sub.add_parser("errors", help="純 ERROR + WARNING (過濾噪音後)")
    p_err.add_argument("--session", default="latest")
    p_err.add_argument("--since", default=None, help="HH:MM 或 HH:MM:SS 起點")
    p_err.add_argument("--until", default=None, help="HH:MM 或 HH:MM:SS 終點")
    p_err.add_argument("--limit", type=int, default=50)
    p_err.add_argument("--exclude-noise", type=lambda x: x.lower() != "false", default=True)
    p_err.add_argument("--noise-extra", nargs="*", default=None)
    p_err.set_defaults(func=cmd_errors)

    # search (T06 v2 add)
    p_search = sub.add_parser("search", help="跨 session 用 regex 搜尋 (比 component 自由)")
    p_search.add_argument("--pattern", required=True, help="regex pattern (e.g. 'discord|inbound|404')")
    p_search.add_argument("--session", default="latest", help="latest / previous / all_recent_N / <filename>")
    p_search.add_argument("--case-insensitive", action="store_true", default=False)
    p_search.add_argument("--level", default="ALL", help="ALL / WARNING+ / ERROR / WARNING / INFO")
    p_search.add_argument("--since", default=None)
    p_search.add_argument("--until", default=None)
    p_search.add_argument("--limit", type=int, default=50)
    p_search.add_argument("--exclude-noise", type=lambda x: x.lower() != "false", default=True)
    p_search.add_argument("--noise-extra", nargs="*", default=None)
    p_search.set_defaults(func=cmd_search)

    # summary (T06 v2 add)
    p_sum = sub.add_parser("summary", help="一個 log 的健康度概覽")
    p_sum.add_argument("--session", default="latest")
    p_sum.set_defaults(func=cmd_summary)

    args = p.parse_args()
    rc = args.func(args)
    sys.exit(rc or 0)


if __name__ == "__main__":
    main()
