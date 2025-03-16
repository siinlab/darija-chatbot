"""This script prepares a dataset for training a Whisper ASR model.

It processes audio files and their corresponding transcripts, extracts features,
and saves the dataset in a format suitable for training.
"""

import argparse
import sys
from pathlib import Path
from typing import Any

import librosa
import psutil
from lgg import logger
from transformers import WhisperFeatureExtractor, WhisperTokenizerFast

from datasets import Dataset, disable_caching, load_dataset

parser = argparse.ArgumentParser(description="Prepare data for training")
parser.add_argument("--data-dir", type=str, required=True, help="Data directory")
parser.add_argument("--output-path", type=str, required=True, help="Output path")
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

logger.setLevel("DEBUG")

# Get the number of physical CPU cores
num_cores = psutil.cpu_count(logical=False) - 4
# Disable HF caching mechanism
disable_caching()

# Define a constant for the maximum label length
MAX_LABEL_LENGTH = 448
BATCH_SIZE = 16  # Adjust based on memory availability

# Load Whisper tokenizer and feature extractor
tokenizer = WhisperTokenizerFast.from_pretrained(
	whisper_version,
	language="Arabic",
	task="transcribe",
)
feature_extractor = WhisperFeatureExtractor.from_pretrained(whisper_version)

# Ensure data directory exists
if not data_dir.exists():
	logger.error(f"Data directory {data_dir} does not exist.")
	sys.exit(1)

# Ensure exactly one CSV file is present
csv_files = list(data_dir.glob("*.csv"))
if len(csv_files) != 1:
	logger.error(
		f"Expected exactly one CSV file in {data_dir}, found {len(csv_files)}.",
	)
	sys.exit(1)

# Ensure 'audios' directory exists
audios_dir = data_dir / "audios"
if not audios_dir.exists():
	logger.error(f"Directory {audios_dir} does not exist.")
	sys.exit(1)


def load_audio_data(csv_path: Path, audios_dir: Path) -> Dataset:
	"""Load audio data and transcripts from CSV file."""

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

	dataset = load_dataset("csv", data_files=csv_path.as_posix(), keep_in_memory=False)
	# dataset["train"] = dataset["train"].select(range(10000))  # noqa: ERA001
	return dataset.map(process_example, remove_columns=["caption"], num_proc=num_cores)


def prepare_dataset(batch: dict[str, Any]) -> dict[str, Any]:
	"""Processes dataset in batches to optimize speed."""
	audio_arrays = [sample["array"] for sample in batch["audio"]]
	sampling_rates = [sample["sampling_rate"] for sample in batch["audio"]]

	# Compute log-Mel spectrogram features in batch
	batch["input_features"] = feature_extractor(
		audio_arrays,
		sampling_rate=sampling_rates[0],
		device="cuda",
	).input_features

	# Encode target text to label IDs in batch
	batch["labels"] = tokenizer.batch_encode_plus(
		batch["sentence"],
		padding=False,  # No padding, return natural-length sequences
		return_tensors=None,  # Avoid converting to tensor (keeps list of lists)
	)["input_ids"]

	return batch


# Load dataset
logger.info(f"Loading audio data from {csv_files[0]} and {audios_dir}")
dataset = load_audio_data(csv_path=csv_files[0], audios_dir=audios_dir)

# Process dataset using batch processing and multiprocessing
dataset = dataset.map(prepare_dataset, batched=True, batch_size=BATCH_SIZE, num_proc=16)

# Filter out samples with long labels in batches
dataset = dataset.filter(
	lambda x: len(x["labels"]) <= MAX_LABEL_LENGTH,
	num_proc=num_cores,
	batched=False,
)

# Print dataset overview
logger.info(f"Dataset overview:\n{dataset}")

# Save dataset to output path
logger.info(f"Saving dataset to {output_path}")
dataset.save_to_disk(output_path.as_posix(), num_proc=num_cores)
