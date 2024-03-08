import logging
import shutil

from common import PLOT_PATH, PROJECT_DIR, configs


def get_sub_plots(plot: str, split_char: str) -> None:
    """Split the plot into subplots (scenes).

    Args:
        plot (str): Plot text
        split_char (str): Character used to split the main plot
    """
    logger.info("Generating subplots")
    subplots = plot.splitlines()
    subplots_: list[str] = []
    if split_char:
        for x in subplots:
            subplots_.extend(
                [x.strip() + str(split_char) for x in x.split(split_char) if x != ""]
            )
        subplots = subplots_

    for idx, subplot in enumerate(subplots):
        scene_dir = PROJECT_DIR / f"scene_{idx+1}"
        scene_plot_path = scene_dir / "subplot.txt"

        if scene_dir.exists():
            shutil.rmtree(scene_dir)

        scene_dir.mkdir(parents=True, exist_ok=True)

        scene_plot_path.write_text(subplot)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

logger.info("\n##### Starting step 1 subplot generation #####\n")

plot = PLOT_PATH.read_text()

get_sub_plots(plot, configs["subplot"]["split_char"])
