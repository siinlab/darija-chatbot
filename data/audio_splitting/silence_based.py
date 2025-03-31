"""Splits audio files into chunks based on silence."""

import os
from pathlib import Path

from lgg import logger
from pydub import AudioSegment
from pydub.silence import split_on_silence
from tqdm import tqdm

logger.setLevel("DEBUG")


def split_audio_on_silence(  # noqa: PLR0913
	input_audio_path: str,
	output_dir: str,
	silence_thresh: int = -50,
	min_silence_len: int = 700,
	seek_step: int = 10,
	min_duration: int = 1,
	max_duration: int = 30,
) -> None:
	"""Splits an audio file into chunks based on silence.

	:param input_audio_path: Path to the input audio file
	:param output_dir: Directory to save the split audio files
	:param silence_thresh: Silence threshold in dBFS
	:param min_silence_len: Minimum silence duration in milliseconds
	:param seek_step: Step size in milliseconds to seek for silence
	:param min_duration: minimum duration of an audio segment in seconds
	:param max_duration: maximum duration of an audio segment in seconds
	"""
	# Create a subdirectory for this file's chunks
	base_filename = Path(input_audio_path).stem
	file_output_dir = Path(output_dir) / base_filename
	# if file_output_dir exists, skip
	if file_output_dir.exists():
		logger.info(f"Skipping {input_audio_path} as it is already processed.")
		return

	# Load the audio file
	audio = AudioSegment.from_file(input_audio_path)

	# Split the audio based on silence
	chunks = split_on_silence(
		audio,
		min_silence_len=min_silence_len,
		silence_thresh=silence_thresh,
		keep_silence=True,
		seek_step=seek_step,
	)

	# if avg chunk duration is less than 3 seconds
	logger.info(f"Splitting {input_audio_path} into {len(chunks)} chunks.")

	# Create the output directory
	file_output_dir.mkdir(parents=True, exist_ok=True)

	# Save chunks
	for i, chunk in tqdm(enumerate(chunks)):
		# ensure the chunk is within the min and max duration
		if not (min_duration * 1000 <= len(chunk) <= max_duration * 1000):
			logger.debug(
				f"Skipping chunk {i + 1} as it is not within the duration limits.",
			)
		chunk_path = file_output_dir / f"chunk_{i + 1}.mp3"
		chunk.export(chunk_path, format="mp3")


def process_audio_folder(input_folder: str, output_dir: str) -> None:
	"""Processes all MP3 audio files in the given input folder by splitting them.

	Args:
		input_folder (str): The path to the folder containing the input MP3 audio files.
		output_dir (str): The path to the directory where the processed audio segments
						will be saved.

	Returns:
		None
	"""
	Path(output_dir).mkdir(parents=True, exist_ok=True)

	for filename in os.listdir(input_folder):
		if filename.lower().endswith(".mp3"):
			input_audio_path = Path(input_folder) / filename
			logger.info(f"Processing: {input_audio_path}")
			split_audio_on_silence(input_audio_path, output_dir)


if __name__ == "__main__":
	# Input directory containing MP3 files
	input_folder = "./raw-data"

	# Output directory for split audio files
	output_dir = "./splitted-audios"

	# Process all MP3 files in the folder
	process_audio_folder(input_folder, output_dir)
