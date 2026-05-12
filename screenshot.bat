@echo off
cd /d "%~dp0"
python -c "
import time, ctypes, ctypes.wintypes as wt
from PIL import ImageGrab

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

time.sleep(1)

found = []
def cb(hwnd, _):
    if user32.IsWindowVisible(hwnd):
        buf = ctypes.create_unicode_buffer(512)
        user32.GetWindowTextW(hwnd, buf, 512)
        t = buf.value
        if t and ('Chrome' in t or 'Edge' in t or 'Firefox' in t):
            found.append((hwnd, t))
    return True
user32.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, wt.HWND, wt.LPARAM)(cb), 0)

if found:
    hwnd = found[0][0]
    fg = user32.GetForegroundWindow()
    fg_tid = user32.GetWindowThreadProcessId(fg, None)
    my_tid = kernel32.GetCurrentThreadId()
    tgt_tid = user32.GetWindowThreadProcessId(hwnd, None)
    user32.AttachThreadInput(my_tid, fg_tid, True)
    user32.AttachThreadInput(my_tid, tgt_tid, True)
    user32.ShowWindow(hwnd, 3)
    user32.BringWindowToTop(hwnd)
    user32.SetForegroundWindow(hwnd)
    user32.AttachThreadInput(my_tid, fg_tid, False)
    user32.AttachThreadInput(my_tid, tgt_tid, False)
    time.sleep(1.5)

ImageGrab.grab().save(r'C:\Users\User\bookkeeping-specialist\screenshot_app.png')
print('Screenshot saved.')
"
