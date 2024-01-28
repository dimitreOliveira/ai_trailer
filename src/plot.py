import logging
from pathlib import Path

from imdb import Cinemagoer

from common import PLOT_PATH, PROJECT_DIR, configs


def get_movie_plot(movie_id: str, plot_path: Path) -> str:
    """Retrieve the movie plot from IMDB.

    Args:
        movie_id (str): Movie ID from IMDB (integer part of the URL)
        plot_path (Path): Path to sabe the plot text

    Returns:
        str: Plot text
    """
    logger.info(f'Fetching plot for movie ID: "{movie_id}"')

    ia = Cinemagoer()
    movie = ia.get_movie(movie_id)
    plot = movie["plot outline"]
    plot_path.write_text(plot)

    return plot


def get_sub_plots(plot: str, project_dir: Path) -> None:
    """Split the plot into subplots (scenes).

    Args:
        plot (str): Plot text
        project_dir (Path): Main project directory
    """
    logger.info("Generating subplots")
    for idx, scene_plot in enumerate([x for x in plot.split(".") if x != ""]):
        scene_plot_path = Path(f"{project_dir}/scene_{idx+1}/plot.txt")
        scene_plot = (
            scene_plot.strip() + "."
        )  # Adding back the final point improves voice generation

        if not scene_plot_path.exists():
            scene_plot_path.parent.mkdir(parents=True, exist_ok=True)
        scene_plot_path.write_text(scene_plot)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

logger.info("##### Starting step 1 plot retrieval #####")

if not PLOT_PATH.exists():
    PLOT_PATH.parent.mkdir(parents=True, exist_ok=True)

plot = get_movie_plot(configs["movie_id"], PLOT_PATH)

get_sub_plots(plot, PROJECT_DIR)
