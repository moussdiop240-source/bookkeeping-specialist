import sys, os, subprocess, time, ctypes, ctypes.wintypes as wt
from PIL import Image, ImageGrab

DETACHED = "--detached" in sys.argv
out_path = next((a for a in sys.argv[1:] if not a.startswith("--")),
                r"C:\Users\User\bookkeeping-specialist\screenshot_app.png")

if not DETACHED:
    args = [sys.executable, os.path.abspath(__file__), "--detached", out_path]
    subprocess.Popen(
        args,
        creationflags=0x00000008 | 0x00000200,  # DETACHED_PROCESS | NEW_PROCESS_GROUP
        close_fds=True,
        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    sys.exit(0)

# ── Detached child ──────────────────────────────────────────────────
user32 = ctypes.windll.user32
gdi32  = ctypes.windll.gdi32

def enum_windows():
    results = []
    def cb(hwnd, _):
        if user32.IsWindowVisible(hwnd):
            buf = ctypes.create_unicode_buffer(512)
            user32.GetWindowTextW(hwnd, buf, 512)
            if buf.value:
                results.append((hwnd, buf.value))
        return True
    user32.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, wt.HWND, wt.LPARAM)(cb), 0)
    return results

def capture_hwnd(hwnd, path):
    """Capture a window via PrintWindow — no focus needed, works with GPU-rendered Chrome/Edge."""
    SW_MAXIMIZE = 3
    user32.ShowWindow(hwnd, SW_MAXIMIZE)
    time.sleep(1.5)  # wait for maximize animation and repaint

    rect = wt.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    width  = rect.right  - rect.left
    height = rect.bottom - rect.top
    if width <= 0 or height <= 0:
        return False

    hwndDC = user32.GetWindowDC(hwnd)
    memDC  = gdi32.CreateCompatibleDC(hwndDC)
    bitmap = gdi32.CreateCompatibleBitmap(hwndDC, width, height)
    gdi32.SelectObject(memDC, bitmap)

    # PW_RENDERFULLCONTENT = 2 captures GPU/hardware-accelerated content (Chrome, Edge)
    user32.PrintWindow(hwnd, memDC, 2)

    class BITMAPINFOHEADER(ctypes.Structure):
        _fields_ = [
            ("biSize",          ctypes.c_uint32),
            ("biWidth",         ctypes.c_int32),
            ("biHeight",        ctypes.c_int32),
            ("biPlanes",        ctypes.c_uint16),
            ("biBitCount",      ctypes.c_uint16),
            ("biCompression",   ctypes.c_uint32),
            ("biSizeImage",     ctypes.c_uint32),
            ("biXPelsPerMeter", ctypes.c_int32),
            ("biYPelsPerMeter", ctypes.c_int32),
            ("biClrUsed",       ctypes.c_uint32),
            ("biClrImportant",  ctypes.c_uint32),
        ]

    class BITMAPINFO(ctypes.Structure):
        _fields_ = [("bmiHeader", BITMAPINFOHEADER), ("bmiColors", ctypes.c_uint32 * 3)]

    bmi = BITMAPINFO()
    bmi.bmiHeader.biSize        = ctypes.sizeof(BITMAPINFOHEADER)
    bmi.bmiHeader.biWidth       = width
    bmi.bmiHeader.biHeight      = -height  # negative = top-down bitmap
    bmi.bmiHeader.biPlanes      = 1
    bmi.bmiHeader.biBitCount    = 32
    bmi.bmiHeader.biCompression = 0  # BI_RGB

    buf = (ctypes.c_byte * (width * height * 4))()
    gdi32.GetDIBits(memDC, bitmap, 0, height, buf, ctypes.byref(bmi), 0)

    img = Image.frombytes("RGBA", (width, height), bytes(buf), "raw", "BGRA")
    img.save(path)

    gdi32.DeleteObject(bitmap)
    gdi32.DeleteDC(memDC)
    user32.ReleaseDC(hwnd, hwndDC)
    return True

time.sleep(2)

browser_fragments = [
    "AI Bookkeeping Specialist", "localhost:8501", "bookkeeping-specialist",
    "Streamlit", "index.html", "GitHub",
]

all_wins = enum_windows()
target = None

# Priority: app-specific titles first
for hwnd, title in all_wins:
    if any(f in title for f in browser_fragments):
        target = hwnd
        break

# Fallback: any Chrome / Edge / Firefox window
if not target:
    for hwnd, title in all_wins:
        if any(b in title for b in ("Chrome", "Edge", "Firefox")):
            target = hwnd
            break

if target:
    ok = capture_hwnd(target, out_path)
    if ok:
        sys.exit(0)

# Last resort: full-screen grab
ImageGrab.grab().save(out_path)
