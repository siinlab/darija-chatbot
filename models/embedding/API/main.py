"""Main API module for the Whisper ASR."""

from fastapi import APIRouter, HTTPException

from .predict import predict  # noqa: F401
from .utils import EmbeddingRequest

router = APIRouter(prefix="/embedding")


@router.post("/")
def compute_embedding(texts: EmbeddingRequest) -> bytes:  # noqa: ARG001
	"""Transcribes the given audio file(s) using a pre-trained model.

	Args:
		texts (EmbeddingRequest): A list of texts.

	"""
	try:
		pass
	except Exception as e:  # noqa: BLE001
		raise HTTPException(status_code=500, detail=str(e))  # noqa: B904
