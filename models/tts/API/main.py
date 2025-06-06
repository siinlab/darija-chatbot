import os  # noqa: D100

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .predict import Speaker, generate_wav

router = APIRouter()


class GenerateRequest(BaseModel):  # noqa: D101
	text: str
	speaker: Speaker


@router.post("/generate")
def generate_speech(request: GenerateRequest):  # noqa: ANN201, D103
	try:
		wav_path = generate_wav(request.text, request.speaker)
		return FileResponse(
			wav_path,
			media_type="audio/wav",
			filename=os.path.basename(wav_path),  # noqa: PTH119
		)
	except Exception as e:  # noqa: BLE001
		raise HTTPException(status_code=500, detail=str(e))  # noqa: B904
