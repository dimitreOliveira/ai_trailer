import itertools
import logging
from glob import glob
from pathlib import Path

from moviepy.editor import VideoFileClip, concatenate_videoclips

from common import TRAILER_DIR, scenes_dir


def join_clips(clip_combinations: list[tuple[str]], trailer_dir: Path) -> None:
    """Join audio clips to create a trailer.

    Args:
        clip_combinations (list[list[str]]): List of audio clips to be combined
        trailer_dir (Path): Directory save the trailers
    """
    for idx, clip_combination in enumerate(clip_combinations):
        logger.info(f"Generating trailer {idx+1}")
        trailer_path = Path(f"{trailer_dir}/trailer_{idx+1}.mp4")
        clips = [VideoFileClip(clip_path) for clip_path in clip_combination]
        trailer = concatenate_videoclips(clips)
        trailer.write_videofile(str(trailer_path))


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

logger.info("##### Starting step 7 trailer creation #####")

if not TRAILER_DIR.exists():
    TRAILER_DIR.mkdir(parents=True, exist_ok=True)

audio_clips = [glob(f"{scene}/audio_clips/*.mp4") for scene in scenes_dir]
audio_clip_combinations = list(itertools.product(*audio_clips))

join_clips(audio_clip_combinations, TRAILER_DIR)
