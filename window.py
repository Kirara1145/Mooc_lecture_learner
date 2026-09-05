import sys

try:
    import ctypes
    from ctypes import wintypes
except Exception:
    ctypes = None

CHROME_CLASS_NAMES = ("Chrome_WidgetWin_1", "Chrome_WidgetWin_0")

_user32 = None


def _get_user32():
    global _user32
    if _user32 is not None:
        return _user32

    user32 = ctypes.windll.user32

    user32.IsWindowVisible.argtypes = [wintypes.HWND]
    user32.IsWindowVisible.restype = wintypes.BOOL
    user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
    user32.GetWindowTextLengthW.restype = ctypes.c_int
    user32.GetClassNameW.argtypes = [wintypes.HWND, ctypes.c_wchar_p, ctypes.c_int]
    user32.GetClassNameW.restype = ctypes.c_int
    user32.GetClientRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
    user32.GetClientRect.restype = wintypes.BOOL
    user32.ClientToScreen.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.POINT)]
    user32.ClientToScreen.restype = wintypes.BOOL
    user32.SetForegroundWindow.argtypes = [wintypes.HWND]
    user32.SetForegroundWindow.restype = wintypes.BOOL
    user32.ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
    user32.ShowWindow.restype = wintypes.BOOL

    _user32 = user32
    return user32


def _fullscreen_rect():
    import pyautogui

    width, height = pyautogui.size()
    return 0, 0, width, height


def _is_chrome_window(user32, hwnd) -> bool:
    if not user32.IsWindowVisible(hwnd):
        return False
    if user32.GetWindowTextLengthW(hwnd) <= 0:
        return False
    buf = ctypes.create_unicode_buffer(256)
    if user32.GetClassNameW(hwnd, buf, len(buf)) == 0:
        return False
    return buf.value in CHROME_CLASS_NAMES


def _find_chrome_hwnd():
    user32 = _get_user32()

    foreground = user32.GetForegroundWindow()
    if foreground and _is_chrome_window(user32, foreground):
        return foreground

    found = []

    @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def callback(hwnd, lparam):
        if _is_chrome_window(user32, hwnd):
            found.append(hwnd)
            return False
        return True

    user32.EnumWindows(callback, 0)
    return found[0] if found else None


def _client_rect(hwnd):
    user32 = _get_user32()
    rect = wintypes.RECT()
    user32.GetClientRect(hwnd, ctypes.byref(rect))
    point = wintypes.POINT(0, 0)
    user32.ClientToScreen(hwnd, ctypes.byref(point))
    return point.x, point.y, rect.right, rect.bottom


def _activate(hwnd) -> None:
    user32 = _get_user32()
    user32.ShowWindow(hwnd, 9)
    user32.SetForegroundWindow(hwnd)


def get_content_rect():
    if sys.platform != "win32":
        return _fullscreen_rect()

    try:
        hwnd = _find_chrome_hwnd()
        if not hwnd:
            return _fullscreen_rect()
        _activate(hwnd)
        return _client_rect(hwnd)
    except Exception:
        return _fullscreen_rect()
