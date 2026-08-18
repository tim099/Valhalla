#!/usr/bin/env python3
# 區塊職責：AgentCommands 端 `_lib.ucl_paths` 的**轉發 shim** —— 實作只留 UCL_Core canonical 一份。
# 物理意義：
#   Tim 2026-08-18 拍板：本檔原本是 sync_lib_mirror.py 位元組同步出來的鏡像（AUTO-SYNCED 檔頭 +
#   canonical body 全文），現改為轉發 —— 因為「同名模組有兩份實作」的漂移是**靜默**的：
#   兩棵工具樹各自 sibling-import 自己的 `_lib`，UCL_Core 端長出新函式而鏡像沒同步時，
#   吃到鏡像的 caller 收到的是 ImportError，而那個 ImportError 常被 fail-soft 吞成「沒有資料」。
#   🩸 血證 (BUG-5, calli wake#24)：canonical 8/18 長出 `letters_persona_dir()`，鏡像停在 8/17，
#      wake_brief 的關係區塊 import 失敗 → exit 仍是 0 → brief 印出「還沒有關係紀錄」（假的）。
#   轉發之後「鏡像落後」這個狀態在物理上不存在：本檔沒有 body 可以落後。
# 數值影響：
#   純 import 期一次性解析（找 canonical 檔 → exec → 複製公開名）。不寫任何檔案／狀態。
#   對外行為與 canonical 完全一致，含 `ucl_core_dir()`／`ucl_tool()`：
#   canonical 靠 `__file__` 往上找名為 UCL_Core 的 ancestor 自我定位，而 exec 時 `__file__`
#   指的是 canonical 真實路徑 ⇒ 過去鏡像會 raise「無法自我定位 UCL_Core」的那兩支，現在可用。
#
# ⚠ 為什麼這裡還是有一小段候選路徑清單（看起來像「第四套解析器」）：
#   雞生蛋 —— 定位 UCL_Core 的邏輯**住在 canonical 裡**，而本檔的工作就是「還沒載到 canonical
#   之前先找到它」。所以本檔只保留 bootstrap 所需的最小量（env → .git walk → 候選 layout →
#   明確報錯），路徑語意一律以 canonical 為準，**不在本檔做任何額外的路徑推導**。
#   不能改成 import `_lib.tavern_paths.find_ucl_core_dir()` 借用它的清單：tavern_paths 在
#   模組層 import 本檔並取值 ⇒ 反向 import 會在初始化期撞 circular（AttributeError）。
#   候選清單的其他兩處（`_lib/tavern_paths.py`、skill `ucl-core-paths` 的 bash/PS 版）改了要一起改。

from __future__ import annotations

import importlib.util as _ilu
import os as _os
import sys as _sys
from pathlib import Path as _Path

_THIS_FILE = _Path(__file__).resolve()

# canonical 在 UCL_Core 樹內的固定相對位置（UCL_Core 根 → 本檔的對應物）。
_CANONICAL_REL = ("Tools~", "AgentCommands", "_lib", "ucl_paths.py")

# host 專案把 UCL_Core 掛在哪不固定；有序候選，第一個命中即用。
_UCL_CORE_CANDIDATES: tuple[tuple[str, ...], ...] = (
    ("Assets", "Plugins", "UCL_Core"),
    ("CardGame", "Assets", "UCL", "UCL_Core"),
    ("Assets", "UCL", "UCL_Core"),
    ("UCL_Core",),
)


def _git_root() -> _Path:
    # 與 canonical `_find_git_root_by_walk` 同契約：.git 為「資料夾」才算 host repo 根
    # （submodule 的 .git 是 gitlink 檔，要跳過繼續往上）。
    p = _THIS_FILE
    while p != p.parent:
        if (p / ".git").is_dir():
            return p
        p = p.parent
    # 走到頂沒命中：本檔在 <root>/AgentCommands/_lib/ ⇒ parents[2] 是慣例位置的 host 根。
    return _THIS_FILE.parents[2]


def _locate_canonical() -> _Path:
    # tier-1：env override（絕對路徑且存在才採用，與 tavern_paths.find_ucl_core_dir 同語意）
    env = _os.environ.get("UCL_CORE_DIR")
    if env:
        cand = _Path(env)
        if cand.is_absolute() and cand.is_dir():
            hit = cand.joinpath(*_CANONICAL_REL)
            if hit.is_file():
                return hit.resolve()
    # tier-2：host repo 根下的候選 layout
    root = _git_root()
    for parts in _UCL_CORE_CANDIDATES:
        hit = root.joinpath(*parts, *_CANONICAL_REL)
        if hit.is_file():
            return hit.resolve()
    # 解析失敗一律明確報錯 —— 靜默 fallback 到別的實作正是本 shim 要消滅的病。
    raise RuntimeError(
        "_lib.ucl_paths（轉發 shim）找不到 UCL_Core canonical："
        f"{'/'.join(_CANONICAL_REL)}\n"
        f"  已試 repo 根：{root}\n"
        f"  已試候選：{', '.join('/'.join(c) for c in _UCL_CORE_CANDIDATES)}\n"
        "  → UCL_Core 掛載位置不在候選清單時，設環境變數 UCL_CORE_DIR=<UCL_Core 絕對路徑>，"
        "或把該 layout 補進本檔與 _lib/tavern_paths.py 的候選清單（兩處要一致）。"
    )


def _load_canonical():
    # 用檔案路徑載入（不走 package import）—— 因為 `_lib` 這個 package 名已經被本樹佔用，
    # sys.path 再怎麼插都會解析回本檔（那正是 BUG-5 的形狀）。
    path = _locate_canonical()
    mod_name = "_ucl_paths_canonical"
    cached = _sys.modules.get(mod_name)
    if cached is not None and getattr(cached, "__file__", None) == str(path):
        return cached
    spec = _ilu.spec_from_file_location(mod_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"_lib.ucl_paths（轉發 shim）無法載入 canonical：{path}")
    mod = _ilu.module_from_spec(spec)
    _sys.modules[mod_name] = mod          # 先註冊再 exec，canonical 內若有自我 import 才不會重跑
    spec.loader.exec_module(mod)
    return mod


_CANONICAL = _load_canonical()

# 公開名一律**動態**轉發，不寫明確清單 —— 寫清單就等於留一份會落後的名冊
# （canonical 新增函式而清單沒跟上 = BUG-5 換個位置重演）。
# lru_cache／常數／函式都是同一個物件，caller 對它做 isinstance／cache_clear 的語意不變。
for _name, _value in vars(_CANONICAL).items():
    if not _name.startswith("_"):
        globals()[_name] = _value
del _name, _value

# canonical 的真實路徑（除錯用：想知道到底轉發到哪一份就讀這個）。
CANONICAL_PATH = _Path(_CANONICAL.__file__)
