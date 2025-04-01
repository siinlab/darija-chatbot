"""This module splits audio files into smaller chunks using Whisper."""

import argparse
import json
import sys
from pathlib import Path

import torch
import torchaudio
import whisper_timestamped as whisper
from lgg import logger
from matplotlib import pyplot as plt
from tqdm import tqdm

parser = argparse.ArgumentParser(description="Split audio files into smaller chunks")
parser.add_argument("audio_file", type=Path, help="The path to the audio file to split")
parser.add_argument(
	"output_dir",
	type=Path,
	help="The directory to save the split audio files",
)
parser.add_argument(
	"--min_silence_duration",
	type=int,
	default=200,
	help="The minimum duration of silence in milliseconds to split the audio",
)

args = parser.parse_args()
audio_file = args.audio_file
output_dir = args.output_dir
min_silence_duration = args.min_silence_duration

# check that the audio file exists
if not audio_file.exists():
	logger.error(f"Audio file {audio_file} does not exist")
	sys.exit(1)

# if the output directory does not exist, create it
if output_dir.exists():
	logger.warning(f"Output directory {output_dir} already exists")
	sys.exit(1)

output_dir.mkdir(parents=True)

# ensure cuda is available
if not torch.cuda.is_available():
	logger.error("CUDA is not available")
	sys.exit(1)

# Load audio file
audio = whisper.load_audio(audio_file.as_posix())
# Load the model
model = whisper.load_model("openai/whisper-large-v3", device="cuda:0")
# Split the audio file into chunks
try:
	result = whisper.transcribe(model, audio, language="ar")
except Exception as e:  # noqa: BLE001
	logger.error(f"Error occurred while inferring timestamps: {e}")
	output_dir.rmdir()
	sys.exit(1)

# Extract words from the segments
words = []
for segment in result["segments"]:
	words.extend(segment["words"])

# Save the chunks to the output directory
with (output_dir / "words.json").open("w", encoding="utf-8") as f:
	f.write(json.dumps(words, indent=2, ensure_ascii=False, default=str))

logger.info(f"Found {len(result['segments'])} segments in the audio file")
logger.info(f"Found {len(words)} words in the audio file")

# Extract silence between words in milliseconds
starts = [int(word["start"] * 10**3) for word in words]
ends = [int(word["end"] * 10**3) for word in words]
silence_duration = [
	start - end for start, end in zip(starts[1:], ends[:-1], strict=False)
]

# Find silence periods with silence duration > min_silence_duration
silent_parts = {
	i: duration
	for i, duration in enumerate(silence_duration)
	if duration > min_silence_duration
}

logger.info(
	f"Found {len(silent_parts)} words with silence duration > {min_silence_duration}ms",
)


def _plot_silence_timeline(silence_duration: list[int]) -> None:
	x = range(len(silence_duration))
	y = silence_duration

	fig, ax = plt.subplots(figsize=(10, 6))

	# Create the bar plot
	bars = ax.bar(x, y)

	# Add exact values above each bar
	for bar in bars:
		height = bar.get_height()
		x_pos = bar.get_x() + bar.get_width() / 2.0
		ax.text(
			x_pos,
			height,
			f"x:{int(x_pos)}\ny:{height}",  # Show both x and y values
			ha="center",
			va="bottom",
			rotation=0,
			fontsize=4,
		)

	# Add grid for better readability
	ax.grid(axis="y", linestyle="--", alpha=0.7)

	# Set descriptive labels
	ax.set_xlabel("X Values", fontsize=12)
	ax.set_ylabel("Y Values", fontsize=12)
	ax.set_title("Bar Chart with Data Labels", fontsize=14)

	# Use logarithmic scale for y-axis to better visualize data distribution
	ax.set_yscale("log")

	# Show the plot
	plt.tight_layout()
	plt.savefig(output_dir / "word_timeline.svg")


# Plot silence timeline
_plot_silence_timeline(silence_duration)

# split and save audio to segments
waveform, sample_rate = torchaudio.load(audio_file.as_posix())


def _save_audio_segment(start: float, end: float, index: int) -> None:
	start_sample = int(start / (10**3) * sample_rate)
	end_sample = int(end / (10**3) * sample_rate)
	segment = waveform[:, start_sample:end_sample]
	segment_path = output_dir / "audios" / (f"segment_{index:04d}" + audio_file.suffix)
	torchaudio.save(segment_path.as_posix(), segment, sample_rate)


# make the audio directory
audio_dir = output_dir / "audios"
audio_dir.mkdir(exist_ok=True)

start = starts[0]
# save the audio segments
for index in tqdm(silent_parts, desc="Saving audio segments"):
	_save_audio_segment(start, ends[index] + min(100, min_silence_duration // 2), index)
	start = starts[index + 1]

logger.info(f"Split audio files saved to {output_dir}")
