import os
import re
import time

import catalog
import config
import ocr_engine
import screen
import template

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
        matched = template.find_template(config.VIDEO_ROI)
        if matched:
            x, y, score = matched
            log(f"[图像匹配] 播放按钮 ({x}, {y}) score={score:.3f}")
            screen.click(x, y)
        else:
            dx, dy = offsets[attempt % len(offsets)]
            x, y = cx + dx, cy + dy
            log(f"[坐标回退] 点击 ({x}, {y})")
            screen.click(x, y)

        time.sleep(config.POLL_INTERVAL)
        if is_playing():
            log("视频开始播放")
            return True

    log("未能确认视频开始播放，请人工检查")
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

    done = set()

    while True:
        items = catalog.visible_items()
        if not items:
            log("右侧目录无课程项，结束")
            break

        target = None
        for item in items:
            if item[0] not in done:
                target = item
                break

        if target is None:
            before = [t for t, _, _ in items]
            screen.scroll_in_roi(config.CATALOG_ROI, config.SCROLL_STEPS)
            time.sleep(1)
            after = [t for t, _, _ in catalog.visible_items()]
            if not after or after == before:
                log("目录已到底，结束")
                break
            continue

        title, cx, cy = target
        log(f"处理课程: {title}")

        screen.click(cx, cy)
        time.sleep(config.WAIT_SECONDS)

        if is_completed():
            log("已显示任务完成，跳过")
        else:
            click_play_button()
            if wait_completion(config.COURSE_TIMEOUT):
                log(f"完成: {title}")
            else:
                log(f"超时未完成: {title}，请人工处理，处理后按回车继续")
                input()

        done.add(title)
        log(f"已处理 {len(done)} 项")

    log("全部课程处理完毕")


if __name__ == "__main__":
    run()
