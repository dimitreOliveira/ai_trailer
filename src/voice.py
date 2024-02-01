import logging
from pathlib import Path

from TTS.api import TTS

from common import configs, scenes_dir


def generate_voices(scenes_dir: list[str]) -> None:
    """Generate voice for each subplot.

    Args:
        scenes_dir (list[str]): Directories for each scence
    """
    for idx, scenes in enumerate(scenes_dir):
        scene_plot = Path(f"{scenes}/plot.txt").read_text()
        audio_dir = Path(f"{scenes}/audios")
        logger.info(f'Generating audio for scene {idx+1} with plot "{scene_plot}"')

        if not audio_dir.exists():
            audio_dir.mkdir(parents=True, exist_ok=True)

        for idx in range(configs["n_audios"]):
            logger.info(f"Generating audio {idx+1}")
            tts.tts_to_file(
                scene_plot,
                speaker_wav=configs["reference_voice_path"],
                language=configs["tts_language"],
                file_path=f"{audio_dir}/audio_{idx+1}.wav",
            )


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

logger.info("##### Starting step 2 voice generation #####")
logger.info(configs["tts_model_id"])

tts = TTS(model_name=configs["tts_model_id"]).to(configs["device"])
generate_voices(scenes_dir)
