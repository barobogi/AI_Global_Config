import ctypes, psutil

claude_pids = set()
for p in psutil.process_iter(['pid', 'name', 'exe']):
    try:
        if p.info['exe'] and 'Claude' in p.info['exe'] and 'WindowsApps' in p.info['exe']:
            claude_pids.add(p.info['pid'])
    except Exception:
        pass

buf = ctypes.create_unicode_buffer(512)
class_buf = ctypes.create_unicode_buffer(256)
all_claude_wins = []

def _cb(hwnd, _):
    pid = ctypes.c_ulong()
    ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    if pid.value in claude_pids:
        vis = ctypes.windll.user32.IsWindowVisible(hwnd)
        ctypes.windll.user32.GetClassNameW(hwnd, class_buf, 256)
        ctypes.windll.user32.GetWindowTextW(hwnd, buf, 512)
        all_claude_wins.append((hwnd, pid.value, vis, class_buf.value, buf.value))
    return True

_WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_size_t, ctypes.c_size_t)
ctypes.windll.user32.EnumWindows(_WNDENUMPROC(_cb), 0)

for w in all_claude_wins:
    print(f"HWND={w[0]} | PID={w[1]} | Visible={w[2]} | Class={w[3]} | Title='{w[4]}'")
