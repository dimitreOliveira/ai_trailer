import logging
from glob import glob
from pathlib import Path

from moviepy.editor import AudioFileClip, CompositeAudioClip, VideoFileClip

from common import configs, scenes_dir


def get_audio_clips(
    scenes_dir: list[str], clip_volume: float, voice_volume: float
) -> None:
    """Add generated voice to each clip.

    Args:
        scenes_dir (list[str]): Directories for each scence
        clip_volume (float): Volume of the original clip used for the audio clip
        voice_volume (float): Volume of the generated voice used for the audio clip
    """
    for idx, scene in enumerate(scenes_dir):
        logger.info(f'Generating audio clips for scene "{idx+1}"')
        clips_dir = Path(f"{scene}/clips")
        audios_dir = Path(f"{scene}/audios")
        audio_clips_dir = Path(f"{scene}/audio_clips")

        if not audio_clips_dir.exists():
            audio_clips_dir.mkdir(parents=True, exist_ok=True)

        for audio_path in glob(f"{audios_dir}/*.wav"):
            audio_name = Path(audio_path).stem
            audio = AudioFileClip(audio_path)

            for clip_path in glob(f"{clips_dir}/*{audio_name}.mp4"):
                clip_name = Path(clip_path).stem
                clip = VideoFileClip(clip_path)

                mixed_audio = CompositeAudioClip(
                    [
                        clip.audio.volumex(clip_volume),
                        audio.volumex(voice_volume),
                    ]
                )
                clip.set_audio(mixed_audio).write_videofile(
                    f"{audio_clips_dir}/audio_clip_{clip_name}.mp4",
                    verbose=False,
                    logger=None,
                )


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

logger.info("##### Starting step 6 audio clip creation #####")

get_audio_clips(scenes_dir, configs["clip_volume"], configs["voice_volume"])
