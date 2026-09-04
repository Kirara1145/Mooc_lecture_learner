import time

import browser
import config
import ocr_engine
import screen


def main() -> None:
    browser.open_url()

    print(f"[main] 等待页面加载 {config.WAIT_SECONDS} 秒...")
    time.sleep(config.WAIT_SECONDS)

    print("[main] 正在截图...")
    img = screen.screenshot()

    print("[main] 正在进行 OCR 识别...")
    result = ocr_engine.recognize(img)

    print("[main] 识别结果:")
    for txt, score in zip(result["txts"], result["scores"]):
        print(f"  {txt}  (置信度: {score:.4f})")

    if config.CLICK_POINTS:
        print("[main] 开始按坐标点击...")
        screen.click_all(config.CLICK_POINTS)
    else:
        print("[main] 未配置点击坐标，跳过点击步骤")


if __name__ == "__main__":
    main()
