#!/usr/bin/env python3
"""繞過 broken pip 手動下載 + 安裝 wheel chain.

用 PyPI JSON API 找 wheel URL → urlretrieve 下載 → zipfile extract 到 site-packages.
壞掉的舊版本改名隔離 (不直接刪).

用法: python install_wheel_chain.py <pkg1> [<pkg2> ...]
"""
import json
import os
import re
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# 路徑解析 — TMP 改由 _lib.repo_root 動態錨定主專案根（拔除寫死絕對路徑；T-PATH-RESOLVE T04）。
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from _lib.repo_root import find_repo_root  # noqa: E402

# 備忘（out of scope）：SITE 是「本機 Python 直譯器的 site-packages」，非 repo 路徑，跟本案
#   「跨專案 repo 相對化」無關 —— 它綁的是這台機器的 Python 安裝位置。真要 portable 應改用
#   sysconfig.get_paths()['purelib']，但那是另一個關注點，本案不動（見 Inventory 第 5 類精神）。
SITE = Path(r"C:\Users\Tim\AppData\Local\Programs\Python\Python310\Lib\site-packages")
TMP = Path(find_repo_root()) / "AgentCommands" / "_tmp"
TMP.mkdir(parents=True, exist_ok=True)


def get_wheel_url(pkg_name: str):
    """從 PyPI 找最新版本的 py3 pure-wheel URL (或對應平台 wheel)."""
    api = f"https://pypi.org/pypi/{pkg_name}/json"
    try:
        data = json.load(urllib.request.urlopen(api, timeout=15))
    except Exception as e:
        return None, str(e)
    files = data.get("urls", [])
    # Prefer pure-Python wheel (py3-none-any)
    pure = [f for f in files if f.get("packagetype") == "bdist_wheel"
            and f.get("filename", "").endswith("-py3-none-any.whl")]
    if pure:
        return pure[0]["url"], None
    # Else find win amd64 wheel for Python 3.10
    win = [f for f in files if f.get("packagetype") == "bdist_wheel"
           and "cp310" in f.get("filename", "") and "win_amd64" in f.get("filename", "")]
    if win:
        return win[0]["url"], None
    # Else any wheel
    any_whl = [f for f in files if f.get("packagetype") == "bdist_wheel"]
    if any_whl:
        return any_whl[0]["url"], None
    return None, "no wheel found"


def quarantine_existing(pkg_dirs):
    """把 site-packages 內衝突的 dir / dist-info 改名隔離."""
    for d in pkg_dirs:
        p = SITE / d
        if p.exists():
            backup = SITE / f"{d}.recuva-corrupted"
            if backup.exists():
                # 已備份過, 直接刪這次的
                shutil.rmtree(p, ignore_errors=True)
            else:
                p.rename(backup)


def install_wheel(pkg_name: str):
    """下載 + 解 wheel 到 site-packages."""
    print(f"\n=== {pkg_name} ===")
    url, err = get_wheel_url(pkg_name)
    if not url:
        print(f"  ✗ get URL fail: {err}")
        return False
    print(f"  URL: {url[:80]}...")
    fname = url.rsplit("/", 1)[-1]
    out = TMP / fname
    try:
        urllib.request.urlretrieve(url, out)
    except Exception as e:
        print(f"  ✗ download fail: {e}")
        return False
    print(f"  Downloaded: {out.stat().st_size} bytes")

    # 隔離 corrupted 舊版本
    # 推測 dir name: pkg_name normalize (lowercase, - → _)
    pkg_dir = pkg_name.lower().replace("-", "_")
    # 嘗試多個變體
    candidates = [pkg_dir, pkg_name.lower(), pkg_name]
    # 找 dist-info
    dist_info_patterns = [d for d in os.listdir(SITE)
                          if d.lower().startswith(pkg_dir + "-") and d.endswith(".dist-info")]
    quarantine_existing(candidates + dist_info_patterns)

    # 解壓
    try:
        with zipfile.ZipFile(out, 'r') as z:
            z.extractall(SITE)
        print(f"  ✓ extracted")
    except Exception as e:
        print(f"  ✗ extract fail: {e}")
        return False

    # 測試 import
    import_name = pkg_name.replace("-", "_").replace(".", "_")
    # 特例
    if pkg_name == "discord.py":
        import_name = "discord"
    elif pkg_name == "PyYAML":
        import_name = "yaml"
    try:
        # 在 subprocess 跑 import 避免污染當前 process state
        import subprocess
        r = subprocess.run(
            [sys.executable, "-c", f"import {import_name}; print('import OK')"],
            capture_output=True, text=True, timeout=15,
        )
        if r.returncode == 0:
            print(f"  ✓ import {import_name} OK")
            return True
        else:
            print(f"  ⚠ import {import_name} fail: {r.stderr.strip().splitlines()[-1]}")
            return False
    except Exception as e:
        print(f"  ⚠ test fail: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("usage: install_wheel_chain.py <pkg1> [<pkg2> ...]")
        return 1
    packages = sys.argv[1:]
    print(f"Installing {len(packages)} packages, target: {SITE}")
    results = {}
    for pkg in packages:
        ok = install_wheel(pkg)
        results[pkg] = ok
    print("\n=== Summary ===")
    for pkg, ok in results.items():
        mark = "✓" if ok else "✗"
        print(f"  {mark} {pkg}")
    return 0 if all(results.values()) else 2


if __name__ == "__main__":
    sys.exit(main())
