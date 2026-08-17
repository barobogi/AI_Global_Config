import sys, ctypes, time, psutil

window_title = "Claude"
required_process_name = "claude.exe"

def get_process_name(hwnd):
    pid = ctypes.c_ulong()
    ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    if pid.value:
        try:
            return psutil.Process(pid.value).name().lower()
        except Exception:
            pass
    return ""

all_wins = []
BROWSER_INDICATORS = [" - microsoft edge", " - google chrome", " - brave", " - firefox", " - whale"]

def _enum_cb(hwnd, _):
    if not ctypes.windll.user32.IsWindowVisible(hwnd):
        return True
    buf = ctypes.create_unicode_buffer(512)
    ctypes.windll.user32.GetWindowTextW(hwnd, buf, 512)
    title = buf.value.strip().lower()
    if not title:
        return True
    if any(b in title for b in BROWSER_INDICATORS):
        return True
    if window_title.lower() in title:
        pname = get_process_name(hwnd)
        print(f"Matched title candidate: HWND={hwnd}, Title='{buf.value}', Process={pname}")
        if required_process_name and pname != required_process_name.lower():
            print(f"  -> Skipped due to required_process_name mismatch ({pname} != {required_process_name.lower()})")
            return True
        all_wins.append((hwnd, buf.value))
    return True

_WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_size_t, ctypes.c_size_t)
ctypes.windll.user32.EnumWindows(_WNDENUMPROC(_enum_cb), 0)
print("Total all_wins found:", len(all_wins))
