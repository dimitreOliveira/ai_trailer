import logging
import shutil

from moviepy.editor import AudioFileClip, CompositeAudioClip, VideoFileClip

from common import SCENES_DIR, configs


def get_audio_clips(clip_volume: float, voice_volume: float) -> None:
    """Add generated voice to each clip.

    Args:
        clip_volume (float): Volume of the original clip used for the audio clip
        voice_volume (float): Volume of the generated voice used for the audio clip
    """
    for idx, scene_dir in enumerate(SCENES_DIR):
        logger.info(f'Generating audio clips for scene "{idx+1}"')
        clips_dir = scene_dir / "clips"
        audios_dir = scene_dir / "audios"
        audio_clips_dir = scene_dir / "audio_clips"

        if audio_clips_dir.exists():
            shutil.rmtree(audio_clips_dir)

        audio_clips_dir.mkdir(parents=True, exist_ok=True)

        for audio_path in audios_dir.glob("*.wav"):
            audio_name = audio_path.stem
            audio = AudioFileClip(str(audio_path))

            for clip_path in clips_dir.glob(f"*{audio_name}.mp4"):
                clip_name = clip_path.stem
                clip = VideoFileClip(str(clip_path))

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

logger.info("\n##### Starting step 6 audio clip creation #####\n")

get_audio_clips(
    configs["audio_clip"]["clip_volume"],
    configs["audio_clip"]["voice_volume"],
)
