# 區塊職責：同事在線狀態快照（presence snapshot）— per-viewer 的「我上次看到誰在線」
# 物理意義：
#   online 事實源 = _session/_persona_*.json lock 檔（2026-07-31 拍板「online 判定統一走 lock」，
#   registry.status 只是快取）。本模組不發明第二個判定，只讀 lock 檔名集合。
#   快照 = 某個 viewer persona 上次觀測到的 online 集合；diff = 這段期間誰上線/下線。
# 消費端（同一前提共用同一判準 — 別在各入口各抄一份）：
#   - Tools/tavern_catchup.py：每次讀酒館訊息時 diff → 印區塊 + 寫 viewer inbox + 更新快照
#   - wake_brief（早安在線區塊，basecamp 施工中）：可直接 import 本模組取 current/diff
# 數值影響：
#   唯一寫檔是 ChatTavern/_presence_snapshot/<viewer>.json 與 rooms/<room>/inbox/<viewer>.md（append）。
#   首次無快照 → 只建檔不進 inbox（避免第一次跑就把「全員上線」灌成假變動）。
# 設計取捨：
#   - per-viewer 快照（跟 _inbox_cursor 同構）：gura 看過的變動 ≠ kaguya 看過的（隔離）。
#   - lock 檔存在即 online，不看 expires_at —— 過期 lock 不自動豁免是 awakening 端拍板，
#     這裡跟隨同一語意，避免兩處各自定義「在線」。

from __future__ import annotations

import glob
import json
import os
from datetime import datetime, timezone, timedelta

from . import tavern_paths as _tp

_TZ_LOCAL = timezone(timedelta(hours=8))  # 顯示用 +08，對齊 inbox 既有條目

_SNAPSHOT_DIRNAME = "_presence_snapshot"
_LOCK_PREFIX = "_persona_"


def _chattavern_root() -> str:
    # tavern_paths 的 room dir 形如 <data>/ChatTavern/rooms/<id> — 往上兩層即 ChatTavern 根
    return str(_tp.get_room_dir("tavern").parent.parent)


def _session_dir() -> str:
    # _session 跟 ChatTavern 同層（<data>/AgentCommands/_session）
    return os.path.join(os.path.dirname(_chattavern_root()), "_session")


def snapshot_path(viewer: str) -> str:
    return os.path.join(_chattavern_root(), _SNAPSHOT_DIRNAME, f"{viewer}.json")


def current_online() -> set[str]:
    """讀 _session/_persona_*.json 檔名集合 = 當前在線 persona（lock 即 online）。"""
    pattern = os.path.join(_session_dir(), f"{_LOCK_PREFIX}*.json")
    result = set()
    for p in glob.glob(pattern):
        name = os.path.basename(p)[len(_LOCK_PREFIX):-len(".json")]
        if name:
            result.add(name)
    return result


def load_snapshot(viewer: str) -> dict | None:
    """回 {"taken_at": iso, "online": [..]}；無快照或壞檔回 None（呼叫端視為首次）。"""
    try:
        with open(snapshot_path(viewer), encoding="utf-8") as f:
            d = json.load(f)
        if isinstance(d.get("online"), list):
            return d
    except (OSError, json.JSONDecodeError):
        pass
    return None


def save_snapshot(viewer: str, online: set[str]) -> None:
    path = snapshot_path(viewer)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = {
        "taken_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        "online": sorted(online),
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def diff_and_update(viewer: str) -> dict:
    """
    比對 viewer 快照 vs 當前 lock 狀態，更新快照，回傳：
      {"first_time": bool, "online": [..], "came": [..], "left": [..], "since": iso|None}
    first_time=True 表示原本沒快照（came/left 為空 — 別把初建當變動）。
    """
    now_online = current_online()
    prev = load_snapshot(viewer)
    save_snapshot(viewer, now_online)
    if prev is None:
        return {"first_time": True, "online": sorted(now_online), "came": [], "left": [], "since": None}
    prev_online = set(prev.get("online", []))
    return {
        "first_time": False,
        "online": sorted(now_online),
        "came": sorted(now_online - prev_online),
        "left": sorted(prev_online - now_online),
        "since": prev.get("taken_at"),
    }


def append_presence_inbox(viewer: str, came: list[str], left: list[str],
                          since: str | None, room_id: str = "tavern") -> str:
    """把上下線變動 append 進 rooms/<room>/inbox/<viewer>.md（格式對齊既有 '## ' 條目）。回寫入路徑。"""
    inbox_dir = str(_tp.get_inbox_dir(room_id))
    os.makedirs(inbox_dir, exist_ok=True)
    path = os.path.join(inbox_dir, f"{viewer}.md")
    now_disp = datetime.now(_TZ_LOCAL).strftime("%Y-%m-%d %H:%M:%S +08")
    parts = []
    if came:
        parts.append("上線: " + ", ".join(came))
    if left:
        parts.append("下線: " + ", ".join(left))
    since_disp = f"（自上次快照 {since}）" if since else ""
    entry = (
        f"\n## [presence] 📡 同事狀態變動 ({now_disp})\n\n"
        f"> {' ／ '.join(parts)}{since_disp}\n\n"
        f"（presence snapshot 自動 diff — lock 檔為事實源）\n"
    )
    with open(path, "a", encoding="utf-8") as f:
        f.write(entry)
    return path
