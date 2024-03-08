import logging
import shutil

from TTS.api import TTS

from common import SCENES_DIR, configs


def generate_voice(
    model: TTS, text: str, audio_path: str, reference_voice_path: str, language: str
) -> None:
    """_summary_

    Args:
        model (TTS): TTS model used to generate the audios
        text (str): Text that will be voiced
        audio_path (str): Output path to save the generated audio
        reference_voice_path (str): Reference audio file used for voice cloning
        language (str): Language used for the TTS model
    """
    model.tts_to_file(
        text,
        speaker_wav=reference_voice_path,
        language=language,
        file_path=audio_path,
    )


def generate_voices(
    model: TTS, n_audios: int, reference_voice_path: str, language: str
) -> None:
    """Generate voice for each subplot.

    Args:
        model (TTS): TTS model used to generate the audios
        n_audios (int): Number of audio samples created for each text
        reference_voice_path (str): Reference audio file used for voice cloning
        language (str): Language used for the TTS model
    """
    for idx, scene_dir in enumerate(SCENES_DIR):
        scene_plot = (scene_dir / "subplot.txt").read_text()
        audio_dir = scene_dir / "audios"
        logger.info(f'Generating audio for scene {idx+1} with plot "{scene_plot}"')

        if audio_dir.exists():
            shutil.rmtree(audio_dir)

        audio_dir.mkdir(parents=True, exist_ok=True)

        for idx in range(n_audios):
            logger.info(f"Generating audio {idx+1}")
            voice_path = audio_dir / f"audio_{idx+1}.wav"
            generate_voice(
                model, scene_plot, str(voice_path), reference_voice_path, language
            )


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

logger.info("\n##### Starting step 2 voice generation #####\n")

tts = TTS(model_name=configs["voice"]["model_id"]).to(configs["voice"]["device"])

generate_voices(
    tts,
    configs["voice"]["n_audios"],
    configs["voice"]["reference_voice_path"],
    configs["voice"]["tts_language"],
)
