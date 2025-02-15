"""Main API module for the Whisper ASR."""

from io import BytesIO

import numpy as np
from fastapi import APIRouter, HTTPException, Response

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
		# Preserve the array shape by saving the array with np.save
		buf = BytesIO()
		np.save(buf, embeddings)
		buf.seek(0)
		return Response(content=buf.getvalue(), media_type="application/octet-stream")
	except Exception as e:  # noqa: BLE001
		raise HTTPException(status_code=500, detail=str(e))  # noqa: B904
