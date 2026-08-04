"""Tavern read-only IO helpers — Python 端讀 jsonl / json / md 的統一封裝.

設計原則：**read-only**。寫入操作一律走 Cmd_Tavern op=post / op=task_X 等
（見 tavern_client.py 即將 ship 的 SDK），不在這 module 內。

API 對應 C# UCL_ChatTavernIO / UCL_ChatTavernQuestIO 的 reader 函式：
    LoadAllMessages / Tail / LoadAllEvents / LoadIdentities / LoadPresence

Robustness：
- partial-line skip (jsonl 行尾 \n 不完整 → 跳過 silent)
- bad-line skip (json.loads 失敗 → 跳過記入 bad_lines list 給 caller 看)
- utf-8 errors='replace' 兜底（防 cp950 / big5 寫入污染）
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator

from . import tavern_paths as _tp


# ---------------------------------------------------------------------------
# messages.jsonl
# ---------------------------------------------------------------------------

def read_messages(room_id: str) -> list[dict]:
    """讀整個房間 messages — T38 改 walk per-msg file dir + ts sort + derive seq.

    Mirror of C# UCL_ChatTavernIO_PerMsgFile.LoadAllMessages.
    結構：rooms/<room>/messages/<YYYY-MM-DD>/<HHMMSS>_<MMM>_<UUID6>.json
    """
    base = _tp.get_room_dir(room_id) / "messages"
    if not base.is_dir():
        return []
    # 字典序 sort = 時間 sort（filename ts prefix 設計）
    files = sorted(base.rglob("*.json"))
    out = []
    for i, f in enumerate(files, start=1):
        try:
            rec = json.loads(f.read_text(encoding="utf-8"))
            rec["seq"] = i   # derive
            out.append(rec)
        except Exception:
            continue   # silent skip bad files
    return out


def read_messages_with_bad_lines(room_id: str) -> tuple[list[dict], list[tuple[int, str, str]]]:
    """讀整個房間 messages + bad_lines list（per-msg file 結構下 bad_lines = file paths that failed parse）。

    回 (records, bad_lines) where bad_lines = [(file_index, file_name[:120], error_msg[:100]), ...].
    """
    base = _tp.get_room_dir(room_id) / "messages"
    if not base.is_dir():
        return [], []
    files = sorted(base.rglob("*.json"))
    out = []
    bad = []
    for i, f in enumerate(files, start=1):
        try:
            rec = json.loads(f.read_text(encoding="utf-8"))
            rec["seq"] = i
            out.append(rec)
        except Exception as e:
            bad.append((i, f.name[:120], str(e)[:100]))
    return out, bad


def iter_messages_since(room_id: str, since_seq: int) -> Iterator[dict]:
    """Streaming 讀房間 messages — yield seq > since_seq 的 record。

    T38: per-msg file 結構下，遍歷檔案順序就是 ts 順序（filename 字典序）。
    """
    base = _tp.get_room_dir(room_id) / "messages"
    if not base.is_dir():
        return
    files = sorted(base.rglob("*.json"))
    for i, f in enumerate(files, start=1):
        if i <= since_seq:
            continue
        try:
            rec = json.loads(f.read_text(encoding="utf-8"))
            rec["seq"] = i
            yield rec
        except Exception:
            continue


def iter_messages_since_ts(room_id: str, since_ts: str) -> Iterator[dict]:
    """T38 NEW — yield ts > since_ts 的 record（推薦用 ts-based 比 seq-based 更穩定）.

    since_ts: ISO 8601 string e.g. "2026-05-09T08:47:52.312Z"
    """
    base = _tp.get_room_dir(room_id) / "messages"
    if not base.is_dir():
        return
    files = sorted(base.rglob("*.json"))
    for i, f in enumerate(files, start=1):
        try:
            rec = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        ts = rec.get("ts", "")
        if ts > since_ts:
            rec["seq"] = i
            yield rec


def tail_messages(room_id: str, n: int) -> list[dict]:
    """讀最後 n 筆 message — 對應 C# Tail。

    Caveat: 簡單版讀整檔取 tail；房間訊息上萬筆要改 reverse-scan。
    """
    all_msgs = read_messages(room_id)
    if len(all_msgs) <= n:
        return all_msgs
    return all_msgs[-n:]


# ---------------------------------------------------------------------------
# events.jsonl (quest task lifecycle)
# ---------------------------------------------------------------------------

def read_events(room_id: str) -> list[dict]:
    """讀整個 events.jsonl；partial-line / bad-line silent skip。

    Mirror of C# UCL_ChatTavernQuestIO.LoadAllEvents。
    """
    base = _tp.get_room_dir(room_id) / "events"
    if not base.is_dir():
        return []
    files = sorted(base.rglob("*.json"))
    out = []
    for i, f in enumerate(files, start=1):
        try:
            rec = json.loads(f.read_text(encoding="utf-8"))
            rec["seq"] = i
            out.append(rec)
        except Exception:
            continue
    return out


def read_events_with_source_tag(room_id: str) -> list[dict]:
    """讀 events.jsonl 且每筆加 _source_room 欄位 — 給 notify_discord 跨房合流用。"""
    out = read_events(room_id)
    for r in out:
        r["_source_room"] = room_id
    return out


# ---------------------------------------------------------------------------
# identities.json / presence.json (top-level metadata)
# ---------------------------------------------------------------------------

def read_identities() -> dict[str, dict]:
    """讀 chat_tavern/identities.json；回 dict {id: identity_dict}；失敗回 {}.

    Mirror of C# UCL_ChatTavernIO.LoadIdentities（屬於 model class，本函式只回 raw dict）。
    """
    p = _tp.IDENTITIES_PATH
    if not p.is_file():
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        result: dict[str, dict] = {}
        for row in data.get("identities", []) or []:
            iid = row.get("id")
            if iid:
                result[iid] = row
        return result
    except Exception:
        return {}


def read_room_meta(room_id: str) -> dict:
    """讀 rooms/<room>/meta.json；找不到 / 解析失敗回 {}.

    Mirror of C# UCL_ChatTavernIO.LoadRoomMeta（簡化 — 不做 cache，每次重讀）。
    """
    p = _tp.get_room_meta_path(room_id)
    if not p.is_file():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def read_inbox(room_id: str, agent_id: str) -> str:
    """讀 rooms/<room>/inbox/<agent>.md；找不到回空字串."""
    p = _tp.get_inbox_path(room_id, agent_id)
    if not p.is_file():
        return ""
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# Internal helpers — jsonl readers
# ---------------------------------------------------------------------------

def _read_jsonl(p: Path) -> list[dict]:
    """讀整個 jsonl；partial-line / bad-line silent skip。

    讀法跟 notify_discord _read_room_messages 一致：raw bytes → utf-8 errors='replace'
    → split by \n → json.loads per line（壞行 silent skip）。
    """
    if not p.is_file():
        return []
    out: list[dict] = []
    try:
        raw = p.read_bytes()
        text = raw.decode("utf-8", errors="replace")
        idx = 0
        while idx < len(text):
            nl = text.find("\n", idx)
            if nl < 0:
                break
            line = text[idx:nl]
            idx = nl + 1
            if not line.strip():
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    except Exception:
        return out
    return out


def _read_jsonl_with_diagnostics(p: Path) -> tuple[list[dict], list[tuple[int, str, str]]]:
    """版本 with bad_lines list — 給 messages_dedupe 用（caller 想知道哪些行壞）。"""
    if not p.is_file():
        return [], []
    out: list[dict] = []
    bad_lines: list[tuple[int, str, str]] = []
    try:
        raw = p.read_bytes().decode("utf-8", errors="replace")
        for line_no, line in enumerate(raw.splitlines(), start=1):
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except Exception as e:
                bad_lines.append((line_no, line[:120], str(e)[:100]))
    except Exception:
        return out, bad_lines
    return out, bad_lines
