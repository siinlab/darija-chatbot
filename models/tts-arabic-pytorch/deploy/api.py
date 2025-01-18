from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse  # import FileResponse
from pydantic import BaseModel
from model_api import generate_wav
import os

app = FastAPI()

class GenerateRequest(BaseModel):
    text: str
    model_name: str

@app.post("/generate")
def generate_speech(request: GenerateRequest):
    try:
        wav_path = generate_wav(request.text, request.model_name)
        return FileResponse(wav_path, media_type="audio/wav", filename=os.path.basename(wav_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
