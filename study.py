import os
import re
import time

import catalog
import config
import ocr_engine
import screen

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "study.log")


def log(message: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {message}"
    print(line)
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass


def is_completed() -> bool:
    img = screen.screenshot()
    result = ocr_engine.recognize_roi(img, config.TITLE_ROI)
    text = "".join(catalog.normalize(t) for t in result["txts"])
    for keyword in config.COMPLETION_KEYWORDS:
        if keyword.replace(" ", "") in text:
            return True
    return False


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

    for attempt in range(config.MAX_PLAY_RETRY):
        dx, dy = offsets[attempt % len(offsets)]
        x, y = cx + dx, cy + dy
        log(f"尝试点击播放按钮 ({x}, {y})")
        screen.click(x, y)
        time.sleep(config.POLL_INTERVAL)
        if is_playing():
            log("视频开始播放")
            return True

    log("未能确认视频开始播放，请人工检查")
    return False


def click_item(title: str) -> bool:
    for _ in range(5):
        pos = catalog.locate_item(title)
        if pos:
            log(f"点击课程项 {title} 于 {pos}")
            screen.click(*pos)
            return True
        time.sleep(1)
    log(f"未能定位课程项: {title}")
    return False


def wait_completion(timeout: int) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if is_completed():
            return True
        time.sleep(config.POLL_INTERVAL)
    return False


def run() -> None:
    titles = catalog.collect_catalog()
    if not titles:
        log("右侧目录未识别到课程项，请确认已登录并停留在学习通课程页")
        return

    for title in titles:
        log(f"处理课程: {title}")

        if is_completed():
            log("该课程已刷过，跳过")
            continue

        if not click_item(title):
            continue
        time.sleep(config.WAIT_SECONDS)

        if is_completed():
            log("已显示完成状态，跳过播放")
            continue

        click_play_button()

        if wait_completion(config.COURSE_TIMEOUT):
            log(f"完成: {title}")
        else:
            log(f"超时未完成: {title}，请人工处理，处理后按回车继续")
            input()

    log("全部课程处理完毕")


if __name__ == "__main__":
    run()
