import time

import browser
import config
import ocr_engine
import screen
from logger import get_logger

logger = get_logger("main")


def main() -> None:
    browser.open_url()

    logger.info(f"等待页面加载 {config.WAIT_SECONDS} 秒...")
    time.sleep(config.WAIT_SECONDS)

    logger.info("正在截图...")
    img = screen.screenshot()

    logger.info("正在进行 OCR 识别...")
    result = ocr_engine.recognize(img)

    logger.info("识别结果:")
    for txt, score in zip(result["txts"], result["scores"]):
        logger.info(f"  {txt}  (置信度: {score:.4f})")

    if config.CLICK_POINTS:
        logger.info("开始按坐标点击...")
        screen.click_all(config.CLICK_POINTS)
    else:
        logger.info("未配置点击坐标，跳过点击步骤")


if __name__ == "__main__":
    main()
