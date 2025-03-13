"""Splits audio files into chunks based on silence."""

import os
from pathlib import Path

from lgg import logger
from pydub import AudioSegment
from pydub.silence import split_on_silence
from tqdm import tqdm

logger.setLevel("DEBUG")


def split_audio_on_silence(
	input_audio_path: str,
	output_dir: str,
	silence_thresh: int = -50,
	min_silence_len: int = 700,
	keep_silence: int = 500,
) -> None:
	"""Splits an audio file into chunks based on silence.

	:param input_audio_path: Path to the input audio file
	:param output_dir: Directory to save the split audio files
	:param silence_thresh: Silence threshold in dBFS
	:param min_silence_len: Minimum silence duration in milliseconds
	:param keep_silence: Amount of silence (in ms) to keep at the edges of chunks
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
		keep_silence=keep_silence,
		seek_step=50,
	)

	# if avg chunk duration is less than 3 seconds
	avg_chunk_duration = sum([len(chunk) for chunk in chunks]) / len(chunks)
	logger.info(f"Splitting {input_audio_path} into {len(chunks)} chunks.")
	logger.info("Average chunk duration: %.2f s", avg_chunk_duration / 1000)
	if avg_chunk_duration < 3_000:  # noqa: PLR2004
		split_audio_on_silence(
			input_audio_path,
			output_dir,
			silence_thresh - 5,
			min_silence_len + 70,
			keep_silence,
		)
		return
	# if the avg chunk duration is greater than 60 seconds
	if avg_chunk_duration > 30_000:  # noqa: PLR2004
		split_audio_on_silence(
			input_audio_path,
			output_dir,
			silence_thresh + 7,
			min_silence_len - 50,
			keep_silence,
		)
		return

	file_output_dir.mkdir(parents=True, exist_ok=True)

	# Save chunks
	for i, chunk in tqdm(enumerate(chunks)):
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
