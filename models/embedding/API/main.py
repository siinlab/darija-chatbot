"""Main API module for the Whisper ASR."""

from fastapi import APIRouter, HTTPException

from .predict import predict
from .utils import EmbeddingRequest

router = APIRouter(prefix="/embedding")


@router.post("/")
def compute_embedding(texts_list: EmbeddingRequest) -> bytes:
	"""Transcribes the given audio file(s) using a pre-trained model.

	Args:
		texts_list (EmbeddingRequest): A list of texts.

	Returns:
		bytes: The embeddings of the input texts.
	"""
	try:
		texts = texts_list.texts
		embeddings = predict(texts)
		return embeddings.tobytes()
	except Exception as e:  # noqa: BLE001
		raise HTTPException(status_code=500, detail=str(e))  # noqa: B904
