import os
import subprocess
import sys

import config
from logger import get_logger

logger = get_logger("browser")


def find_chrome() -> str:
    for path in config.CHROME_CANDIDATE_PATHS:
        if path and os.path.isfile(path):
            return path

    raise FileNotFoundError(
        "未找到 Chrome 浏览器，请在 config.py 的 CHROME_CANDIDATE_PATHS 中添加 chrome.exe 路径"
    )


def open_url(url: str = None) -> subprocess.Popen:
    url = url or config.TARGET_URL
    chrome = find_chrome()

    proc = subprocess.Popen([chrome, *config.CHROME_ARGS, url])

    if proc.poll() is not None:
        raise RuntimeError("Chrome 启动失败")

    logger.info(f"已启动 Chrome: {url}")
    return proc


if __name__ == "__main__":
    try:
        open_url()
    except Exception as exc:
        logger.error(f"{exc}")
        sys.exit(1)
