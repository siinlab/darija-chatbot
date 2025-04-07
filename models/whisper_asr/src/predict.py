"""Evaluate the Whisper model on few Arabic audios."""

import argparse
import random
import shutil
import warnings
from pathlib import Path
from shutil import copyfile

import joblib
import librosa
import pandas as pd
import psutil
from lgg import logger
from tqdm import tqdm
from transformers import pipeline

# suppress FutureWarning
warnings.simplefilter("ignore", category=FutureWarning)
logger.setLevel("INFO")

# Get the number of physical CPU cores
num_cores = psutil.cpu_count(logical=False) - 4


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
parser.add_argument(
	"--batch-size",
	type=int,
	default=32,
	help="Batch size for prediction.",
)
parser.add_argument(
	"--fresh-start",
	action="store_true",
	help="If True, then start the prediction from scratch, ie. don't use the existing results.",  # noqa: E501
)

args = parser.parse_args()

audios = args.audios
model = args.model
batch_size = args.batch_size
fresh_start = args.fresh_start

output_dir = Path(args.output_dir).resolve()
audios_dir = output_dir / "audios"
csv_file = output_dir / "data.csv"

if fresh_start:
	logger.info(f"Removing the existing output directory {output_dir}")
	shutil.rmtree(output_dir, ignore_errors=True)
else:
	logger.info(
		f"Using the existing output directory {output_dir} "
		"including the audios and data.csv",
	)
# create the output directory if it doesn't exist
if not audios_dir.exists():
	fresh_start = True  # if the directory doesn't exist, then start over
	logger.debug(f"Output directory {audios_dir} doesn't exist. Creating it.")
	audios_dir.mkdir(parents=True, exist_ok=False)

# Load the model
logger.info(f"Loading model from {model}")
model = pipeline(
	model=model,
	task="automatic-speech-recognition",
	device=0,
	torch_dtype="float16",
)

# Load the audio files
audio_paths = []
if fresh_start:
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
	def filter_audio(audio_path):  # noqa: ANN001, ANN201, D103
		try:
			return (
				audio_path
				if librosa.load(audio_path, sr=16000)[0].shape[0] < 30 * 16000
				else None
			)
		except Exception as e:  # noqa: BLE001
			logger.warning(f"Error processing {audio_path}: {e}")
			return None

	audio_paths = joblib.Parallel(n_jobs=-1)(
		joblib.delayed(filter_audio)(audio_path) for audio_path in audio_paths
	)
	audio_paths = [audio_path for audio_path in audio_paths if audio_path]

	logger.info(f"Found {len(audio_paths)} audio files with duration < 30 seconds")

	# Randomly sample num_samples audios
	if args.num_samples > 0 and len(audio_paths) > args.num_samples:
		audio_paths = random.sample(audio_paths, args.num_samples)
else:
	# load audio_paths from the audios_dir
	audio_paths = list(audios_dir.rglob("*"))

logger.info(f"Using {len(audio_paths)} audio files for prediction")

# sort the audio paths for reproducibility
audio_paths = sorted(audio_paths)

# Evaluate the model on the audio files
result = []
for i in tqdm(range(0, len(audio_paths), batch_size)):
	try:
		batch_audio_paths = audio_paths[i : i + batch_size]
		batch_result = model(
			[audio_path.as_posix() for audio_path in batch_audio_paths],
			batch_size=len(batch_audio_paths),
			num_workers=num_cores,
		)
		result.extend(batch_result)
	except Exception as e:  # noqa: BLE001, PERF203
		result.extend([{"text": ""} for _ in batch_audio_paths])
		logger.warning(f"Error occurred while processing {batch_audio_paths}: {e}")

# pretty print the results
for i, res in enumerate(result):
	logger.info(f"Audio {audio_paths[i]}")
	logger.info(f"Transcription: {res['text']}")

# save results to a csv file: audio,caption
new_audio_filenames = [
	f"{audio_path.parent.name}-{audio_path.name}" for audio_path in audio_paths
]
if fresh_start:
	logger.info("Creating a new dataframe with columns 'audio' and 'caption-1'")
	dataframe = pd.DataFrame(
		{
			"audio": new_audio_filenames,
			"caption-1": [res["text"] for res in result],
		},
	)
else:
	dataframe = pd.read_csv(csv_file)
	num_columns = len(dataframe.columns)
	dataframe[f"caption-{num_columns}"] = [res["text"] for res in result]
	logger.info(f"Saving new captions in the column 'caption-{num_columns}'")

# save the dataframe to a csv file
dataframe.to_csv(csv_file, index=False)

# copy the audio files to the output directory
if fresh_start:
	logger.info(f"Copying audio files to {audios_dir}")
	for audio_path, audio_filename in zip(
		audio_paths,
		new_audio_filenames,
		strict=False,
	):
		copyfile(audio_path, audios_dir / audio_filename)

logger.info(f"Results saved to {output_dir}")
