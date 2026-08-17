import ctypes, psutil, sys
sys.stdout.reconfigure(encoding='utf-8')

buf = ctypes.create_unicode_buffer(512)
class_buf = ctypes.create_unicode_buffer(256)

def _cb(hwnd, _):
    if ctypes.windll.user32.IsWindowVisible(hwnd):
        ctypes.windll.user32.GetWindowTextW(hwnd, buf, 512)
        ctypes.windll.user32.GetClassNameW(hwnd, class_buf, 256)
        t = buf.value.strip()
        c = class_buf.value.strip()
        pid = ctypes.c_ulong()
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        try:
            pname = psutil.Process(pid.value).name()
        except Exception:
            pname = ""
        # Filter noise
        if t or "Chrome_Widget" in c or "ApplicationFrame" in c:
            print(f"HWND: {hwnd:8d} | PID: {pid.value:5d} | Proc: {pname:20s} | Class: {c:25s} | Title: '{t}'")
    return True

_WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_size_t, ctypes.c_size_t)
ctypes.windll.user32.EnumWindows(_WNDENUMPROC(_cb), 0)
