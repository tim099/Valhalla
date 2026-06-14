"""Tavern path constants + helpers — Python 端對應 C# UCL_ChatTavernIO 的 single source of truth.

C# 端集中常數在 UCL_ChatTavernIO.cs（TavernDirRelative / RoomsFile / MessagesFile / SeqFile / etc.）
本 module 提供 Python 版鏡像，給 notify_discord / messages_dedupe / discord_inbound_daemon
等 tool 統一引用，避免散落 hard-code。

Conventions matching C# UCL_ChatTavernIO.cs (line 28-39):
    AgentCommands/ChatTavern/                         <- TavernDirRelative
    AgentCommands/ChatTavern/identities.json          <- IdentitiesFile
    AgentCommands/ChatTavern/presence.json            <- PresenceFile
    AgentCommands/ChatTavern/rooms/<id>/              <- room dir
    AgentCommands/ChatTavern/rooms/<id>/messages.jsonl
    AgentCommands/ChatTavern/rooms/<id>/_seq.txt
    AgentCommands/ChatTavern/rooms/<id>/events.jsonl
    AgentCommands/ChatTavern/rooms/<id>/_events_seq.txt
    AgentCommands/ChatTavern/rooms/<id>/inbox/<agent>.md
    AgentCommands/ChatTavern/rooms/<id>/meta.json     <- per-room metadata
    AgentCommands/ChatTavern/rooms/<id>/notes/<key>.md
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable


# ---------------------------------------------------------------------------
# Repo root resolution
# ---------------------------------------------------------------------------

# 區塊職責：找 repo root（含 .git/ 目錄的最外層 parent）
# 物理意義：本 module 位於 AgentCommands/_lib/，repo root 是 _lib.parent.parent
# 數值影響：固定 2 層回溯，跨平台 / 跨呼叫位置都 stable
def _find_repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


# 區塊職責：T-PATH-01 (2026-05-28) — AgentCommands 資料根 pointer 檔解析
# 物理意義：C# 控制台 Apply 時把絕對資料根寫到 <git-root>/.agentcommands_root.local;
#          本 helper 讀這檔得實際資料根,沒有 → 預設 git_root/AgentCommands (與舊行為相同)。
# 數值影響：跨語言 (C#/Python) 共讀同一檔,per-machine (gitignored);純文字 IO。
def _resolve_agentcommands_data_root(git_root: Path) -> Path:
    pointer = git_root / ".agentcommands_root.local"
    try:
        if pointer.exists():
            content = pointer.read_text(encoding="utf-8").strip()
            if content:
                p = Path(content)
                if p.is_absolute():
                    return p.resolve()
    except Exception:
        pass
    return (git_root / "AgentCommands").resolve()


# 對外暴露的常數 — caller 引用這些而不是自己 hardcode
REPO_ROOT: Path = _find_repo_root()
# AGENT_COMMANDS_DIR = 資料根 (可被 pointer 檔 override;預設 = REPO_ROOT/AgentCommands)
AGENT_COMMANDS_DIR: Path = _resolve_agentcommands_data_root(REPO_ROOT)
TAVERN_DIR: Path = AGENT_COMMANDS_DIR / "ChatTavern"
ROOMS_DIR: Path = TAVERN_DIR / "rooms"

# Per-tavern 全域 metadata（不在 rooms/<id>/ 下）
IDENTITIES_PATH: Path = TAVERN_DIR / "identities.json"
PRESENCE_PATH: Path = TAVERN_DIR / "presence.json"
HANDSHAKE_START_PATH: Path = TAVERN_DIR / "_handshake_start.txt"
LAST_OP_PATH: Path = TAVERN_DIR / "_last_op.md"
ACTIVE_WAITS_PATH: Path = TAVERN_DIR / "_active_waits.json"
BARTENDER_LINES_PATH: Path = TAVERN_DIR / "bartender_lines.json"
BARTENDER_STATE_PATH: Path = TAVERN_DIR / "bartender_state.json"

# PromptQueue 含 scripts (notify_discord.py / notify_treasury.py 等), 跟 RPC queue 一樣留 canonical
# (T-PATH-01 不跟資料搬;與 C# RepoPath.AgentCommandsDir 對齊 — code 永遠錨在 repo)
PROMPT_QUEUE_DIR: Path = REPO_ROOT / "AgentCommands" / "PromptQueue"
NOTIFY_STATE_PATH: Path = PROMPT_QUEUE_DIR / "_notify_state.json"
TAVERN_STATE_PATH: Path = PROMPT_QUEUE_DIR / "_tavern_state.json"
WAKE_STATE_PATH: Path = PROMPT_QUEUE_DIR / "_wake_state.json"
NOTIFY_CONFIG_PATH: Path = PROMPT_QUEUE_DIR / "notify_config.json"


# ---------------------------------------------------------------------------
# Per-room path helpers
# ---------------------------------------------------------------------------

# 區塊職責：對應 C# UCL_ChatTavernIO.GetRoomDir / GetMessagesPath / GetSeqPath / etc.
# 物理意義：room_id → 各種子檔絕對路徑
# 數值影響：純函式，無 IO；呼叫前不檢查存在性（caller 自行判斷 .is_file()）

def get_room_dir(room_id: str) -> Path:
    """Mirror of C# UCL_ChatTavernIO.GetRoomDir(roomId)."""
    return ROOMS_DIR / room_id


def get_messages_path(room_id: str) -> Path:
    """messages.jsonl absolute path — mirror C# GetMessagesPath."""
    return get_room_dir(room_id) / "messages.jsonl"


def get_seq_path(room_id: str) -> Path:
    """_seq.txt absolute path — mirror C# GetSeqPath."""
    return get_room_dir(room_id) / "_seq.txt"


def get_events_path(room_id: str) -> Path:
    """events.jsonl absolute path — mirror C# UCL_ChatTavernQuestIO.GetEventsPath."""
    return get_room_dir(room_id) / "events.jsonl"


def get_events_seq_path(room_id: str) -> Path:
    """_events_seq.txt absolute path."""
    return get_room_dir(room_id) / "_events_seq.txt"


def get_room_meta_path(room_id: str) -> Path:
    """meta.json (per-room metadata) — mirror C# GetRoomMetaPath."""
    return get_room_dir(room_id) / "meta.json"


def get_members_path(room_id: str) -> Path:
    """members.json — mirror C# GetMembersPath."""
    return get_room_dir(room_id) / "members.json"


def get_last_view_path(room_id: str) -> Path:
    """_last_view.md — mirror C# GetLastViewPath."""
    return get_room_dir(room_id) / "_last_view.md"


def get_inbox_dir(room_id: str) -> Path:
    """inbox/ dir for given room."""
    return get_room_dir(room_id) / "inbox"


def get_inbox_path(room_id: str, agent_id: str) -> Path:
    """inbox/<agent_id>.md — mirror C# UCL_ChatTavernQuestIO.GetInboxPath."""
    return get_inbox_dir(room_id) / f"{agent_id}.md"


def get_tasks_dir(room_id: str) -> Path:
    """tasks/ dir for given room (quest spec MD files)."""
    return get_room_dir(room_id) / "tasks"


def get_task_spec_path(room_id: str, task_id: str) -> Path:
    """tasks/<task_id>.md — mirror C# UCL_ChatTavernQuestIO.GetTaskSpecPath."""
    return get_tasks_dir(room_id) / f"{task_id}.md"


def get_notes_dir(room_id: str) -> Path:
    """notes/ dir for given room."""
    return get_room_dir(room_id) / "notes"


def get_note_path(room_id: str, key: str) -> Path:
    """notes/<key>.md — mirror C# GetNotePath."""
    return get_notes_dir(room_id) / f"{key}.md"


# ---------------------------------------------------------------------------
# Room enumeration + existence
# ---------------------------------------------------------------------------

def enumerate_room_ids() -> list[str]:
    """List all room directories under rooms/, sorted ascending. Mirrors C# EnumerateRoomIds."""
    if not ROOMS_DIR.is_dir():
        return []
    return sorted(d.name for d in ROOMS_DIR.iterdir() if d.is_dir())


def room_exists(room_id: str) -> bool:
    """Quick check if room dir exists."""
    return get_room_dir(room_id).is_dir()


# ---------------------------------------------------------------------------
# Convenience for CLI tools that print debug info
# ---------------------------------------------------------------------------

def debug_print_paths() -> None:
    """Smoke-test helper — print all top-level paths to verify resolution."""
    print(f"REPO_ROOT          = {REPO_ROOT}")
    print(f"AGENT_COMMANDS_DIR = {AGENT_COMMANDS_DIR}")
    print(f"TAVERN_DIR         = {TAVERN_DIR}")
    print(f"ROOMS_DIR          = {ROOMS_DIR}")
    print(f"IDENTITIES_PATH    = {IDENTITIES_PATH}")
    print(f"PRESENCE_PATH      = {PRESENCE_PATH}")
    print(f"NOTIFY_CONFIG_PATH = {NOTIFY_CONFIG_PATH}")
    print(f"discovered rooms   = {enumerate_room_ids()}")


if __name__ == "__main__":
    debug_print_paths()
