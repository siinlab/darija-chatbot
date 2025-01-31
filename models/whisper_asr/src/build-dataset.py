"""Prepare data for training the Whisper model on the Arabic ASR task."""

import argparse
import sys
from pathlib import Path
from typing import Any

import librosa
import psutil
from datasets import Dataset, load_dataset
from lgg import logger
from transformers import WhisperFeatureExtractor, WhisperTokenizer

# get number of physical CPU cores
num_cores = psutil.cpu_count(logical=False) // 2

parser = argparse.ArgumentParser(description="Prepare data for training")
parser.add_argument("--data-dir", type=str, required=True, help="data directory")
parser.add_argument("--output-path", type=str, required=True, help="output path")
parser.add_argument(
	"--whisper-version",
	type=str,
	default="openai/whisper-small",
	help="Whisper model version",
)
args = parser.parse_args()

data_dir = Path(args.data_dir)
output_path = Path(args.output_path)
whisper_version = args.whisper_version

# load the Whisper tokenizer and feature extractor
tokenizer = WhisperTokenizer.from_pretrained(
	whisper_version,
	language="Arabic",
	task="transcribe",
)
feature_extractor = WhisperFeatureExtractor.from_pretrained(whisper_version, device=0)

# read the output directory
output_dir = output_path.parent

# check if the data directory exists
if not data_dir.exists():
	logger.error(f"Data directory {data_dir} does not exist.")
	sys.exit(1)

# check if there's exactly one CSV file in the data directory
csv_files = list(data_dir.glob("*.csv"))
if len(csv_files) != 1:
	logger.error(
		f"Expected exactly one CSV file in {data_dir}, "
		f"but found {len(csv_files)} files.",
	)
	sys.exit(1)

# check if the there's an "audios" directory in the data directory
audios_dir = data_dir / "audios"
if not audios_dir.exists():
	logger.error(f"Directory {audios_dir} does not exist.")
	sys.exit(1)

# create the output directory if it doesn't exist
if not output_dir.exists():
	logger.debug(f"Output directory {output_dir} doesn't exist. Creating it.")
	output_dir.mkdir(parents=True, exist_ok=False)


def load_audio_data(csv_path: Path, audios_dir: Path) -> Dataset:
	"""Load audio data and transcripts from a CSV file and audio directory.

	Args:
		csv_path (Path): Path to the CSV file containing audio paths and transcripts.
		audios_dir (Path): Path to the directory containing audio files.

	Returns:
		Dataset: A dataset containing audio data and corresponding transcripts.
	"""

	def process_example(example: dict) -> dict:
		audio_path = (audios_dir / example["audio"]).as_posix()
		audio_array, sr = librosa.load(audio_path, sr=16000)
		return {
			"audio": {
				"path": example["audio"],
				"array": audio_array,
				"sampling_rate": sr,
			},
			"sentence": example["caption"],
		}

	dataset = load_dataset("csv", data_files=csv_path.as_posix())

	return dataset.map(process_example, remove_columns=["caption"])


def prepare_dataset(batch: dict[str, Any]) -> dict[str, Any]:
	"""Prepares the dataset by processing the audio data and encoding the target text.

	Args:
		batch (Dict[str, Any]): A dictionary containing the audio data and target text.
			- "audio" (Dict[str, Any]): A dictionary with keys:
				- "array" (np.ndarray): The audio signal array.
				- "sampling_rate" (int): The sampling rate of the audio signal.
			- "sentence" (str): The target text to be encoded.

	Returns:
		Dict[str, Any]: A dictionary with the processed input features and encoded labels.
			- "input_features" (np.ndarray): The log-Mel input features computed from the audio array.
			- "labels" (List[int]): The encoded label ids for the target text.
	"""  # noqa: E501
	# load and resample audio data from 48 to 16kHz
	audio = batch["audio"]

	# compute log-Mel input features from input audio array
	batch["input_features"] = feature_extractor(
		audio["array"],
		sampling_rate=audio["sampling_rate"],
	).input_features[0]

	# encode target text to label ids
	batch["labels"] = tokenizer(batch["sentence"]).input_ids
	return batch


# load the audio data
logger.info(f"Loading audio data from {csv_files[0]} and {audios_dir}")
dataset = load_audio_data(csv_path=csv_files[0], audios_dir=audios_dir)

# Preprocess the dataset
dataset = dataset.map(prepare_dataset, num_proc=num_cores)

# print datset overview
logger.info(f"Dataset overview:\n{dataset}")

# save the dataset to the output directory
logger.info(f"Saving dataset to {output_path}")
dataset.save_to_disk(output_path.as_posix())
