import re
import time

import catalog
import config
import ocr_engine
import screen
import template
from logger import get_logger

logger = get_logger("study")


def mission_status() -> str:
    complete = template.find_complete()
    incomplete = template.find_incomplete()

    if complete and incomplete:
        return "complete" if complete[2] >= incomplete[2] else "incomplete"
    if complete:
        logger.info(f"[图像匹配] 检测到任务已完成 ({complete[0]}, {complete[1]}) score={complete[2]:.3f}")
        return "complete"
    if incomplete:
        logger.info(f"[图像匹配] 检测到任务未完成 ({incomplete[0]}, {incomplete[1]}) score={incomplete[2]:.3f}")
        return "incomplete"
    return "unknown"


def is_completed() -> bool:
    return mission_status() == "complete"


def is_playing() -> bool:
    img = screen.screenshot()
    result = ocr_engine.recognize_roi(img, config.VIDEO_ROI)
    text = "".join(catalog.normalize(t) for t in result["txts"])
    match = re.search(r"(\d+):(\d+)", text)
    if match:
        seconds = int(match.group(1)) * 60 + int(match.group(2))
        return seconds > 0
    return False


def click_play_button() -> bool:
    cx, cy = screen.frac_point(*config.VIDEO_CENTER)

    offsets = (0, 0), (-40, 0), (40, 0), (0, -40), (0, 40), (0, -80), (0, 80)

    def click_once(attempt: int) -> None:
        matched = template.find_template(config.VIDEO_ROI)
        if matched:
            x, y, score = matched
            logger.info(f"[图像匹配] 播放按钮 ({x}, {y}) score={score:.3f}")
        else:
            dx, dy = offsets[attempt % len(offsets)]
            x, y = cx + dx, cy + dy
            logger.info(f"[坐标回退] 点击 ({x}, {y})")
        screen.click(x, y)

    if not config.VERIFY_PLAYBACK:
        click_once(0)
        logger.info("已关闭播放验证，视为开始播放")
        return True

    for attempt in range(config.MAX_PLAY_RETRY):
        click_once(attempt)
        time.sleep(config.PLAY_VERIFY_DELAY)
        if is_playing():
            logger.info("视频开始播放")
            return True

    logger.info("未能确认视频开始播放，请人工检查")
    return False


def wait_completion(timeout: int) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if is_completed():
            return True
        time.sleep(config.POLL_INTERVAL)
    return False


def run() -> None:
    catalog.scroll_to_top()

    leaf_numbers = catalog.collect_leaf_numbers()
    if not leaf_numbers:
        logger.info("未识别到最低级课程编号，请确认已登录并停留在学习通课程页")
        return

    catalog.scroll_to_top()

    done = set()

    while True:
        items = catalog.visible_items()
        if not items:
            logger.info("右侧目录无课程项，结束")
            break

        target = None
        for item in items:
            number = catalog.parse_number(item[0])
            if number is not None and number in leaf_numbers and number not in done:
                target = item
                break

        if target is None:
            before = [t for t, _, _ in items]
            screen.scroll_in_roi(config.CATALOG_ROI, config.SCROLL_STEPS)
            time.sleep(1)
            after = [t for t, _, _ in catalog.visible_items()]
            if not after or after == before:
                logger.info("目录已到底，结束")
                break
            continue

        title, cx, cy = target
        number = catalog.parse_number(title)
        logger.info(f"处理课程: {title}")

        screen.click(cx, cy)
        time.sleep(config.WAIT_SECONDS)

        status = mission_status()
        for _ in range(3):
            if status != "unknown":
                break
            time.sleep(2)
            status = mission_status()

        if status == "complete":
            logger.info("已显示任务完成，跳过")
        elif status == "unknown":
            logger.info(f"无法确认任务状态: {title}，请人工检查")
        else:
            click_play_button()
            if wait_completion(config.COURSE_TIMEOUT):
                logger.info(f"完成: {title}")
            else:
                logger.info(f"超时未完成: {title}，请人工处理，处理后按回车继续")
                input()

        done.add(number)
        logger.info(f"已处理 {len(done)} 项")

    logger.info("全部课程处理完毕")


if __name__ == "__main__":
    run()
