import sys

import numpy as np
import pyautogui

import window


def _enable_dpi_awareness() -> None:
    if sys.platform != "win32":
        return
    import ctypes

    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


_enable_dpi_awareness()

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5


def screenshot() -> np.ndarray:
    img = pyautogui.screenshot()
    return np.array(img)


def click(x: int, y: int) -> None:
    print(f"[screen] 点击坐标: ({x}, {y})")
    pyautogui.click(x, y)


def click_all(points) -> None:
    for point in points:
        x, y = point
        click(x, y)


def screen_size() -> tuple:
    width, height = pyautogui.size()
    return width, height


def content_rect() -> tuple:
    return window.get_content_rect()


def frac_point(x: float, y: float) -> tuple:
    left, top, width, height = content_rect()
    return int(left + x * width), int(top + y * height)


def click_frac(x: float, y: float) -> None:
    sx, sy = frac_point(x, y)
    click(sx, sy)


def crop_roi(img: np.ndarray, roi) -> np.ndarray:
    left, top, width, height = content_rect()
    x1, y1, x2, y2 = roi
    x1 = int(left + x1 * width)
    y1 = int(top + y1 * height)
    x2 = int(left + x2 * width)
    y2 = int(top + y2 * height)
    return img[y1:y2, x1:x2]


def roi_origin(roi) -> tuple:
    left, top, width, height = content_rect()
    x1, y1, _, _ = roi
    return int(left + x1 * width), int(top + y1 * height)


def scroll_in_roi(roi, steps: int) -> None:
    x1, y1, x2, y2 = roi
    cx, cy = frac_point((x1 + x2) / 2, (y1 + y2) / 2)
    pyautogui.moveTo(cx, cy)
    pyautogui.scroll(steps)
