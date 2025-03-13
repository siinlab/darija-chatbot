"""Evaluate the Whisper model on few Arabic audios."""

import argparse
import random
from pathlib import Path
from shutil import copyfile

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
	"--output-dir",
	type=str,
	default=".",
	help="path to the output directory where the results will be saved",
)
parser.add_argument(
	"--num-samples",
	type=int,
	default=10,
	help="Number of audios to use for prediction."
	"The audios are randomly sampled from the dataset.",
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
		audio_paths.extend(audio_path.rglob("**/*.mp3"))
		audio_paths.extend(audio_path.rglob("**/*.wav"))
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

# Randomly sample num_samples audios
if len(audio_paths) > args.num_samples:
	audio_paths = random.sample(audio_paths, args.num_samples)

logger.info(f"Using {len(audio_paths)} audio files for prediction")

# sort the audio paths for reproducibility
audio_paths = sorted(audio_paths)

# Evaluate the model on the audio files
result = model([audio_path.as_posix() for audio_path in audio_paths])

# pretty print the results
for i, res in enumerate(result):
	logger.info(f"Audio {audio_paths[i]}")
	logger.info(f"Transcription: {res['text']}")

# save results to a csv file: audio,caption
output_dir = Path(args.output_dir).resolve()
audios_dir = output_dir / "audios"
# create the output directory if it doesn't exist
if not audios_dir.exists():
	logger.debug(f"Output directory {audios_dir} doesn't exist. Creating it.")
	audios_dir.mkdir(parents=True, exist_ok=False)
new_audio_filenames = [
	f"{audio_path.parent.name}-{audio_path.name}" for audio_path in audio_paths
]
dataframe = pd.DataFrame(
	{
		"audio": new_audio_filenames,
		"caption": [res["text"] for res in result],
	},
)
output_file = output_dir / "data.csv"
dataframe.to_csv(output_file, index=False)

# copy the audio files to the output directory
for audio_path, audio_filename in zip(audio_paths, new_audio_filenames, strict=False):
	copyfile(audio_path, audios_dir / audio_filename)

logger.info(f"Results saved to {output_dir}")
