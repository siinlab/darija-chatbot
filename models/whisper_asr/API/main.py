"""Main API module for the Whisper ASR."""

from fastapi import APIRouter, HTTPException, UploadFile

from .predict import generate_random_path, predict

router = APIRouter()


@router.post("/transcribe")
def transcribe_audio(files: list[UploadFile]) -> list[str]:
	"""Transcribes the given audio file(s) using a pre-trained model.

	Args:
		files (list[UploadFile]): A list of audio files to be transcribed.

	Returns:
		list: A list containing the transcription of the audio file(s).

	Raises:
		HTTPException: If an error occurs during the transcription process,
		an HTTPException is raised with a status code of 500 and the error details.
	"""
	try:
		# save file to disk
		audio_paths = []
		for file in files:
			file_path = generate_random_path()
			with open(file_path, "wb") as f:  # noqa: PTH123
				f.write(file.file.read())
			audio_paths.append(file_path)
		return predict(audio_paths)
	except Exception as e:  # noqa: BLE001
		raise HTTPException(status_code=500, detail=str(e))  # noqa: B904
