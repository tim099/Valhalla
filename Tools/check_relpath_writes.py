#!/usr/bin/env python3
# 區塊職責：cwd-相對路徑寫檔 anti-pattern 偵測器（warning-only lint）。
# 物理意義：
#   掃 AgentCommands/Tools/*.py，揪出「把資料路徑寫成裸 cwd-相對字串」的病灶簽名
#   （e.g. LEDGER_ROOT = "AgentCommands/Treasury/ledger"）。這種寫法會跟著呼叫端 cwd 漂移：
#   從子目錄跑時誤落雙層位置、stdout 卻報對 —— 2026-06-16 qa_bug_reward + 4 支 ledger 工具血證、
#   tavern_catchup .git walk-up 同家族。正解是改用 _lib.repo_root.find_repo_root() 錨定主根。
# 數值影響：
#   純讀檔 + 印警告，**不修改任何檔、預設不擋 commit**（exit 0），對齊既有 pre-commit hook
#   「warning 不 block」慣例，免 false-positive 厭世。加 --strict 才回 exit 1（CI gating 用）。
#
# 用法：
#   python AgentCommands/Tools/check_relpath_writes.py            # 掃全 Tools，印警告，exit 0
#   python AgentCommands/Tools/check_relpath_writes.py --strict   # 有命中回 exit 1
#   python AgentCommands/Tools/check_relpath_writes.py f1.py f2.py # 只掃指定檔（pre-commit staged 用）

import argparse
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

# 區塊職責：病灶簽名 regex
# 物理意義：抓「常數名 = 引號 + AgentCommands/ 或 docs/ 開頭的裸相對字串」。
#          這類常數後續多半拿去 open()/makedirs()/glob() 當路徑根，cwd 一漂就誤寫。
# 數值影響：純比對；只挑「字面以已知 repo 子目錄開頭」的相對字串，降低誤報。
_BARE_RELPATH = re.compile(
    r"""^\s*[A-Z_][A-Z0-9_]*\s*=\s*['"](AgentCommands|docs|CardGame)[/\\]"""
)

# 本檔自身 + helper 不算病灶（它們是解法，不是病灶）。
_SKIP_FILES = {"check_relpath_writes.py"}


def scan_file(path: str):
    """回 [(lineno, line_text), ...] 命中清單。"""
    hits = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                # 跳過註解行（# 開頭 trim 後）— 註解裡舉例不算病灶
                if line.lstrip().startswith("#"):
                    continue
                if _BARE_RELPATH.match(line):
                    hits.append((i, line.rstrip()))
    except (OSError, UnicodeDecodeError):
        pass
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description="cwd-相對路徑寫檔 anti-pattern 偵測 (warning-only)")
    parser.add_argument("files", nargs="*", help="指定檔（缺則掃整個 AgentCommands/Tools）")
    parser.add_argument("--strict", action="store_true", help="有命中回 exit 1（CI gating）")
    args = parser.parse_args()

    # 決定掃描清單
    if args.files:
        targets = [f for f in args.files if f.endswith(".py")]
    else:
        tools_dir = os.path.dirname(os.path.abspath(__file__))
        targets = [
            os.path.join(tools_dir, n)
            for n in sorted(os.listdir(tools_dir))
            if n.endswith(".py")
        ]

    total = 0
    for path in targets:
        if os.path.basename(path) in _SKIP_FILES:
            continue
        hits = scan_file(path)
        if hits:
            # os.path.relpath 在 Windows 跨磁碟（檔在 C:、cwd 在 D:）會 ValueError → 退回原始路徑顯示
            try:
                rel = os.path.relpath(path)
            except ValueError:
                rel = path
            for lineno, text in hits:
                total += 1
                print(f"⚠ {rel}:{lineno}  裸 cwd-相對路徑常數 → 改用 _lib.repo_root.find_repo_root()")
                print(f"    {text.strip()}")

    if total == 0:
        print("✓ 無裸 cwd-相對路徑常數命中")
        return 0

    print(f"\n⚠ 共 {total} 處命中。修法：from _lib.repo_root import find_repo_root; "
          f"ROOT = os.path.join(find_repo_root(), 'AgentCommands', ...)")
    print("  （warning-only，預設不擋 commit；CI 想 gate 加 --strict）")
    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
