from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse  # import FileResponse
from pydantic import BaseModel
from model_api import generate_wav, Voice
import os

app = FastAPI()


class GenerateRequest(BaseModel):
	text: str
	voice: Voice
	checkpoint: str = "states_6000"


@app.post("/generate")
def generate_speech(request: GenerateRequest):
	try:
		wav_path = generate_wav(request.text, request.voice, request.checkpoint)
		return FileResponse(
			wav_path, media_type="audio/wav", filename=os.path.basename(wav_path),
		)
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
