import os  # noqa: D100
import traceback as tb

from fastapi import FastAPI, HTTPException, UploadFile  # import UploadFile
from fastapi.responses import FileResponse  # import FileResponse
from model_api import Voice, generate_wav, respond, transcribe
from pydantic import BaseModel

app = FastAPI()


class GenerateRequest(BaseModel):  # noqa: D101
	text: str
	voice: Voice
	checkpoint: str = "states_6000"


class Message(BaseModel):  # noqa: D101
	role: str
	content: str


class Dialog(BaseModel):  # noqa: D101
	messages: list[Message]


@app.post("/generate")
def generate_speech(request: GenerateRequest):  # noqa: ANN201, D103
	try:
		wav_path = generate_wav(request.text, request.voice, request.checkpoint)
		return FileResponse(
			wav_path,
			media_type="audio/wav",
			filename=os.path.basename(wav_path),  # noqa: PTH119
		)
	except Exception as e:  # noqa: BLE001
		raise HTTPException(status_code=500, detail=str(e))  # noqa: B904


@app.post("/transcribe")
def transcribe_audio(file: UploadFile):  # noqa: ANN201, D103
	try:
		# save file to disk
		file_path = f"/tmp/{file.filename}"  # noqa: S108
		with open(file_path, "wb") as f:  # noqa: PTH123
			f.write(file.file.read())
		transcription = transcribe(file_path)
		return {"transcription": transcription}  # noqa: TRY300
	except Exception as e:  # noqa: BLE001
		raise HTTPException(status_code=500, detail=str(e))  # noqa: B904


@app.post("/chat")
def respond_to_dialog(dialog: Dialog):  # noqa: ANN201, D103
	try:
		# convert dialog to python dict
		messages = dialog.model_dump()["messages"]
		response = respond(messages)
		return {"response": response}  # noqa: TRY300
	except Exception as e:  # noqa: BLE001
		tb.print_exc()
		raise HTTPException(status_code=500, detail=str(e))  # noqa: B904
