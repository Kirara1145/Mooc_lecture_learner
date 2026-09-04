import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TARGET_URL = "https://i.chaoxing.com"

WAIT_SECONDS = 5

CLICK_POINTS = []

CHROME_CANDIDATE_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe".format(
        os.environ.get("USERNAME", "")
    ),
]

CHROME_ARGS = ["--window-size=1920,1080", "--window-position=0,0"]

CATALOG_ROI = (0.72, 0.24, 1.00, 1.00)

TITLE_ROI = (0.05, 0.15, 0.40, 0.32)

VIDEO_CENTER = (0.40, 0.68)

VIDEO_ROI = (0.02, 0.28, 0.72, 0.86)

MAX_PLAY_RETRY = 6

VERIFY_PLAYBACK = True

PLAY_VERIFY_DELAY = 12

COMPLETION_KEYWORDS = ("任务完成", "任务点已完成", "已完成")

COURSE_TIMEOUT = 1800

POLL_INTERVAL = 5

SCROLL_STEPS = -400

SCROLL_UP = 400

MAX_ROLLS = 12

PLAY_BUTTON_TEMPLATE = os.path.join(BASE_DIR, "assets", "play_button.png")

MATCH_THRESHOLD = 0.75

MATCH_SCALE_MIN = 0.5

MATCH_SCALE_MAX = 2.0

MATCH_SCALE_STEP = 0.05

