"""Evaluate the Whisper model on few Arabic audios."""

import argparse
from pathlib import Path

import librosa
import pandas as pd
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
parser.add_argument(
	"--output-file",
	type=str,
	default="./results.csv",
	help="path to the output file",
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

# drop audios with durtion > 30 seconds
audio_paths = [
	audio_path
	for audio_path in audio_paths
	if librosa.load(audio_path, sr=16000)[0].shape[0] < 30 * 16000
]

logger.info(f"Found {len(audio_paths)} audio files with duration < 30 seconds")

# Evaluate the model on the audio files
result = model([audio_path.as_posix() for audio_path in audio_paths])

# pretty print the results
for i, res in enumerate(result):
	logger.info(f"Audio {audio_paths[i]}")
	logger.info(f"Transcription: {res['text']}")

# save results to a csv file: audio,caption
output_file = Path(args.output_file).resolve()
# create the output directory if it doesn't exist
if not output_file.parent.exists():
	logger.debug(f"Output directory {output_file.parent} doesn't exist. Creating it.")
	output_file.parent.mkdir(parents=True, exist_ok=False)
dataframe = pd.DataFrame(
	{
		"audio": [audio_path.as_posix() for audio_path in audio_paths],
		"caption": [res["text"] for res in result],
	},
)

dataframe.to_csv(output_file, index=False)
