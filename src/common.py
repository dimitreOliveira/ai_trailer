import logging
import re
from pathlib import Path

import yaml


def parse_configs(configs_path: str) -> dict:
    """Parse configs from the YAML file.

    Args:
        configs_path (str): Path to the YAML file

    Returns:
        dict: Parsed configs
    """
    configs = yaml.safe_load(open(configs_path, "r"))
    logger.info(f"Configs: {configs}")
    return configs


CONFIGS_PATH = "configs.yaml"


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

configs = parse_configs(CONFIGS_PATH)

PROJECT_DIR = Path(f"{configs['project_dir']}/{configs['project_name']}")
PLOT_PATH = PROJECT_DIR / configs["plot_filename"]
FRAMES_DIR = PROJECT_DIR / "frames"
TRAILER_DIR = PROJECT_DIR / "trailers"

SCENES_DIR = list(PROJECT_DIR.glob("scene_*"))
SCENES_DIR = sorted(
    SCENES_DIR, key=lambda s: int(re.search(r"\d+", str(s)).group())
)  # Natural sort
