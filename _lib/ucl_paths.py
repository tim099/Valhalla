# ╔═══ 退場 shim — 本檔不再是鏡像副本（Tim 2026-08-18 拍板）═══╗
# 區塊職責：把 `AgentCommands/_lib.ucl_paths` 這個 import 路徑轉發到 UCL_Core 的 canonical。
#
# 物理意義：本檔原本是 canonical 的**位元組同步鏡像**（sync_lib_mirror.py 維護）。
#   鏡像制的問題不是機制不好，是它**要有人記得同步**：
#   🩸 2026-08-18 實測 —— canonical 468 行、鏡像停在 447 行，
#      少的正好是新加的 `letters_persona_dir`。任何吃到鏡像的 import 都會
#      `ImportError: cannot import name 'letters_persona_dir'`。
#      而那次會被發現，只因為呼叫端剛好把失敗印出來；原設計是 `except: return None`，
#      那樣只會少一段輸出、什麼都不說。
#
# ⇒ Tim 拍板：**一律改用 UCL_Core 版本，本檔廢棄。**
#   ⛔ 但不直接刪 —— 刪掉的話舊 import 只會得到 `ModuleNotFoundError`，
#     那句話不告訴任何人該改用什麼。轉發 shim 讓舊路徑繼續能動，
#     而且**實作只剩一份**，漂移從此不可能發生。
#
# 數值影響：純轉發，零邏輯。canonical 找不到時**大聲失敗**（不 fallback 到舊副本）——
#   靜默 fallback 正是這次要消滅的東西。
#
# 📌 新程式碼請直接寫：
#       import sys; sys.path.insert(0, "<UCL_Core>/Tools~/AgentCommands")
#       from _lib.ucl_paths import letters_root, letters_persona_dir, data_root, repo_root
# ╚══════════════════════════════════════════════════════════════╝
from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path


def _canonical_dir() -> _Path:
    """找 UCL_Core 的 Tools~/AgentCommands（canonical `_lib` 的所在）。

    🩸 **不靠 `.git` walk-up 定位 repo 根** —— `AgentCommands` 自己是 submodule，
       它的 `.git` 是一個檔案（gitlink），往上找「第一個含 .git 的祖先」會**停在這裡**，
       於是永遠找不到 UCL_Core。這隻坑在本專案有前科（catchup 路徑 bug 同一族）。
    ⇒ 改成**逐層祖先直接試候選**：誰底下真的有那個檔，誰就是答案。
       判準從「這裡像不像 repo 根」換成「這裡有沒有我要的東西」——
       後者不需要猜，也不會被 submodule 的 .git 騙。
    ⚠ 掛載位置各專案不同，所以是清單不是單一路徑；清單沒中再 glob 掃一輪。
    """
    here = _Path(__file__).resolve()
    rels = ("Assets/Plugins/UCL_Core", "Assets/UCL/UCL_Core", "UCL_Core")
    for parent in here.parents:
        for rel in rels:
            cand = parent.joinpath(*rel.split("/")) / "Tools~" / "AgentCommands"
            if (cand / "_lib" / "ucl_paths.py").is_file():
                return cand
    for parent in here.parents:
        for cand in parent.glob("*/**/UCL_Core/Tools~/AgentCommands"):
            if (cand / "_lib" / "ucl_paths.py").is_file():
                return cand
        if (parent / ".git").is_dir():      # 真的 repo 根（目錄不是 gitlink 檔）就別再往上
            break
    raise ImportError(
        "[ucl_paths shim] 找不到 UCL_Core canonical 的 _lib/ucl_paths.py。"
        " 本檔已退場為轉發 shim，不再自帶實作 —— 請確認 UCL_Core submodule 已 checkout。")


_CANON = _canonical_dir()
if str(_CANON) not in _sys.path:
    _sys.path.insert(0, str(_CANON))

# ⚠ 不能寫 `from _lib.ucl_paths import *` —— 那個名字**現在就是本 shim 自己**
#   （已在 sys.modules 裡且只初始化到一半），會轉發到自己 ⇒ 拿不到 canonical 的東西。
#   ⇒ 用檔案路徑以**別的模組名**載入 canonical，再把它的命名空間複製過來。
import importlib.util as _ilu   # noqa: E402

_spec = _ilu.spec_from_file_location("_ucl_paths_canonical", _CANON / "_lib" / "ucl_paths.py")
_canon = _ilu.module_from_spec(_spec)
_sys.modules.setdefault("_ucl_paths_canonical", _canon)
_spec.loader.exec_module(_canon)

for _k in dir(_canon):
    if _k.startswith("__"):
        continue
    globals()[_k] = getattr(_canon, _k)
del _k, _spec, _ilu
