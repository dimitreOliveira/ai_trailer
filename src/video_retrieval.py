import logging
from pathlib import Path

from pytube import YouTube

from common import PROJECT_DIR, configs


def get_video(video_url: str, video_path: Path) -> None:
    logger.info(f'Downloading video from URL: "{video_url}"')

    youtubeObject = YouTube(video_url)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    youtubeObject.download(
        output_path=video_path.parents[0],
        filename=video_path.name,
    )

    logger.info(f'Video saved to: "{video_path}"')


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

logger.info("\n##### Starting optional step video retrieval #####\n")

video_path = Path(configs["video_path"])

if not video_path.exists():
    video_path.parent.mkdir(parents=True, exist_ok=True)

if not PROJECT_DIR.exists():
    PROJECT_DIR.mkdir(parents=True, exist_ok=True)

get_video(configs["video_retrieval"]["video_url"], video_path)
