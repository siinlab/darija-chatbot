"""Speeds up audio files to generate an augmented dataset."""

import argparse
import random
import shutil
from pathlib import Path

import pandas as pd
from joblib import Parallel, delayed
from lgg import logger
from pydub import AudioSegment
from tqdm import tqdm

logger.setLevel("DEBUG")


def _load_datasets(root_dir: Path) -> list[dict[str, str]]:
	"""Loads all datasets into memory.

	Parameters:
	- root_dir (Path): Root directory containing dataset folders.

	Returns:
	- data (list of dicts): List containing {"audio": Path, "caption": str}.
	"""
	root_path = Path(root_dir)
	data = []

	for dataset_folder in tqdm(root_path.iterdir(), desc="Loading datasets"):
		if not dataset_folder.is_dir():
			continue

		audio_dir = dataset_folder / "audios"
		csv_path = dataset_folder / "data.csv"

		if not audio_dir.exists() or not csv_path.exists():
			continue  # Skip invalid datasets

		try:
			dataframe = pd.read_csv(csv_path)
		except pd.errors.ParserError:
			logger.warning(f"Failed to load {csv_path}. Trying with ';' separator.")
			dataframe = pd.read_csv(csv_path, sep=";")

		for _, row in dataframe.iterrows():
			try:
				audio_path = audio_dir / row["audio"]
			except Exception as e:  # noqa: BLE001
				logger.warning(f"Failed to load audio file: {e}")
				continue
			if audio_path.exists():
				data.append({"audio": audio_path, "caption": row["caption"]})

	logger.info(f"Loaded {len(data)} audio files from all datasets.")
	return data


def _speed_up_audio(audio: AudioSegment, speed_factor: float) -> AudioSegment:
	"""Speeds up an audio file without changing pitch.

	Args:
		audio (AudioSegment): The original audio.
		speed_factor (float): Factor to speed up audio (e.g., 1.2 for 20% faster).

	Returns:
		AudioSegment: The sped-up audio.
	"""
	return audio.speedup(playback_speed=speed_factor)


def _generate_augmented_dataset(
	data: list[dict[str, str]],
	output_dir: Path,
	min_speed: float,
	max_speed: float,
	num_augmented_samples: int,
) -> None:
	"""Generates an augmented dataset by speeding up audio files.

	Args:
		data (list[dict[str, str]]): List of {"audio": Path, "caption": str}.
		output_dir (Path): Directory to store augmented dataset.
		min_speed (float): Minimum speed-up factor.
		max_speed (float): Maximum speed-up factor.
		num_augmented_samples (int): Number of augmented samples to generate.
	"""
	if len(data) == 0:
		msg = "No audio files found in dataset."
		raise ValueError(msg)

	output_audio_path = output_dir / "audios"
	csv_file = output_dir / "data.csv"
	output_audio_path.mkdir(exist_ok=True, parents=True)

	new_entries = []

	def process_sample(i: int):  # noqa: ANN202
		item = random.choice(data)  # Select a random audio file  # noqa: S311
		audio = AudioSegment.from_file(item["audio"])

		speed_factor = random.uniform(  # noqa: S311
			min_speed,
			max_speed,
		)  # Pick a random speed-up factor
		try:
			augmented_audio = _speed_up_audio(audio, speed_factor)
		except Exception:  # noqa: BLE001
			return process_sample(i)  # Retry if an error occurs

		extension = item["audio"].suffix
		new_filename = f"sped_up_{i}{extension}"
		new_audio_path = output_audio_path / new_filename
		augmented_audio.export(new_audio_path, format=extension.lstrip("."))

		return {"audio": new_filename, "caption": item["caption"]}

	logger.info(f"Generating {num_augmented_samples} augmented samples.")
	new_entries = Parallel(n_jobs=8)(
		delayed(process_sample)(i) for i in range(num_augmented_samples)
	)

	logger.info("Saving augmented CSV file to disk.")
	new_df = pd.DataFrame(new_entries)
	new_df.to_csv(csv_file, index=False)

	logger.info(f"Augmented dataset saved in: {output_dir}")


def augment_dataset(
	root_dir: Path,
	output_dir: Path,
	min_speed: float,
	max_speed: float,
	num_augmented_samples: int,
) -> None:
	"""Generates an augmented dataset by speeding up audio files.

	Args:
		root_dir (Path): Root directory containing dataset folders.
		output_dir (Path): Directory to store augmented dataset.
		min_speed (float): Minimum speed-up factor.
		max_speed (float): Maximum speed-up factor.
		num_augmented_samples (int): Number of augmented samples to generate.
	"""
	# Delete the existing output directory if it exists
	if output_dir.exists():
		logger.warning(f"Removing the existing output directory {output_dir}")
		shutil.rmtree(output_dir)
	# Load datasets and generate augmented dataset
	data = _load_datasets(root_dir)
	# Generate augmented dataset
	_generate_augmented_dataset(
		data,
		output_dir,
		min_speed,
		max_speed,
		num_augmented_samples,
	)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description="Generate an augmented dataset by speeding up audio files.",
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
		"--min_speed",
		type=float,
		default=1.1,
		help="Minimum speed-up factor (default: 1.1).",
	)
	parser.add_argument(
		"--max_speed",
		type=float,
		default=1.5,
		help="Maximum speed-up factor (default: 1.5).",
	)
	parser.add_argument(
		"--num_augmented_samples",
		type=int,
		default=100,
		help="Number of augmented samples to generate (default: 100).",
	)

	args = parser.parse_args()

	augment_dataset(
		root_dir=args.root_dir,
		output_dir=args.output_dir,
		min_speed=args.min_speed,
		max_speed=args.max_speed,
		num_augmented_samples=args.num_augmented_samples,
	)
