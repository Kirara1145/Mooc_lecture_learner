import os

import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(BASE_DIR, "config.yaml")


def _load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    template = data.get("play_button_template")
    if template:
        data["PLAY_BUTTON_TEMPLATE"] = os.path.join(BASE_DIR, template)
    data.pop("play_button_template", None)

    username = os.environ.get("USERNAME", "")
    paths = data.get("CHROME_CANDIDATE_PATHS") or []
    data["CHROME_CANDIDATE_PATHS"] = [
        path.replace("${USERNAME}", username) if isinstance(path, str) else path
        for path in paths
    ]

    return data

TITLE_ROI = (0.05, 0.15, 0.40, 0.32)

VIDEO_CENTER = (0.40, 0.68)

VIDEO_ROI = (0.02, 0.28, 0.72, 0.86)

MAX_PLAY_RETRY = 6

VERIFY_PLAYBACK = False

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

for _key, _value in _load_config().items():
    globals()[_key] = _value
