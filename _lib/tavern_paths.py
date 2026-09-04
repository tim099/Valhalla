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

import os as _os
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
# ⚠ 2026-08-17（Tim 拍板）：pointer 檔讀取的唯一實作在 UCL_Core 的 _lib/ucl_paths.py。
#   原本有 10 份平行實作（本檔是唯一住在**專案側 repo**的那份）。十份都對，
#   但十份就是十個會各自漂移的真相源；漂移的症狀是「這支讀 A 目錄、那支讀 B 目錄」，
#   兩邊都不報錯。⇒ 之後改 pointer 檔格式只需改一處。
# ⚠ 跨 repo：本檔在 AgentCommands（專案狀態側），ucl_paths 在 UCL_Core（程式碼側，
#   掛載位置跨專案不定）⇒ 用**資料夾名搜尋**定位 UCL_Core，與 C# UCL_RepoPath.FindUCLCoreDir
#   同演算法（只搜 Assets/ 底下，不往專案外找 —— 專案外可能有另一份 checkout）。
#   找不到就走 fallback，不 raise：本檔是被 daemon / notify 這類長壽命工具 import 的，
#   在此炸掉會讓整條通知線斷掉，而那比「用預設路徑」嚴重。
def _load_ucl_paths(git_root: Path):
    assets = git_root / "Assets"
    if assets.is_dir():
        for cand in assets.rglob("UCL_Core"):
            mod_path = cand / "Tools~" / "AgentCommands" / "_lib" / "ucl_paths.py"
            if mod_path.is_file():
                import importlib.util as ilu
                spec = ilu.spec_from_file_location("_ucl_paths_from_tavern_paths", mod_path)
                m = ilu.module_from_spec(spec)
                spec.loader.exec_module(m)
                return m
    return None


def _resolve_agentcommands_data_root(git_root: Path) -> Path:
    mod = _load_ucl_paths(git_root)
    if mod is not None:
        return mod.data_root()
    # fallback：找不到 UCL_Core（非標準佈局）→ 只能走預設。
    # ⚠ 這裡**刻意不再讀 pointer 檔**：2026-08-17 起 pointer 住在 <UCL_Core>/ 底下，
    #   而走到這一行就代表 UCL_Core 沒找到 ⇒ 那個檔按定義也讀不到。
    #   舊版在這裡讀 repo-root 下的 pointer，格式改成多行之後會讀到 `schema=2` 那行、
    #   判定不是絕對路徑、**靜默退回預設** —— 看起來一樣，但那是「碰巧對」不是「對」。
    return (git_root / "AgentCommands").resolve()


# 對外暴露的常數 — caller 引用這些而不是自己 hardcode
REPO_ROOT: Path = _find_repo_root()
# AGENT_COMMANDS_DIR = 資料根 (可被 pointer 檔 override;預設 = REPO_ROOT/AgentCommands)
AGENT_COMMANDS_DIR: Path = _resolve_agentcommands_data_root(REPO_ROOT)


# 區塊職責：AwakenInit 子路徑（persona 檔 / registry meta）的專案側入口。
# 物理意義：專案側工具（tavern_catchup / migrate_voucher…）原本各自拼
#          `REPO_ROOT / "AgentCommands" / "AwakenInit" / "personas"`。那串字每多一份，
#          就多一個在資料根被 override 時**安靜讀錯目錄**的地方（不會報錯）。
#          ⇒ 收斂到這裡；能取到 UCL_Core 就直接用它的解析（含 registry_path override），
#            取不到才退回資料根拼接（與舊行為相同）。
def _awaken_init_dir() -> Path:
    mod = _load_ucl_paths(REPO_ROOT)
    if mod is not None:
        return mod.awaken_init_dir()
    return AGENT_COMMANDS_DIR / "AwakenInit"


AWAKEN_INIT_DIR: Path = _awaken_init_dir()
PERSONAS_DIR: Path = AWAKEN_INIT_DIR / "personas"
REGISTRY_META_PATH: Path = AWAKEN_INIT_DIR / "_registry_meta.json"


def persona_file(persona: str) -> Path:
    return PERSONAS_DIR / f"{persona}.json"
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

# PromptQueue = mirror 系統的「資料目錄」(config / state / webhook secret / log) — 留專案 canonical
# (T-PATH-01 不跟 DataRoot override 搬)。T-MOVE (Tim 2026-07-15 拍板): scripts 本體
# (notify_discord.py / notify_treasury.py) 已搬 UCL_CORE 的 Tools~/AgentCommands/PromptQueue/
# (UCL_AGENTCMD_DIR / "PromptQueue")；本目錄舊檔為 forwarding shim (過渡一版)。
PROMPT_QUEUE_DIR: Path = REPO_ROOT / "AgentCommands" / "PromptQueue"
NOTIFY_STATE_PATH: Path = PROMPT_QUEUE_DIR / "_notify_state.json"
TAVERN_STATE_PATH: Path = PROMPT_QUEUE_DIR / "_tavern_state.json"
WAKE_STATE_PATH: Path = PROMPT_QUEUE_DIR / "_wake_state.json"
NOTIFY_CONFIG_PATH: Path = PROMPT_QUEUE_DIR / "notify_config.json"


# ---------------------------------------------------------------------------
# UCL_Core / .BuiltinModules location resolution (layout-agnostic)  [T-PATH-02]
# ---------------------------------------------------------------------------
# 區塊職責：集中做 UCL_Core（含 run_cmd.py / awakening.py）與 .BuiltinModules 的跨布局定位。
# 物理意義：上層專案把 UCL_Core 放的位置各異 —
#   - 本 (LY) 專案:   Assets/Plugins/UCL_Core          + Assets/.BuiltinModules
#   - CardGame 專案:  CardGame/Assets/UCL/UCL_Core     + CardGame/Assets/.BuiltinModules
#   - 其他布局:       Assets/UCL/UCL_Core / <root>/UCL_Core
#   舊 code 各自 hardcode "CardGame/Assets/UCL/UCL_Core" → 換專案即斷（run_cmd.py not found，
#   awakening tavern post FAIL、treasury_ledger 靜默降級 inline 等）。這裡逐一探測候選 layout。
# 數值影響：純檔案存在性探測 + 環境變數 override；找不到才退回第一候選（讓 caller 在呼叫點以清楚路徑報錯，不靜默）。

_UCL_CORE_CANDIDATES: tuple[tuple[str, ...], ...] = (
    ("Assets", "Plugins", "UCL_Core"),
    ("CardGame", "Assets", "UCL", "UCL_Core"),
    ("Assets", "UCL", "UCL_Core"),
    ("UCL_Core",),
)

# UCL_Core 的**身分錨** —— 用來判定「這個候選目錄是不是 UCL_Core」（任一命中即可）。
# ⛔ 這裡放的東西必須是**不隨某次轉接／重構退場**的：
#    2026-09-04 之前這格是 `Tools~/AgentCommands/run_cmd.py`，而那支檔案排定要刪（TASK-0107）
#    ⇒ 刪掉的那天所有候選會一起落空，然後靜默退到 fallback。
# ⚠ 要加新錨請問一句：**「這個檔會不會因為某次改動而消失？」** 會的話它就不是錨。
_UCL_CORE_ANCHORS: tuple[tuple[str, ...], ...] = (
    ("Tools~", "AgentCommands", "_lib", "ucl_paths.py"),   # python 路徑解析的 canonical
    ("AgentEntry", "UCL_Core_Entry.md"),                   # UCL_Core 的 agent 入口（身分，不是功能）
)

_BUILTIN_MODULES_CANDIDATES: tuple[tuple[str, ...], ...] = (
    ("Assets", ".BuiltinModules"),
    ("CardGame", "Assets", ".BuiltinModules"),
)


def find_ucl_core_dir(repo_root: Path | None = None) -> Path:
    """回傳 UCL_Core 根目錄（layout-agnostic）。

    解析優先序：
      1. 環境變數 UCL_CORE_DIR（絕對路徑且存在，最權威）
      2. repo_root 下第一個命中「UCL_Core 身分錨」的候選 layout（見 _UCL_CORE_ANCHORS）
      3. fallback：第一候選（Assets/Plugins/UCL_Core）— 讓 caller 報出清楚的 not-found 而非靜默

    🩸 2026-09-04（TASK-0107）：第 2 層的錨原本是 ``Tools~/AgentCommands/run_cmd.py`` ——
       **那是拿一個排定要刪的檔，當「這個目錄是不是 UCL_Core」的判準。**
       `run_cmd.py` 一刪，四個候選 layout 會**全部落空** ⇒ 退到 fallback（第一候選），
       於是在 layout 不同的專案上（`CardGame/Assets/UCL/UCL_Core` 那種）**靜默指到一個不存在的目錄**，
       而下游只會看到「檔案找不到」，看不到「根解錯了」。
       📌 **常數壞掉會喊，判準壞掉不會。**
    ⇒ 改用兩個**不隨轉接退場**的錨（任一命中即可）：
       · `Tools~/AgentCommands/_lib/ucl_paths.py` —— python 端路徑解析的 canonical，
         它不在的話這個函式找到了也沒用（同一層的問題）
       · `AgentEntry/UCL_Core_Entry.md` —— UCL_Core 的 agent 入口薄索引，那是**身分**不是功能
       兩個都列而不是挑一個：單一錨正是這次要修的病，換一個單一錨只是把到期日往後挪。
    """
    root = (repo_root or REPO_ROOT).resolve()
    env = _os.environ.get("UCL_CORE_DIR")
    if env:
        p = Path(env)
        if p.is_absolute() and p.is_dir():
            return p.resolve()
    for parts in _UCL_CORE_CANDIDATES:
        cand = root.joinpath(*parts)
        if any(cand.joinpath(*_a).is_file() for _a in _UCL_CORE_ANCHORS):
            return cand.resolve()
    return root.joinpath(*_UCL_CORE_CANDIDATES[0])


def find_builtin_modules_dir(repo_root: Path | None = None) -> Path:
    """回傳 .BuiltinModules 根目錄（layout-agnostic），規則同 find_ucl_core_dir。"""
    root = (repo_root or REPO_ROOT).resolve()
    env = _os.environ.get("UCL_BUILTIN_MODULES_DIR")
    if env:
        p = Path(env)
        if p.is_absolute() and p.is_dir():
            return p.resolve()
    for parts in _BUILTIN_MODULES_CANDIDATES:
        cand = root.joinpath(*parts)
        if cand.is_dir():
            return cand.resolve()
    return root.joinpath(*_BUILTIN_MODULES_CANDIDATES[0])


def senate_exe() -> Path:
    """Senate CLI（`senate.exe`）的絕對路徑 —— python 端派 Cmd 時的執行檔（TASK-0107）。

    ⛔ **不在這裡重造解析邏輯** —— 轉呼叫 UCL_Core 的 `_lib/ucl_paths.senate_exe()`
    （三層：env `UCL_SENATE_EXE` → pointer 檔的 `senate_exe=` → `shutil.which("senate")`，
    全落空才 raise）。本專案的硬規則是「路徑一律走既有解析器」，而那支就是既有的那個。

    ⚠ **刻意寫成函式而不是模組級常數**：解不到時它會 raise，
    而模組級常數會讓 `import tavern_paths` 整支炸掉 ⇒ 連帶炸掉七個消費端
    （其中六支是 PromptQueue 的活體工具）。
    ⇒ **失敗要發生在真的要用它的那一刻**，不是在 import 的時候。
    """
    import importlib.util as _ilu
    _p = UCL_LIB_DIR / "ucl_paths.py"
    if not _p.is_file():
        raise FileNotFoundError(
            f"找不到 UCL_Core 的路徑解析器：{_p}\n"
            f"（UCL_CORE_DIR 解到 {UCL_CORE_DIR} —— 如果那不是你的 UCL_Core，"
            f"問題在 find_ucl_core_dir() 的錨，不在這裡。）")
    _spec = _ilu.spec_from_file_location("_ucl_paths_tavern_paths", _p)
    _m = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_m)
    return _m.senate_exe()


# 對外常數 — caller 引用這些而不是自己 hardcode CardGame/... 路徑
UCL_CORE_DIR: Path = find_ucl_core_dir()
UCL_AGENTCMD_DIR: Path = UCL_CORE_DIR / "Tools~" / "AgentCommands"
UCL_LIB_DIR: Path = UCL_AGENTCMD_DIR / "_lib"
RUN_CMD_PATH: Path = UCL_AGENTCMD_DIR / "run_cmd.py"
AWAKENING_PATH: Path = UCL_AGENTCMD_DIR / "awakening.py"
CANVAS_PATH: Path = UCL_AGENTCMD_DIR / "canvas.py"
BUILTIN_MODULES_DIR: Path = find_builtin_modules_dir()


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
    print(f"UCL_CORE_DIR       = {UCL_CORE_DIR}")
    print(f"RUN_CMD_PATH       = {RUN_CMD_PATH}  (exists={RUN_CMD_PATH.is_file()})"
          f"　⏳ 退場中（TASK-0107）")
    # senate_exe() 會 raise（刻意的）⇒ 自測要把失敗印成可讀的診斷，而不是讓整支自測當掉。
    try:
        print(f"senate_exe()       = {senate_exe()}")
    except Exception as _e:
        print(f"senate_exe()       = ⛔ 解不到 —— {_e}")
    print(f"AWAKENING_PATH     = {AWAKENING_PATH}  (exists={AWAKENING_PATH.is_file()})")
    print(f"BUILTIN_MODULES    = {BUILTIN_MODULES_DIR}  (exists={BUILTIN_MODULES_DIR.is_dir()})")
    print(f"discovered rooms   = {enumerate_room_ids()}")


if __name__ == "__main__":
    debug_print_paths()
