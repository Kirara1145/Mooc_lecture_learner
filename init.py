import ctypes
import os
import subprocess
import sys

import browser

SW_HIDE = 0


def _require_windows() -> None:
    if sys.platform != "win32":
        raise RuntimeError("本程序仅在 Windows 平台运行")


def _console_hwnd() -> int:
    return ctypes.windll.kernel32.GetConsoleWindow()


def hide_console() -> None:
    hwnd = _console_hwnd()
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, SW_HIDE)


def wait_input() -> None:
    input("请在浏览器中登录学习通，登录完成后在此输入任意内容并回车： ")


def launch_main() -> None:
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "study.py")
    subprocess.Popen([sys.executable, script])


def main() -> None:
    _require_windows()

    browser.open_url()

    wait_input()

    hide_console()

    launch_main()


if __name__ == "__main__":
    main()
