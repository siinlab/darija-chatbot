"""Evaluate the Whisper model on few Arabic audios."""

import argparse
from pathlib import Path

from lgg import logger
from transformers import pipeline

parser = argparse.ArgumentParser(
	description="Evaluate the Whisper model on few Arabic audios.",
)
parser.add_argument(
	"--audios",
	type=str,
	nargs="+",
	required=True,
	help="path to the audio files",
)
parser.add_argument(
	"--model",
	type=str,
	required=True,
	help="path to the model checkpoint",
)

args = parser.parse_args()

audios = args.audios
model = args.model

# Load the model
logger.info(f"Loading model from {model}")
model = loaded_pipeline = pipeline(model=model)

# Load the audio files
audio_paths = []
for audio in audios:
	audio_path = Path(audio)
	# if audio_path is a directory, then get all mp3 and wav files
	if audio_path.is_dir():
		audio_paths.extend(audio_path.glob("*.mp3"))
		audio_paths.extend(audio_path.glob("*.wav"))
	else:
		audio_paths.append(audio_path)

logger.info(f"Found {len(audio_paths)} audio files")


# Evaluate the model on the audio files
for audio_path in audio_paths:
	logger.info(f"Evaluating {audio_path}")
	result = model(audio_path.as_posix())
	logger.info(result)
