"""Main API module for the Whisper ASR."""

from fastapi import APIRouter, HTTPException, UploadFile
from predict import generate_random_path, predict

router = APIRouter("Darija Speech To Text API")


@router.post("/transcribe")
def transcribe_audio(file: UploadFile):  # noqa: ANN201, D103
	try:
		# save file to disk
		file_path = generate_random_path()
		with open(file_path, "wb") as f:  # noqa: PTH123
			f.write(file.file.read())
		transcription = predict([file_path])
		return {"transcription": transcription}  # noqa: TRY300
	except Exception as e:  # noqa: BLE001
		raise HTTPException(status_code=500, detail=str(e))  # noqa: B904
