import logging
import shutil
from glob import glob
from pathlib import Path

import numpy as np
from PIL import Image
from sentence_transformers import SentenceTransformer, util

from common import FRAME_DIR, configs, scenes_dir


def get_image_embeddings(
    model: SentenceTransformer, img_filepaths: list[str], batch_size: int
) -> np.ndarray:
    """Create embeddings from a set of images.

    Args:
        model (SentenceTransformer): Model used to embed the images
        img_filepaths (list[str]): File paths for all images
        batch_size (int): Batch size of images to embed at the same time

    Returns:
        np.ndarray: Image embeddings
    """
    img_emb = model.encode(
        [Image.open(img_filepath) for img_filepath in img_filepaths],
        batch_size=batch_size,
        convert_to_tensor=True,
        show_progress_bar=True,
    )
    return img_emb


def retrieve_frames(
    scenes_dir: list[str],
    img_filepaths: list[str],
    model: SentenceTransformer,
    img_emb: np.ndarray,
    top_k: int,
) -> None:
    """Retrieve the `top_k` most similar frame images to a subplot text.

    Args:
        scenes_dir (list[str]): Directories for each scence
        img_filepaths (list[str]): File paths for all images
        model (SentenceTransformer): Similarity model used to measure similarity
        img_emb (np.ndarray): Image embeddings used as the retrieval source
        top_k (int): Number of images to be retrieved
    """
    for idx, scene_dir in enumerate(scenes_dir):
        logger.info(f"Retrieving images for scene {idx+1}")
        plot_path = Path(f"{scene_dir}/plot.txt")
        frames_dir = Path(f"{scene_dir}/frames")

        if not frames_dir.exists():
            frames_dir.mkdir(parents=True, exist_ok=True)

        plot = plot_path.read_text()
        hits = search(plot, model, img_emb, top_k=top_k)

        for hit in hits:
            img_filepath = img_filepaths[hit["corpus_id"]]
            img_name = img_filepath.split("/")[-1]

            shutil.copyfile(img_filepath, f"{frames_dir}/{img_name}")


def search(
    query: str, model: SentenceTransformer, img_emb: np.ndarray, top_k: int
) -> dict:
    """Search the `top_k` most similar embeddings to a text.

    Args:
        query (str): Subplot text used as a similarity reference
        model (SentenceTransformer): Similarity model used to measure similarity
        img_emb (np.ndarray): Image embeddings used as the retrieval source
        top_k (int): Number of images to be retrieved

    Returns:
        dict: Retrieved images with some metadata
    """
    query_emb = model.encode(
        [query],
        convert_to_tensor=True,
        show_progress_bar=False,
    )
    hits = util.semantic_search(query_emb, img_emb, top_k=top_k)[0]
    return hits


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

logger.info("##### Starting step 4 frame retrieval #####")

logger.info(f"Loading {configs['similarity_model_id']} as the similarity model")
model = SentenceTransformer(configs["similarity_model_id"])

img_filepaths = glob(f"{FRAME_DIR}/*.jpg")
logger.info(f"Retrieving from {len(img_filepaths)} images")
img_emb = get_image_embeddings(model, img_filepaths, configs["similarity_batch_size"])

retrieve_frames(
    scenes_dir, img_filepaths, model, img_emb, configs["n_retrieved_images"]
)
