TARGET_URL = "https://i.chaoxing.com"

WAIT_SECONDS = 5

CLICK_POINTS = []

CHROME_CANDIDATE_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe".format(
        __import__("os").environ.get("USERNAME", "")
    ),
]

CHROME_ARGS = ["--window-size=1920,1080", "--window-position=0,0"]

CATALOG_ROI = (0.72, 0.24, 1.00, 1.00)

TITLE_ROI = (0.05, 0.15, 0.40, 0.32)

VIDEO_CENTER = (0.40, 0.68)

VIDEO_ROI = (0.02, 0.28, 0.72, 0.86)

MAX_PLAY_RETRY = 6

COMPLETION_KEYWORDS = ("任务完成", "任务点已完成", "已完成")

COURSE_TIMEOUT = 1800

POLL_INTERVAL = 5

SCROLL_STEPS = -400

MAX_ROLLS = 12
