import cv2
import numpy as np

import config
import screen

_template_cache = None


def _load_template():
    global _template_cache
    if _template_cache is None:
        _template_cache = cv2.imread(config.PLAY_BUTTON_TEMPLATE, cv2.IMREAD_GRAYSCALE)
        if _template_cache is None:
            raise FileNotFoundError(
                f"无法加载播放按钮模板: {config.PLAY_BUTTON_TEMPLATE}"
            )
    return _template_cache


def find_template(roi=None):
    tpl = _load_template()
    template_h, template_w = tpl.shape

    img = screen.screenshot()
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img

    left, top, width, height = screen.content_rect()
    if roi is None:
        region = gray
        ox = oy = 0
    else:
        x1, y1, x2, y2 = roi
        rx1 = int(left + x1 * width)
        ry1 = int(top + y1 * height)
        rx2 = int(left + x2 * width)
        ry2 = int(top + y2 * height)
        region = gray[ry1:ry2, rx1:rx2]
        ox, oy = rx1, ry1

    if region.size == 0:
        return None

    region_h, region_w = region.shape
    best_score = -1.0
    best = None

    scale = config.MATCH_SCALE_MIN
    while scale <= config.MATCH_SCALE_MAX:
        new_w = max(int(template_w * scale), 8)
        new_h = max(int(template_h * scale), 8)
        if new_w >= region_w or new_h >= region_h:
            scale += config.MATCH_SCALE_STEP
            continue

        resized = cv2.resize(tpl, (new_w, new_h), interpolation=cv2.INTER_AREA)
        result = cv2.matchTemplate(region, resized, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val > best_score:
            best_score = max_val
            best = (max_loc[0], max_loc[1], new_w, new_h)

        scale += config.MATCH_SCALE_STEP

    if best is None or best_score < config.MATCH_THRESHOLD:
        return None

    loc_x, loc_y, new_w, new_h = best
    center_x = ox + loc_x + new_w // 2
    center_y = oy + loc_y + new_h // 2
    return center_x, center_y, best_score
