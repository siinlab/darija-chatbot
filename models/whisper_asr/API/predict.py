"""Evaluate the Whisper model on few Arabic audios."""

from pathlib import Path

from lgg import logger
from transformers import pipeline

logger.setLevel("INFO")

model = Path(__file__).parent.parent / "checkpoints"

# Load the model
logger.info(f"Loading model from {model}")
model = pipeline(model=model, task="automatic-speech-recognition", device=0)


def predict(audio_paths: list[str]) -> list[str]:
	"""Predict the transcription of given audio files.

	Args:
		audio_paths (list[str]): A list of file paths to the audio files
		to be transcribed.

	Returns:
		list[str]: A list of transcriptions corresponding to the input audio files.
	"""
	logger.debug(f"Received {len(audio_paths)} audio files.")
	result = model(audio_paths)
	return [res["text"] for res in result]


def generate_random_path() -> str:
	"""Generate a random path for the audio file.

	Returns:
		str: The path to the generated audio file.
	"""
	import tempfile
	import uuid

	name = f"test-{uuid.uuid4()!s}.wav"
	out_dir = tempfile.gettempdir()
	return (Path(out_dir) / name).as_posix()
