"""This script provides functionality to augment audio datasets by merging multiple audio files.
with optional silence between them. The augmented dataset is saved in a specified output directory.

Functions:
- _load_datasets(root_dir: Path) -> list[dict[str, str]]:
	Loads all datasets from the specified root directory into memory. Each dataset folder should
	contain an "audios" directory and a "data.csv" file with audio file names and captions.

- _generate_augmented_dataset(
	num_augmented_samples: int = 1000
	Generates an augmented dataset by merging multiple audio files with optional silence between
	them. The merged audio files and their corresponding transcripts are saved in the output directory.

- augment_dataset(
	num_augmented_samples: int = 1000
	High-level function to load datasets and generate an augmented dataset. Combines the functionality
	of `_load_datasets` and `_generate_augmented_dataset`.

Command-line Usage:
	This script can be executed from the command line with the following arguments:
	- root_dir: Path to the root directory containing dataset folders.
	- output_dir: Path to the directory where the augmented dataset will be saved.
	- --max_num_audios_to_merge: Maximum number of audios to merge per sample (default: 2).
	- --silence_duration: Silence duration (ms) between merged audios (default: 200ms).
	- --num_augmented_samples: Number of augmented samples to generate (default: 1000).

Example:
	python concat_audios.py /path/to/datasets /path/to/output --max_num_audios_to_merge 3 --silence_duration 300 --num_augmented_samples 500
"""  # noqa: D205, E501

import argparse
import random
import shutil
from pathlib import Path

import pandas as pd
from lgg import logger
from pydub import AudioSegment


def _load_datasets(root_dir: Path) -> list[dict[str, str]]:
	"""Loads all datasets into memory without saving to disk.

	Parameters:
	- root_dir (str or Path): Root directory containing dataset folders.

	Returns:
	- data (list of dicts): List containing {"audio": Path, "caption": str}.
	"""
	root_path = Path(root_dir)
	data = []

	for dataset_folder in root_path.iterdir():
		if not dataset_folder.is_dir():
			continue

		audio_dir = dataset_folder / "audios"
		csv_path = dataset_folder / "data.csv"

		if not audio_dir.exists() or not csv_path.exists():
			continue  # Skip invalid datasets

		dataframe = pd.read_csv(csv_path)

		for _, row in dataframe.iterrows():
			audio_path = audio_dir / row["audio"]
			if audio_path.exists():
				data.append({"audio": audio_path, "caption": row["caption"]})

	logger.info(f"Loaded {len(data)} audio files from all datasets.")
	return data


def _generate_augmented_dataset(
	data: list[dict[str, str]],
	output_dir: Path,
	max_num_audios_to_merge: int = 2,
	silence_duration: int = 200,
	num_augmented_samples: int = 1000,
) -> None:
	"""Generates an augmented dataset by merging multiple audio files.

	Args:
		data (list[dict[str, str]]): List of {"audio": Path, "caption": str}.
		output_dir (Path): Directory to store augmented dataset.
		max_num_audios_to_merge (int): Maximum number of audios to merge.
		silence_duration (int): Silence duration (ms) between merged audios.
		num_augmented_samples (int): Number of augmented samples to generate.
	"""
	if len(data) < max_num_audios_to_merge:
		msg = "Not enough audio files to merge."
		raise ValueError(msg)

	if output_dir.exists():
		logger.warning(f"Removing the existing output directory {output_dir}")
		shutil.rmtree(output_dir)

	output_audio_path = output_dir / "audios"
	csv_file = output_dir / "data.csv"
	output_audio_path.mkdir(exist_ok=True, parents=True)

	new_entries = []

	for i in range(num_augmented_samples):
		num_audios_to_merge = random.randint(2, max_num_audios_to_merge)  # noqa: S311
		selected_files = random.sample(data, num_audios_to_merge)
		merged_audio = AudioSegment.empty()
		merged_transcript = ""

		for idx, item in enumerate(selected_files):
			audio = AudioSegment.from_file(item["audio"])
			if idx > 0:
				merged_audio += AudioSegment.silent(duration=silence_duration)
			merged_audio += audio

			merged_transcript += " " + item["caption"]

		# Trim merged transcript
		merged_transcript = merged_transcript.strip()

		new_filename = f"merged_{i}.wav"
		new_audio_path = output_audio_path / new_filename
		merged_audio.export(new_audio_path, format="wav")

		new_entries.append({"filename": new_filename, "transcript": merged_transcript})

	new_df = pd.DataFrame(new_entries)
	new_df.to_csv(csv_file, index=False)

	logger.info(f"Augmented dataset saved in: {output_dir}")


def augment_dataset(
	root_dir: Path,
	output_dir: Path,
	max_num_audios_to_merge: int = 2,
	silence_duration: int = 200,
	num_augmented_samples: int = 1000,
) -> None:
	"""Generates an augmented dataset by merging multiple audio files.

	Args:
		root_dir (Path): Root directory containing dataset folders.
		output_dir (Path): Directory to store augmented dataset.
		max_num_audios_to_merge (int): Maximum number of audios to merge.
		silence_duration (int): Silence duration (ms) between merged audios.
		num_augmented_samples (int): Number of augmented samples to generate.
	"""
	data = _load_datasets(root_dir)
	_generate_augmented_dataset(
		data,
		output_dir,
		max_num_audios_to_merge,
		silence_duration,
		num_augmented_samples,
	)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description="Generate an augmented dataset by merging audio files.",
	)

	parser.add_argument(
		"root_dir",
		type=Path,
		help="Path to the root directory containing dataset folders.",
	)
	parser.add_argument(
		"output_dir",
		type=Path,
		help="Path to the directory where the augmented dataset will be saved.",
	)
	parser.add_argument(
		"--max_num_audios_to_merge",
		type=int,
		default=2,
		help="Maximum number of audios to merge per sample (default: 2).",
	)
	parser.add_argument(
		"--silence_duration",
		type=int,
		default=200,
		help="Silence duration (ms) between merged audios (default: 200ms).",
	)
	parser.add_argument(
		"--num_augmented_samples",
		type=int,
		default=1000,
		help="Number of augmented samples to generate (default: 1000).",
	)

	args = parser.parse_args()

	augment_dataset(
		root_dir=args.root_dir,
		output_dir=args.output_dir,
		max_num_audios_to_merge=args.max_num_audios_to_merge,
		silence_duration=args.silence_duration,
		num_augmented_samples=args.num_augmented_samples,
	)
