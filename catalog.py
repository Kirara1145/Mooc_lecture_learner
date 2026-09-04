import re
import time

import config
import ocr_engine
import screen

ITEM_RE = re.compile(r"^\d")
LETTER_RE = re.compile(r"[\u4e00-\u9fa5A-Za-z]")


def normalize(text: str) -> str:
    text = re.sub(r"\s+", "", text)
    return text.replace("…", "").replace("...", "")


def is_catalog_item(text: str) -> bool:
    if len(text) < 2:
        return False
    if not ITEM_RE.match(text):
        return False
    return bool(LETTER_RE.search(text))


def _visible_titles() -> list:
    img = screen.screenshot()
    result = ocr_engine.recognize_roi(img, config.CATALOG_ROI)
    titles = []
    for text in result["txts"]:
        text = normalize(text)
        if text and is_catalog_item(text):
            titles.append(text)
    return titles


def collect_catalog() -> list:
    titles = []
    seen = set()
    prev = None

    for _ in range(config.MAX_ROLLS):
        visible = _visible_titles()
        current = frozenset(visible)

        if current == prev:
            break
        prev = current

        for title in visible:
            if title not in seen:
                seen.add(title)
                titles.append(title)

        if not visible:
            break

        screen.scroll_in_roi(config.CATALOG_ROI, config.SCROLL_STEPS)
        time.sleep(1)

    print(f"[catalog] 收集到 {len(titles)} 个课程项")
    return titles


def locate_item(title: str):
    img = screen.screenshot()
    result = ocr_engine.recognize_roi(img, config.CATALOG_ROI)

    for text, box in zip(result["txts"], result["boxes"]):
        text = normalize(text)
        if not text:
            continue
        if text == title or title in text or text in title:
            cx = int(box[:, 0].mean())
            cy = int(box[:, 1].mean())
            return cx, cy
    return None
