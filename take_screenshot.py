import time, ctypes, ctypes.wintypes as wt, sys
from PIL import ImageGrab

user32   = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

def force_foreground(hwnd):
    """Force a window to the foreground bypassing Windows focus-theft protection."""
    fg    = user32.GetForegroundWindow()
    fg_tid = user32.GetWindowThreadProcessId(fg, None)
    my_tid = kernel32.GetCurrentThreadId()
    tgt_tid = user32.GetWindowThreadProcessId(hwnd, None)
    user32.AttachThreadInput(my_tid, fg_tid, True)
    user32.AttachThreadInput(my_tid, tgt_tid, True)
    user32.ShowWindow(hwnd, 3)          # SW_MAXIMIZE
    user32.BringWindowToTop(hwnd)
    user32.SetForegroundWindow(hwnd)
    user32.AttachThreadInput(my_tid, fg_tid, False)
    user32.AttachThreadInput(my_tid, tgt_tid, False)

def find_window(*fragments):
    found = []
    def cb(hwnd, _):
        if user32.IsWindowVisible(hwnd):
            buf = ctypes.create_unicode_buffer(512)
            user32.GetWindowTextW(hwnd, buf, 512)
            if any(f in buf.value for f in fragments):
                found.append(hwnd)
        return True
    PROC = ctypes.WINFUNCTYPE(ctypes.c_bool, wt.HWND, wt.LPARAM)
    user32.EnumWindows(PROC(cb), 0)
    return found[0] if found else None

out_path = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\User\bookkeeping-specialist\screenshot_app.png"

time.sleep(1)
hwnd = find_window("AI Bookkeeping Specialist", "Streamlit", "localhost:8501")
if hwnd:
    force_foreground(hwnd)
    time.sleep(2)

img = ImageGrab.grab()
img.save(out_path)
