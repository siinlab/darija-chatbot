from fastapi import FastAPI, HTTPException, UploadFile  # import UploadFile
from fastapi.responses import FileResponse  # import FileResponse
from pydantic import BaseModel
from model_api import generate_wav, Voice, transcribe, respond
import os
import traceback as tb

app = FastAPI()


class GenerateRequest(BaseModel):
	text: str
	voice: Voice
	checkpoint: str = "states_6000"


class Message(BaseModel):
	role: str
	content: str


class Dialog(BaseModel):
	messages: list[Message]


@app.post("/generate")
def generate_speech(request: GenerateRequest):
	try:
		wav_path = generate_wav(request.text, request.voice, request.checkpoint)
		return FileResponse(
			wav_path,
			media_type="audio/wav",
			filename=os.path.basename(wav_path),
		)
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@app.post("/transcribe")
def transcribe_audio(file: UploadFile):
	# make sure the file is a wav file
	# if file.content_type != "audio/wav":
	# 	raise HTTPException(status_code=400, detail=f"Only wav files are supported. Got: {file.content_type}")
	try:
		# save file to disk
		file_path = f"/tmp/{file.filename}"
		with open(file_path, "wb") as f:
			f.write(file.file.read())
		transcription = transcribe(file_path)
		return {"transcription": transcription}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat")
def respond_to_dialog(dialog: Dialog):
	try:
		# convert dialog to python dict
		messages = dialog.model_dump()["messages"]
		response = respond(messages)
		return {"response": response}
	except Exception as e:
		tb.print_exc()
		raise HTTPException(status_code=500, detail=str(e))
