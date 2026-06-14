#!/usr/bin/env python3
# 區塊職責：Civ6 桌面操控 POC 去風險工具 (T-Civ6-Desktop-Control, Tim 2026-06-14 啟動)
# 物理意義：在真正寫 game_input.py / guardian 架構前, 先驗 summit 拍板的「四綠燈」:
#   ① ImageGrab 抓得到 Civ6 畫面
#   ② SendInput 一次點擊遊戲有反應 (截圖 diff)
#   ③ 自己 SendInput 的事件 → LL hook 看到 injected=true
#   ④ Tim 實體動滑鼠 → LL hook 看到 injected=false
# 四個都綠才開架構, 否則白做 (跨層次驗證: 不假設 SendInput 一定生效 / injected 一定可辨)。
# 數值影響：純 stdlib (ctypes + PIL), 無第三方輸入庫依賴; DPI-aware 讓截圖像素 == SendInput ABSOLUTE 座標。
import argparse
import ctypes
import sys
import time
from ctypes import wintypes
from pathlib import Path

# Windows console UTF-8
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# DPI-aware 必須在任何螢幕/游標 API 之前設, 否則 2560x1600 會被當 1280x800 之類縮放座標
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

user32 = ctypes.windll.user32
OUT_DIR = Path(__file__).resolve().parent.parent / "_civ6_poc"
OUT_DIR.mkdir(exist_ok=True)

SCREEN_W = user32.GetSystemMetrics(0)
SCREEN_H = user32.GetSystemMetrics(1)


# ===========================================================
# 找 Civ6 視窗 + PrintWindow 截圖 (DX12-safe, 不受遮擋)
# 物理意義: PrintWindow(PW_RENDERFULLCONTENT=2) 叫視窗自己 render 進 DC,
#   即使被 File Explorer 蓋住 / 非前景 / DX12 也抓得到乾淨畫面 (POC 已驗)。
# ===========================================================
def find_civ6():
    import ctypes.wintypes as wt
    found = []
    EnumProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wt.HWND, wt.LPARAM)

    def cb(h, l):
        n = user32.GetWindowTextLengthW(h)
        if n:
            buf = ctypes.create_unicode_buffer(n + 1)
            user32.GetWindowTextW(h, buf, n + 1)
            if "Civilization" in buf.value:
                found.append(h)
        return True

    user32.EnumWindows(EnumProc(cb), 0)
    return found[0] if found else None


def window_rect(hwnd):
    r = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(r))
    return r.left, r.top, r.right - r.left, r.bottom - r.top


def capture_window(hwnd):
    from PIL import Image
    gdi32 = ctypes.windll.gdi32
    _, _, w, h = window_rect(hwnd)
    hdc = user32.GetWindowDC(hwnd)
    mdc = gdi32.CreateCompatibleDC(hdc)
    bmp = gdi32.CreateCompatibleBitmap(hdc, w, h)
    gdi32.SelectObject(mdc, bmp)
    user32.PrintWindow(hwnd, mdc, 2)  # PW_RENDERFULLCONTENT

    class BMIH(ctypes.Structure):
        _fields_ = [("biSize", wintypes.DWORD), ("biWidth", wintypes.LONG),
                    ("biHeight", wintypes.LONG), ("biPlanes", wintypes.WORD),
                    ("biBitCount", wintypes.WORD), ("biCompression", wintypes.DWORD),
                    ("biSizeImage", wintypes.DWORD), ("biXPelsPerMeter", wintypes.LONG),
                    ("biYPelsPerMeter", wintypes.LONG), ("biClrUsed", wintypes.DWORD),
                    ("biClrImportant", wintypes.DWORD)]

    bmi = BMIH()
    bmi.biSize = ctypes.sizeof(BMIH)
    bmi.biWidth = w
    bmi.biHeight = -h
    bmi.biPlanes = 1
    bmi.biBitCount = 32
    bmi.biCompression = 0
    buf = ctypes.create_string_buffer(w * h * 4)
    gdi32.GetDIBits(mdc, bmp, 0, h, buf, ctypes.byref(bmi), 0)
    img = Image.frombuffer("RGB", (w, h), buf, "raw", "BGRX", 0, 1)
    gdi32.DeleteObject(bmp)
    gdi32.DeleteDC(mdc)
    user32.ReleaseDC(hwnd, hdc)
    return img


def foreground(hwnd):
    # 穩健叫前景: minimize→restore 強制 raise (比單 SetForegroundWindow 可靠)
    user32.ShowWindow(hwnd, 6)   # SW_MINIMIZE
    time.sleep(0.15)
    user32.ShowWindow(hwnd, 9)   # SW_RESTORE
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.4)
    return user32.GetForegroundWindow() == hwnd


def root_of(hwnd):
    GA_ROOT = 2
    return user32.GetAncestor(hwnd, GA_ROOT)


# ===========================================================
# SendInput 結構 (mouse) — 走 SendInput 而非 SetCursorPos
# 物理意義: summit 拍板 — SetCursorPos 的 injected 標記跨 Windows 版本不一致,
#   移動也走 SendInput(MOUSEEVENTF_MOVE|ABSOLUTE) 才能讓 injected 標記統一,
#   否則 guardian 會把 agent 自己的移動誤判成 Tim 實體操作 → 自我冷卻凍死。
# 數值影響: ABSOLUTE 座標係 0..65535 normalized 到 virtual screen, 要自己換算。
# ===========================================================
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_WHEEL = 0x0800
INPUT_MOUSE = 0


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", wintypes.LONG), ("dy", wintypes.LONG),
                ("mouseData", wintypes.DWORD), ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD), ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [("wVk", wintypes.WORD), ("wScan", wintypes.WORD),
                ("dwFlags", wintypes.DWORD), ("time", wintypes.DWORD),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]


class _INPUTunion(ctypes.Union):
    _fields_ = [("mi", MOUSEINPUT), ("ki", KEYBDINPUT)]


class INPUT(ctypes.Structure):
    _fields_ = [("type", wintypes.DWORD), ("u", _INPUTunion)]


# ===========================================================
# 鍵盤 SendInput (scancode) — Tim 補充: WASD 平移鏡頭
# 物理意義: 走 KEYEVENTF_SCANCODE (硬體掃描碼) 而非 VK, 對遊戲相容性最好 —
#   許多遊戲經 DirectInput 讀 scancode, 純 VK 注入可能不吃 (summit DirectInput 顧慮)。
#   WASD 平移鏡頭 = 零遊戲狀態變動的最安全可見變化測試。
# ===========================================================
INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008
VK = {"w": 0x57, "a": 0x41, "s": 0x53, "d": 0x44, "esc": 0x1B}


def _send_key(vk, up=False):
    # VK → scancode (MapVirtualKey MAPVK_VK_TO_VSC=0)
    scan = user32.MapVirtualKeyW(vk, 0)
    extra = ctypes.c_ulong(0)
    flags = KEYEVENTF_SCANCODE | (KEYEVENTF_KEYUP if up else 0)
    ki = KEYBDINPUT(0, scan, flags, 0, ctypes.pointer(extra))
    inp = INPUT(INPUT_KEYBOARD, _INPUTunion(ki=ki))
    return user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))


def press_key(name, hold=0.0):
    vk = VK[name]
    _send_key(vk, up=False)
    if hold > 0:
        time.sleep(hold)
    _send_key(vk, up=True)


def _abs(x, y):
    # 像素座標 → 0..65535 ABSOLUTE (relative to primary screen)
    ax = int(x * 65535 / (SCREEN_W - 1))
    ay = int(y * 65535 / (SCREEN_H - 1))
    return ax, ay


def _send_mouse(dwFlags, x=0, y=0, data=0):
    extra = ctypes.c_ulong(0)
    mi = MOUSEINPUT(x, y, data, dwFlags, 0, ctypes.pointer(extra))
    inp = INPUT(INPUT_MOUSE, _INPUTunion(mi=mi))
    n = user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))
    return n


def move_to(x, y):
    ax, ay = _abs(x, y)
    return _send_mouse(MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE, ax, ay)


def click_at(x, y, button="left"):
    ax, ay = _abs(x, y)
    _send_mouse(MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE, ax, ay)
    time.sleep(0.05)
    down = MOUSEEVENTF_LEFTDOWN if button == "left" else MOUSEEVENTF_RIGHTDOWN
    up = MOUSEEVENTF_LEFTUP if button == "left" else MOUSEEVENTF_RIGHTUP
    _send_mouse(down | MOUSEEVENTF_ABSOLUTE, ax, ay)
    time.sleep(0.03)
    _send_mouse(up | MOUSEEVENTF_ABSOLUTE, ax, ay)


# ===========================================================
# 截圖 (綠燈①) — DPI-aware 全螢幕, 可選 downscale 給 agent 讀
# ===========================================================
def cmd_shot(args):
    from PIL import ImageGrab
    img = ImageGrab.grab(all_screens=False)
    raw = OUT_DIR / "shot_full.png"
    img.save(raw)
    print(f"✓ 截圖 OK: {img.width}x{img.height} → {raw}")
    # downscale 版給 agent Read (省 token + 夠看)
    if args.scale and args.scale < 1.0:
        small = img.resize((int(img.width * args.scale), int(img.height * args.scale)))
        sp = OUT_DIR / "shot_view.png"
        small.save(sp)
        print(f"✓ 縮圖 ({args.scale}x): {small.width}x{small.height} → {sp}")
    return 0


# ===========================================================
# 點擊 + 截圖 diff (綠燈②) — 點前點後各截一張, 算差異比例
# 物理意義: 驗 SendInput 點擊「真的有打進 Civ6」, 不只信 SendInput 回傳值 (跨層次驗證)。
# 安全: --dry 只移動+log 不真點; 真點前印座標讓 audit。
# ===========================================================
def cmd_click(args):
    from PIL import ImageChops
    hwnd = find_civ6()
    if not hwnd:
        print("✗ 找不到 Civ6 視窗")
        return 1
    x, y = args.x, args.y

    # 安全閘①: WindowFromPoint 確認該座標確實落在 Civ6 (root), 不會誤點到 File Explorer
    raised = foreground(hwnd)
    pt = wintypes.POINT(x, y)
    target_hwnd = user32.WindowFromPoint(pt)
    target_root = root_of(target_hwnd) if target_hwnd else 0
    civ_root = root_of(hwnd)
    on_civ = (target_root == civ_root)
    print(f"  Civ6 hwnd={hwnd} foreground_raised={raised}")
    print(f"  WindowFromPoint({x},{y}) → hwnd={target_hwnd} root={target_root} (Civ6 root={civ_root}) → 在 Civ6 上={on_civ}")
    if not on_civ:
        print(f"⚠ 該座標不在 Civ6 上 (可能被別的視窗蓋住) → 中止點擊, 避免誤點。先確保 Civ6 真前景。")
        return 2

    if args.dry:
        print(f"[dry-run] 想點 ({x},{y}) button={args.button} — 不真點, 僅移動游標到該處供你確認")
        move_to(x, y)
        return 0

    before = capture_window(hwnd)
    before.save(OUT_DIR / "click_before.png")
    print(f"→ 點擊 ({x},{y}) button={args.button}")
    click_at(x, y, args.button)
    time.sleep(args.settle)
    after = capture_window(hwnd)
    after.save(OUT_DIR / "click_after.png")
    # PrintWindow 截圖 diff (DX12-safe, 抓 Civ6 視窗自身內容)
    diff = ImageChops.difference(before.convert("RGB"), after.convert("RGB"))
    bbox = diff.getbbox()
    if bbox is None:
        print("⚠ Civ6 畫面 diff = 0 (完全沒變) → SendInput 點擊可能沒生效, 或點到無反應處")
    else:
        bw, bh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        area_pct = 100.0 * (bw * bh) / (before.width * before.height)
        print(f"✓ Civ6 畫面有變化 — diff bbox={bbox} (~{area_pct:.1f}% 區域) → 點擊大機率生效")
    # 存縮圖供 agent Read
    after.resize((after.width // 2, after.height // 2)).save(OUT_DIR / "click_after_view.png")
    print(f"  before/after 存於 {OUT_DIR} (click_after_view.png 縮圖)")
    return 0


# ===========================================================
# LL mouse hook injected 偵測 (綠燈③④)
# 物理意義: 裝 WH_MOUSE_LL, callback 只讀 MSLLHOOKSTRUCT.flags 的 LLMHF_INJECTED bit + 記一筆,
#   sub-ms 回傳 (callback 超過 LowLevelHooksTimeout=300ms 會被 Windows 靜默跳過)。
#   驗: ③ 自己 SendInput 移動 → 該事件 injected=true; ④ Tim 實體動 → injected=false。
# 數值影響: 純偵測, 不攔不改事件 (CallNextHookEx 照傳)。
# ===========================================================
WH_MOUSE_LL = 14
LLMHF_INJECTED = 0x00000001
WM_MOUSEMOVE = 0x0200


class MSLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [("pt", wintypes.POINT), ("mouseData", wintypes.DWORD),
                ("flags", wintypes.DWORD), ("time", wintypes.DWORD),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]


HOOKPROC = ctypes.CFUNCTYPE(ctypes.c_long, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)


def cmd_hooktest(args):
    kernel32 = ctypes.windll.kernel32
    # ctypes 原型 — 必設, 否則 64-bit handle 被預設 c_int(32-bit) 截斷 → 傳無效 hMod/hook → 失敗
    user32.SetWindowsHookExW.restype = wintypes.HHOOK
    user32.SetWindowsHookExW.argtypes = [ctypes.c_int, HOOKPROC, wintypes.HMODULE, wintypes.DWORD]
    user32.CallNextHookEx.restype = wintypes.LPARAM
    user32.CallNextHookEx.argtypes = [wintypes.HHOOK, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM]
    user32.UnhookWindowsHookEx.argtypes = [wintypes.HHOOK]
    kernel32.GetModuleHandleW.restype = wintypes.HMODULE
    kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
    events = {"injected": 0, "physical": 0, "self_seen": False, "self_injected": None}

    def low_level(nCode, wParam, lParam):
        # callback 鐵律: 只 flag-set, 不做重活 (超 300ms 被 Windows 拔)
        if nCode == 0 and wParam == WM_MOUSEMOVE:
            ms = ctypes.cast(lParam, ctypes.POINTER(MSLLHOOKSTRUCT)).contents
            injected = bool(ms.flags & LLMHF_INJECTED)
            if injected:
                events["injected"] += 1
            else:
                events["physical"] += 1
        return user32.CallNextHookEx(None, nCode, wParam, lParam)

    proc = HOOKPROC(low_level)
    hook = user32.SetWindowsHookExW(WH_MOUSE_LL, proc,
                                    kernel32.GetModuleHandleW(None), 0)
    if not hook:
        print(f"✗ SetWindowsHookExW 失敗, err={ctypes.get_last_error()}")
        return 1
    print(f"✓ WH_MOUSE_LL 裝好 (hook={hook})")

    # message pump — LL hook 必須有 GetMessage loop 才會回呼
    msg = wintypes.MSG()

    def pump(seconds):
        end = time.time() + seconds
        while time.time() < end:
            # PeekMessage 非阻塞, 讓我們能在 pump 之間插 SendInput
            while user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, 1):
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageW(ctypes.byref(msg))
            time.sleep(0.005)

    # ③ 自己 SendInput 移動 (移到螢幕中央附近小幅移動) → 期望 injected=true
    print("→ [③] 本工具 SendInput 移動游標 5 次, 看 hook 是否標 injected...")
    base_inj = events["injected"]
    cx, cy = SCREEN_W // 2, SCREEN_H // 2
    for i in range(5):
        move_to(cx + i * 3, cy + i * 3)
        pump(0.08)
    self_injected_count = events["injected"] - base_inj
    print(f"   自己移動後 injected 計數 +{self_injected_count} (應 >0 = 自己的動作被標 injected ✓)")

    # ④ Tim 實體移動 → 期望 injected=false (physical 計數上升)
    print(f"→ [④] 請 Tim **實體動一下滑鼠** ({args.listen}s 內)... (本工具此期間不送任何 input)")
    base_phys = events["physical"]
    pump(args.listen)
    phys = events["physical"] - base_phys
    print(f"   監聽期間 physical(injected=false) 事件 +{phys} (Tim 有動的話應 >0 ✓)")

    user32.UnhookWindowsHookEx(hook)
    print("✓ hook 卸載")
    print(f"\n=== 結果 ===")
    print(f"  ③ 自己 SendInput → injected=true 計數: {self_injected_count}  {'✅' if self_injected_count > 0 else '❌'}")
    print(f"  ④ Tim 實體動 → injected=false 計數: {phys}  {'✅' if phys > 0 else '⚠ (Tim 沒動或沒偵測到)'}")
    return 0


def cmd_key(args):
    # 綠燈② (鍵盤路徑) — WASD 平移鏡頭, PrintWindow diff. 零遊戲狀態變動, 最安全。
    from PIL import ImageChops
    hwnd = find_civ6()
    if not hwnd:
        print("✗ 找不到 Civ6 視窗")
        return 1
    raised = foreground(hwnd)
    print(f"  Civ6 foreground_raised={raised}")
    if not raised:
        print("⚠ Civ6 沒成功叫前景 → 鍵盤事件不會進遊戲, 中止")
        return 2
    keys = args.keys.lower().split(",")
    for k in keys:
        if k not in VK:
            print(f"✗ 未知鍵 '{k}' (支援: {list(VK)})")
            return 1
    before = capture_window(hwnd)
    before.save(OUT_DIR / "key_before.png")
    print(f"→ 送鍵 {keys} (每鍵 hold {args.hold}s)")
    for k in keys:
        press_key(k, hold=args.hold)
        time.sleep(0.08)
    time.sleep(args.settle)
    after = capture_window(hwnd)
    after.save(OUT_DIR / "key_after.png")
    diff = ImageChops.difference(before.convert("RGB"), after.convert("RGB"))
    bbox = diff.getbbox()
    if bbox is None:
        print("⚠ Civ6 畫面 diff = 0 → 鍵盤 SendInput 可能沒進遊戲 (scancode 不吃?)")
    else:
        bw, bh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        area_pct = 100.0 * (bw * bh) / (before.width * before.height)
        print(f"✓ Civ6 畫面有變化 — diff bbox={bbox} (~{area_pct:.1f}% 區域) → 鍵盤輸入生效")
    after.resize((after.width // 2, after.height // 2)).save(OUT_DIR / "key_after_view.png")
    print(f"  before/after 存於 {OUT_DIR} (key_after_view.png 縮圖)")
    return 0


def cmd_winshot(args):
    hwnd = find_civ6()
    if not hwnd:
        print("✗ 找不到 Civ6 視窗")
        return 1
    x0, y0, w, h = window_rect(hwnd)
    img = capture_window(hwnd)
    img.save(OUT_DIR / "civ_full.png")
    sv = img.resize((int(img.width * args.scale), int(img.height * args.scale)))
    sv.save(OUT_DIR / "civ_view.png")
    print(f"✓ Civ6 PrintWindow 截圖: {w}x{h} at screen({x0},{y0}) → civ_full.png + civ_view.png ({args.scale}x)")
    print(f"  注意: Civ6 視窗在 ({x0},{y0}), 故 full 圖像素 (px,py) → 螢幕座標 ({x0}+px, {y0}+py)")
    return 0


def main():
    p = argparse.ArgumentParser(description="Civ6 桌面操控 POC — 四綠燈去風險")
    sub = p.add_subparsers(dest="cmd", required=True)

    ps = sub.add_parser("shot", help="綠燈① DPI-aware 全螢幕截圖")
    ps.add_argument("--scale", type=float, default=0.5, help="額外存縮圖比例 (預設 0.5)")
    ps.set_defaults(func=cmd_shot)

    pw = sub.add_parser("winshot", help="綠燈① Civ6 視窗 PrintWindow 截圖 (DX12-safe, 不受遮擋)")
    pw.add_argument("--scale", type=float, default=0.5)
    pw.set_defaults(func=cmd_winshot)

    pk = sub.add_parser("key", help="綠燈②(鍵盤) WASD 平移鏡頭 + PrintWindow diff (零狀態變動)")
    pk.add_argument("--keys", default="d", help="逗號分隔, e.g. d 或 d,d,s (支援 w/a/s/d/esc)")
    pk.add_argument("--hold", type=float, default=0.5, help="每鍵按住秒數 (平移距離)")
    pk.add_argument("--settle", type=float, default=0.4)
    pk.set_defaults(func=cmd_key)

    pc = sub.add_parser("click", help="綠燈② SendInput 點擊 + 截圖 diff")
    pc.add_argument("--x", type=int, required=True)
    pc.add_argument("--y", type=int, required=True)
    pc.add_argument("--button", default="left", choices=["left", "right"])
    pc.add_argument("--dry", action="store_true", help="只移動+log 不真點 (dry-run 預覽)")
    pc.add_argument("--settle", type=float, default=0.6, help="點擊後等畫面反應秒數")
    pc.set_defaults(func=cmd_click)

    ph = sub.add_parser("hooktest", help="綠燈③④ LL hook injected 雙向偵測")
    ph.add_argument("--listen", type=float, default=6.0, help="聽 Tim 實體動的秒數")
    ph.set_defaults(func=cmd_hooktest)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
