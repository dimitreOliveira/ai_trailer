import logging
import shutil
from pathlib import Path

import numpy as np
from PIL import Image
from sentence_transformers import SentenceTransformer, util

from common import FRAMES_DIR, SCENES_DIR, configs


def get_image_embeddings(
    model: SentenceTransformer, img_filepaths: list[Path], batch_size: int
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
    img_filepaths: list[Path],
    model: SentenceTransformer,
    img_emb: np.ndarray,
    top_k: int,
) -> None:
    """Retrieve the `top_k` most similar frame images to a subplot text.

    Args:
        img_filepaths (list[str]): File paths for all images
        model (SentenceTransformer): Similarity model used to measure similarity
        img_emb (np.ndarray): Image embeddings used as the retrieval source
        top_k (int): Number of images to be retrieved
    """
    for idx, scene_dir in enumerate(SCENES_DIR):
        logger.info(f"Retrieving images for scene {idx+1}")
        plot_path = scene_dir / "subplot.txt"
        scene_frames_dir = scene_dir / "frames"

        if scene_frames_dir.exists():
            shutil.rmtree(scene_frames_dir)

        scene_frames_dir.mkdir(parents=True, exist_ok=True)

        plot = plot_path.read_text()
        hits = search(plot, model, img_emb, top_k=top_k)

        for hit in hits:
            img_filepath = img_filepaths[hit["corpus_id"]]
            img_name = img_filepath.name

            shutil.copyfile(img_filepath, f"{scene_frames_dir}/{img_name}")


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

logger.info("\n##### Starting step 4 frame retrieval #####\n")

logger.info(f"Loading {configs['frame_ranking']['model_id']} as the similarity model")
model = SentenceTransformer(
    configs["frame_ranking"]["model_id"], device=configs["frame_ranking"]["device"]
)

img_filepaths = list(FRAMES_DIR.glob("*.jpg"))
logger.info(f"Retrieving from {len(img_filepaths)} images")
img_emb = get_image_embeddings(
    model, img_filepaths, configs["frame_ranking"]["similarity_batch_size"]
)

retrieve_frames(
    img_filepaths, model, img_emb, configs["frame_ranking"]["n_retrieved_images"]
)
