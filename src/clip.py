import logging
import math
from glob import glob
from pathlib import Path

import librosa
from moviepy.editor import VideoFileClip

from common import configs, scenes_dir


def get_clip(movie: VideoFileClip, scenes_dir: list[str], min_clip_len: int) -> None:
    """Create video clips based on individual frames

    Args:
        movie (VideoFileClip): Movie file source for the clips
        scenes_dir (list[str]): Directories for each scence
        min_clip_len (int): Minimum clip length
    """
    fps = movie.fps

    for idx, scene_dir in enumerate(scenes_dir):
        logger.info(f"Generating clips for scene {idx+1}")
        clip_dir = Path(f"{scene_dir}/clips")
        audio_filepaths = glob(f"{scene_dir}/audios/*.wav")
        frame_paths = glob(f"{scene_dir}/frames/*.jpg")

        if not clip_dir.exists():
            clip_dir.mkdir(parents=True, exist_ok=True)

        for audio_filepath in audio_filepaths:
            audio_filename = audio_filepath.split("/")[-1].split(".")[0]
            audio_duration = math.ceil(librosa.get_duration(path=audio_filepath))
            audio_duration = max(min_clip_len, audio_duration)

            for frame_path in frame_paths:
                frame = int(frame_path.split("/")[-1].split(".")[0].split("_")[-1])

                clip_start = frame // fps
                clip_end = clip_start + audio_duration

                clip = movie.subclip(clip_start, clip_end)
                clip.write_videofile(
                    f"{clip_dir}/clip_{frame}_{audio_filename}.mp4",
                    verbose=False,
                    logger=None,
                )
                clip.close()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

logger.info("##### Starting step 5 clip creation #####")

movie = VideoFileClip(configs["movie_path"], audio=True)

get_clip(movie, scenes_dir, configs["min_clip_len"])
