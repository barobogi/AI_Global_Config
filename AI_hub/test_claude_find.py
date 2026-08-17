import ctypes, psutil

claude_pids = set()
for p in psutil.process_iter(['pid', 'name', 'exe']):
    try:
        if p.info['exe'] and 'Claude' in p.info['exe'] and 'WindowsApps' in p.info['exe']:
            claude_pids.add(p.info['pid'])
    except Exception:
        pass

print("Claude Desktop PIDs:", claude_pids)

buf = ctypes.create_unicode_buffer(512)
class_buf = ctypes.create_unicode_buffer(256)
found_hwnds = []

def _cb(hwnd, _):
    pid = ctypes.c_ulong()
    ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    if pid.value in claude_pids:
        if ctypes.windll.user32.IsWindowVisible(hwnd):
            ctypes.windll.user32.GetClassNameW(hwnd, class_buf, 256)
            ctypes.windll.user32.GetWindowTextW(hwnd, buf, 512)
            # Top-level Electron window class is Chrome_WidgetWin_1
            if class_buf.value == "Chrome_WidgetWin_1":
                found_hwnds.append(hwnd)
                print(f"FOUND CLAUDE DESKTOP WINDOW! HWND={hwnd}, Class={class_buf.value}, Title='{buf.value}'")
    return True

_WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_size_t, ctypes.c_size_t)
ctypes.windll.user32.EnumWindows(_WNDENUMPROC(_cb), 0)
print("Found Claude HWNDs:", found_hwnds)
