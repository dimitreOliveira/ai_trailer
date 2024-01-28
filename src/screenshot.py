import logging
from pathlib import Path

import cv2

from common import SCREENSHOT_DIR, configs


def create_screeshots(movie_path: str, n_screenshot: int, screenshot_dir: Path) -> None:
    """Take multiple screenshots from a video file.

    Args:
        movie_path (str): Path to the movie file
        n_screenshot (int): Number of screenshots that will be taken
        screenshot_dir (Path): Directory to save the screenshots
    """
    if not screenshot_dir.exists():
        screenshot_dir.mkdir(parents=True, exist_ok=True)

    cam = cv2.VideoCapture(movie_path)

    total_frames = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))

    currentframe = 0

    while True:
        ret, frame = cam.read()
        if ret:
            img_name = f"frame_{currentframe}.jpg"
            if currentframe % (total_frames // n_screenshot) == 0:
                cv2.imwrite(f"{screenshot_dir}/{img_name}", frame)
            currentframe += 1
        else:
            break

    cam.release()
    cv2.destroyAllWindows()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

logger.info("##### Starting step 3 frame sampling #####")

create_screeshots(configs["movie_path"], configs["n_screenshot"], SCREENSHOT_DIR)
