import logging
import shutil

import cv2

from common import FRAMES_DIR, configs


def create_screeshots(video_path: str, n_frames: int) -> None:
    """Take multiple frames from a video file.

    Args:
        video_path (str): Path to the video file
        n_frames (int): Number of frames that will be taken
    """
    if FRAMES_DIR.exists():
        shutil.rmtree(FRAMES_DIR)

    FRAMES_DIR.mkdir(parents=True, exist_ok=True)

    cam = cv2.VideoCapture(video_path)

    total_frames = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))

    currentframe = 0

    while True:
        ret, frame = cam.read()
        if ret:
            img_path = FRAMES_DIR / f"frame_{currentframe}.jpg"
            if currentframe % (total_frames // n_frames) == 0:
                cv2.imwrite(str(img_path), frame)
            currentframe += 1
        else:
            break

    cam.release()
    cv2.destroyAllWindows()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

logger.info("\n##### Starting step 3 frame sampling #####\n")

create_screeshots(configs["video_path"], configs["frame_sampling"]["n_frames"])
