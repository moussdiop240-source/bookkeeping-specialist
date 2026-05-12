import sys, os, subprocess, time, ctypes, ctypes.wintypes as wt
from PIL import ImageGrab

DETACHED = "--detached" in sys.argv
out_path = next((a for a in sys.argv[1:] if not a.startswith("--")),
                r"C:\Users\User\bookkeeping-specialist\screenshot_app.png")
refresh  = "--refresh" in sys.argv

if not DETACHED:
    # Spawn independent child, exit immediately so terminal stops being active
    args = [sys.executable, os.path.abspath(__file__), "--detached", out_path]
    if refresh:
        args.append("--refresh")
    subprocess.Popen(
        args,
        creationflags=0x00000008 | 0x00000200,  # DETACHED_PROCESS | NEW_PROCESS_GROUP
        close_fds=True,
        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    sys.exit(0)

# ── Detached child ──────────────────────────────────────────────────
user32   = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

SW_MINIMIZE = 6
SW_RESTORE  = 9
SW_MAXIMIZE = 3

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

time.sleep(1.5)

all_wins = enum_windows()

# Step 1: minimize Claude Code / terminal windows
terminal_fragments = ["Build new features", "Claude Code", "claude.exe", "Windows PowerShell", "cmd.exe"]
for hwnd, title in all_wins:
    if any(f in title for f in terminal_fragments):
        user32.ShowWindow(hwnd, SW_MINIMIZE)

time.sleep(0.8)

# Step 2: find and foreground the browser with our page
browser_fragments = [
    "AI Bookkeeping Specialist", "localhost:8501", "bookkeeping-specialist",
    "GitHub", "Streamlit",
]
target = None
for hwnd, title in all_wins:
    if any(f in title for f in browser_fragments):
        target = hwnd
        break

# Fallback: any visible Chrome/Edge window
if not target:
    for hwnd, title in all_wins:
        if "Chrome" in title or "Edge" in title:
            target = hwnd
            break

if target:
    fg      = user32.GetForegroundWindow()
    fg_tid  = user32.GetWindowThreadProcessId(fg, None)
    my_tid  = kernel32.GetCurrentThreadId()
    tgt_tid = user32.GetWindowThreadProcessId(target, None)
    user32.AttachThreadInput(my_tid, fg_tid,  True)
    user32.AttachThreadInput(my_tid, tgt_tid, True)
    user32.ShowWindow(target, SW_MAXIMIZE)
    user32.BringWindowToTop(target)
    user32.SetForegroundWindow(target)
    user32.AttachThreadInput(my_tid, fg_tid,  False)
    user32.AttachThreadInput(my_tid, tgt_tid, False)
    time.sleep(1.5)

    if refresh:
        VK_CTRL, VK_R = 0x11, 0x52
        user32.keybd_event(VK_CTRL, 0, 0, 0)
        user32.keybd_event(VK_R,    0, 0, 0)
        time.sleep(0.05)
        user32.keybd_event(VK_R,    0, 2, 0)
        user32.keybd_event(VK_CTRL, 0, 2, 0)
        time.sleep(4)

ImageGrab.grab().save(out_path)
