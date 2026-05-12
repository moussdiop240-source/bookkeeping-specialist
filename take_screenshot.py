import time, ctypes, ctypes.wintypes as wt, sys
from PIL import ImageGrab

user32   = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

def force_foreground(hwnd):
    fg     = user32.GetForegroundWindow()
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

def send_key(vk, extended=False):
    """Simulate a key press + release."""
    flags = 0x0001 if extended else 0
    user32.keybd_event(vk, 0, flags, 0)
    time.sleep(0.05)
    user32.keybd_event(vk, 0, flags | 0x0002, 0)  # KEYEVENTF_KEYUP

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
refresh  = "--refresh" in sys.argv

time.sleep(1)
hwnd = find_window("AI Bookkeeping Specialist", "Streamlit", "localhost:8501")
if hwnd:
    force_foreground(hwnd)
    time.sleep(1)
    if refresh:
        # Ctrl+R: navigate active Chrome tab to fresh load
        VK_CTRL = 0x11
        VK_R    = 0x52
        user32.keybd_event(VK_CTRL, 0, 0, 0)
        send_key(VK_R)
        user32.keybd_event(VK_CTRL, 0, 0x0002, 0)
        time.sleep(4)  # wait for page to reload

img = ImageGrab.grab()
img.save(out_path)
