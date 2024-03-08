import logging

from imdb import Cinemagoer

from common import PLOT_PATH, configs


def get_video_plot(video_id: str) -> str:
    """Retrieve the video plot from IMDB.

    Args:
        video_id (str): Video ID from IMDB (integer part of the URL)

    Returns:
        str: Plot text
    """
    logger.info(f'Fetching plot for video ID: "{video_id}"')

    ia = Cinemagoer()
    video = ia.get_movie(video_id)
    plot = video["plot outline"]
    PLOT_PATH.write_text(plot)

    return plot


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

logger.info("\n##### Starting optional step plot retrieval #####\n")

if not PLOT_PATH.exists():
    PLOT_PATH.parent.mkdir(parents=True, exist_ok=True)

plot = get_video_plot(configs["plot_retrieval"]["video_id"])
