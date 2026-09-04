import os
import sys

try:
    import ctypes
    from ctypes import wintypes
except ImportError:
    ctypes = None


def _fullscreen_rect():
    import pyautogui

    width, height = pyautogui.size()
    return 0, 0, width, height


def _process_name(pid: int) -> str:
    kernel32 = ctypes.windll.kernel32
    psapi = ctypes.windll.psapi
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

    handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not handle:
        return ""
    try:
        buffer = ctypes.create_unicode_buffer(260)
        size = ctypes.c_ulong(260)
        if psapi.QueryFullProcessImageNameW(handle, 0, buffer, ctypes.byref(size)):
            return os.path.basename(buffer.value).lower()
        return ""
    finally:
        kernel32.CloseHandle(handle)


def _find_chrome_hwnd():
    user32 = ctypes.windll.user32
    found = []

    @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def callback(hwnd, lparam):
        if not user32.IsWindowVisible(hwnd):
            return True
        if user32.GetWindowTextLengthW(hwnd) == 0:
            return True
        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        if _process_name(pid.value) == "chrome.exe":
            found.append(hwnd)
            return False
        return True

    user32.EnumWindows(callback, 0)
    return found[0] if found else None


def _client_rect(hwnd):
    user32 = ctypes.windll.user32
    rect = wintypes.RECT()
    user32.GetClientRect(hwnd, ctypes.byref(rect))
    point = wintypes.POINT(0, 0)
    user32.ClientToScreen(hwnd, ctypes.byref(point))
    return point.x, point.y, rect.right, rect.bottom


def _activate(hwnd) -> None:
    user32 = ctypes.windll.user32
    user32.SetForegroundWindow(hwnd)
    user32.ShowWindow(hwnd, 9)


def get_content_rect():
    if sys.platform != "win32":
        return _fullscreen_rect()

    user32 = ctypes.windll.user32
    hwnd = _find_chrome_hwnd() or user32.GetForegroundWindow()
    if hwnd:
        try:
            _activate(hwnd)
            return _client_rect(hwnd)
        except Exception:
            return _fullscreen_rect()
    return _fullscreen_rect()
