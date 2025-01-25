import argparse
import shutil
import sys
from pathlib import Path

import librosa
from datasets import Dataset, load_dataset
from lgg import logger

parser = argparse.ArgumentParser(description="Prepare data for training")
parser.add_argument("--data-dir", type=str, required=True, help="data directory")
parser.add_argument("--output-path", type=str, required=True, help="output path")
args = parser.parse_args()

data_dir = Path(args.data_dir)
output_path = Path(args.output_path)
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

	def process_example(example):
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

# load the audio data
logger.info(f"Loading audio data from {csv_files[0]} and {audios_dir}")
dataset = load_audio_data(csv_path=csv_files[0], audios_dir=audios_dir)

# save the dataset to the output directory
logger.info(f"Saving dataset to {output_path}")
dataset.save_to_disk(output_path.as_posix())
