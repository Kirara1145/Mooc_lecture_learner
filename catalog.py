import re
import time

import config
import ocr_engine
import screen
from logger import get_logger

logger = get_logger("catalog")

ITEM_RE = re.compile(r"^\d")
LETTER_RE = re.compile(r"[\u4e00-\u9fa5A-Za-z]")
NUMBER_RE = re.compile(r"^\s*(\d+(?:\.\d+)*)")


def normalize(text: str) -> str:
    text = re.sub(r"\s+", "", text)
    return text.replace("…", "").replace("...", "")


def is_catalog_item(text: str) -> bool:
    if len(text) < 2:
        return False
    if not ITEM_RE.match(text):
        return False
    return bool(LETTER_RE.search(text))


def parse_number(text: str):
    match = NUMBER_RE.match(text)
    if not match:
        return None
    return tuple(int(part) for part in match.group(1).split("."))


def filter_leaves(numbers: set) -> set:
    nums = list(numbers)
    leaves = set()
    for number in nums:
        if not any(
            len(other) > len(number) and other[: len(number)] == number
            for other in nums
        ):
            leaves.add(number)
    return leaves


def _visible_titles() -> list:
    img = screen.screenshot()
    result = ocr_engine.recognize_roi(img, config.CATALOG_ROI)
    titles = []
    for text in result["txts"]:
        text = normalize(text)
        if text and is_catalog_item(text):
            titles.append(text)
    return titles


def collect_leaf_numbers() -> set:
    numbers = set()
    prev = None

    for _ in range(config.MAX_ROLLS):
        visible = _visible_titles()
        current = frozenset(visible)

        if current == prev:
            break
        prev = current

        for text in visible:
            number = parse_number(text)
            if number is not None:
                numbers.add(number)

        screen.scroll_in_roi(config.CATALOG_ROI, config.SCROLL_STEPS)
        time.sleep(1)

    leaves = filter_leaves(numbers)
    logger.info(f"共识别 {len(numbers)} 个编号，其中最低级 {len(leaves)} 个")
    return leaves


def visible_items() -> list:
    img = screen.screenshot()
    result = ocr_engine.recognize_roi(img, config.CATALOG_ROI)

    items = []
    for text, box in zip(result["txts"], result["boxes"]):
        text = normalize(text)
        if text and is_catalog_item(text):
            cx = int(box[:, 0].mean())
            cy = int(box[:, 1].mean())
            items.append((text, cx, cy))

    items.sort(key=lambda item: item[2])
    return items


def scroll_to_top() -> None:
    prev = None
    for _ in range(config.MAX_ROLLS):
        current = frozenset(_visible_titles())
        if prev is not None and current == prev:
            break
        prev = current
        screen.scroll_in_roi(config.CATALOG_ROI, config.SCROLL_UP)
        time.sleep(1)
