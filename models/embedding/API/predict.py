"""Evaluate the Whisper model on few Arabic audios."""

import numpy as np
from lgg import logger
from sentence_transformers import SentenceTransformer

# Load the model
_model = SentenceTransformer(
	"Omartificial-Intelligence-Space/Arabic-Triplet-Matryoshka-V2",
)


def predict(texts: list[str]) -> np.ndarray:
	"""Compute the embeddings of the input texts.

	Args:
		texts (list[str]): A list of texts.

	Returns:
		np.ndarray: The embeddings of the input texts.
	"""
	logger.debug(f"Computing the embeddings of {len(texts)} input texts.")
	return _model.encode(texts)
