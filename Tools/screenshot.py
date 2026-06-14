#!/usr/bin/env python3
"""screenshot.py — T47: 螢幕截圖指令 + 存檔到專案內 (壓縮過避免大檔)

Usage:
    # 截整個 desktop 全螢幕（預設 JPEG quality 70 壓縮）
    python AgentCommands/Tools/screenshot.py

    # 指定品質 (1-95)；越低檔案越小
    python AgentCommands/Tools/screenshot.py --quality 50

    # 指定主螢幕 / 全螢幕（預設 all = 多螢幕全抓）
    python AgentCommands/Tools/screenshot.py --monitor primary
    python AgentCommands/Tools/screenshot.py --monitor all

    # 自訂 prefix（會附在檔名前面，方便辨識）
    python AgentCommands/Tools/screenshot.py --prefix bug-report

    # 不壓縮輸出 PNG（檔案較大，無損）
    python AgentCommands/Tools/screenshot.py --format png

存檔路徑：AgentCommands/Screenshots/<YYYY-MM-DD>/<HHMMSS_mmm>__<prefix>.jpg
（預設走 .gitignore 不入 commit；保 untracked 給 Tim 視覺確認）

回傳：stdout 印出 absolute path + size + dimensions；exit 0 = 成功

實作：
- 走 PIL.ImageGrab.grab(all_screens=True) 抓整個 desktop（Windows 內建支援）
- JPEG quality 70 平衡品質 / 檔案大小（~200-500KB / 1080p）；--quality 可調
- PIL 不可用時 fallback PowerShell .NET API（System.Drawing + System.Windows.Forms.Screen）

注意：
- 螢幕內可能含敏感資訊（密碼 / 私人 chat） — agent 取得截圖視為敏感資料，不該丟進 Discord 共享頻道；本 script 只負責存檔，由 caller 決定後續用途
- multi-monitor 環境預設抓 primary；--monitor all 抓全部（檔案會更大）
"""

from __future__ import annotations

import argparse
import datetime
import io
import os
import pathlib
import subprocess
import sys
import tempfile

_HERE = pathlib.Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent.parent
_SCREENSHOT_DIR = _REPO_ROOT / "AgentCommands" / "Screenshots"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def _get_target_path(prefix: str, fmt: str) -> pathlib.Path:
    """產生目標檔案路徑：AgentCommands/Screenshots/<YYYY-MM-DD>/<HHMMSS_mmm>__<prefix>.<ext>"""
    now = datetime.datetime.now()
    date_dir = _SCREENSHOT_DIR / now.strftime("%Y-%m-%d")
    date_dir.mkdir(parents=True, exist_ok=True)
    ms = f"{now.microsecond // 1000:03d}"
    base_name = now.strftime("%H%M%S") + f"_{ms}"
    if prefix:
        # 過濾不安全檔名字元
        safe_prefix = "".join(c if c.isalnum() or c in "-_" else "_" for c in prefix)[:50]
        base_name = f"{base_name}__{safe_prefix}"
    return date_dir / f"{base_name}.{fmt}"


def _grab_with_pil(all_screens: bool):
    """用 PIL.ImageGrab 截圖 — Windows 內建支援多螢幕"""
    from PIL import ImageGrab
    return ImageGrab.grab(all_screens=all_screens)


def _grab_with_powershell(target_path: pathlib.Path) -> bool:
    """fallback：PowerShell + .NET API 截整個 virtual screen 直接寫檔。

    回 True 表示成功；False 表示失敗。"""
    ps_script = f'''
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$screens = [System.Windows.Forms.Screen]::AllScreens
$rect = [System.Windows.Forms.SystemInformation]::VirtualScreen
$bmp = New-Object System.Drawing.Bitmap $rect.Width, $rect.Height
$gfx = [System.Drawing.Graphics]::FromImage($bmp)
$gfx.CopyFromScreen($rect.X, $rect.Y, 0, 0, $rect.Size)
$bmp.Save("{target_path.as_posix()}", [System.Drawing.Imaging.ImageFormat]::Png)
$gfx.Dispose()
$bmp.Dispose()
'''
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_script],
            capture_output=True, text=True, timeout=30, encoding="utf-8", errors="replace"
        )
        return result.returncode == 0 and target_path.exists()
    except Exception as e:
        print(f"[screenshot] powershell fallback fail: {e}", file=sys.stderr)
        return False


def take_screenshot(prefix: str, fmt: str, quality: int, monitor: str) -> int:
    """主流程：截圖 → 壓縮 → 存檔 → print 路徑

    回 exit code (0 成功)"""
    target_path = _get_target_path(prefix, fmt)
    all_screens = (monitor.lower() == "all")

    img = None
    # Layer 1: 嘗試 PIL.ImageGrab
    try:
        img = _grab_with_pil(all_screens=all_screens)
    except Exception as e:
        print(f"[screenshot] PIL fail (try powershell fallback)：{e}", file=sys.stderr)

    if img is not None:
        # PIL 成功 → 走壓縮 / 存檔路徑
        try:
            if fmt == "png":
                img.save(str(target_path), format="PNG", optimize=True, compress_level=9)
            else:
                # JPEG 不支援 alpha，需轉 RGB
                if img.mode != "RGB":
                    img = img.convert("RGB")
                img.save(str(target_path), format="JPEG", quality=int(quality), optimize=True)
        except Exception as e:
            print(f"[screenshot] save fail：{e}", file=sys.stderr)
            return 2
    else:
        # Layer 2: PowerShell fallback (PNG only)
        if fmt != "png":
            target_path = target_path.with_suffix(".png")
        ok = _grab_with_powershell(target_path)
        if not ok:
            print("[screenshot] 全部 backend 都失敗 — Pillow 未裝 + PowerShell 走不通", file=sys.stderr)
            return 3

    if not target_path.exists():
        print(f"[screenshot] 存檔失敗 (檔案不存在): {target_path}", file=sys.stderr)
        return 4

    size_bytes = target_path.stat().st_size
    rel_path = target_path.relative_to(_REPO_ROOT)
    width, height = (img.size if img is not None else ("?", "?"))
    print(f"[screenshot] saved: {target_path}")
    print(f"  rel_path: {rel_path}")
    print(f"  size: {size_bytes:,} bytes ({size_bytes / 1024:.1f} KB)")
    print(f"  dims: {width}x{height}")
    print(f"  format: {fmt.upper()}{f' quality={quality}' if fmt == 'jpg' else ''}")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--prefix", default="", help="檔名 prefix (預設無)")
    parser.add_argument("--format", choices=["jpg", "png"], default="jpg",
                        help="輸出格式：jpg = 壓縮(預設) / png = 無損")
    parser.add_argument("--quality", type=int, default=70,
                        help="JPEG quality 1-95 (預設 70)；越低檔案越小")
    parser.add_argument("--monitor", choices=["primary", "all"], default="all",
                        help="抓哪些螢幕：primary 主螢幕 / all 多螢幕全抓 (預設)")
    args = parser.parse_args(argv)

    if not (1 <= args.quality <= 95):
        parser.error(f"--quality 必須在 1-95 範圍，傳入 {args.quality}")

    return take_screenshot(args.prefix, args.format, args.quality, args.monitor)


if __name__ == "__main__":
    sys.exit(main())
