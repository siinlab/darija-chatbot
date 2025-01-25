"""Evaluate the Whisper model on few Arabic audios."""

import argparse
from pathlib import Path

from lgg import logger
from transformers import pipeline

logger.setLevel("INFO")

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
model = pipeline(model=model, task="automatic-speech-recognition", device=0)

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
result = model([audio_path.as_posix() for audio_path in audio_paths])

# pretty print the results
for i, res in enumerate(result):
	logger.info(f"Audio {audio_paths[i]}")
	logger.info(f"Transcription: {res['text']}")
