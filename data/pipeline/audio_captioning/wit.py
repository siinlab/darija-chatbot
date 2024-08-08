"""This module is responsible for transcribing audio files using the Wit.ai API,
and saving the generated captions in a CSV file.
"""  # noqa: D205

from collections import deque
from pathlib import Path

import pandas as pd
from lgg import logger
from tafrigh import Config, farrigh

# Define Wit.ai API keys for languages
WTI_API_KEY = "LFW3IZAW7KPOV6X3TV2I67A6QJH4OHX4"


def transcribe_files(file_paths: list[str], output_path: str) -> None:
	"""Transcribe the given audio file using the Wit.ai API.

	Args:
		file_paths (list[str]): The path to the audio file.
		output_path (str): The path to the CSV file where the captions will be saved.
	"""
	output_dir = Path("~/.cache/tafrigh/captions").expanduser()
	# Delete the output directory if it exists
	if output_dir.exists():
		for file in output_dir.iterdir():
			file.unlink()
	else:
		output_dir.mkdir(parents=True)

	config = Config(
		input=Config.Input(
			urls_or_paths=file_paths,
			skip_if_output_exist=False,
			playlist_items="",
			download_retries=3,
			verbose=False,
		),
		whisper=Config.Whisper(
			model_name_or_path="tiny",
			task="transcribe",
			language="ar",
			use_faster_whisper=True,
			beam_size=5,
			ct2_compute_type="default",
		),
		wit=Config.Wit(
			wit_client_access_tokens=[WTI_API_KEY],
			max_cutting_duration=10,
		),
		output=Config.Output(
			min_words_per_segment=10,
			save_files_before_compact=False,
			save_yt_dlp_responses=False,
			output_sample=0,
			output_formats=["txt"],
			output_dir=output_dir,
		),
	)

	deque(farrigh(config), maxlen=0)
	logger.debug("Transcription completed.")
	captions = []
	# Load all txt files in the output directory
	for audio_file in file_paths:
		# get the audio file name with the extension
		full_file_name = audio_file.stem + audio_file.suffix
		# get the audio file name
		audio_file_name = audio_file.stem
		# get the generated caption file
		caption_file = output_dir / f"{audio_file_name}.txt"
		# read the caption file
		with caption_file.open() as f:
			lines = f.readlines()
			all_in_one = " ".join(lines)
			all_in_one = " ".join(all_in_one.split())
		captions.append({"caption": all_in_one, "audio_path": full_file_name})
	# save captions in a CSV file
	csv_file = Path(output_path)
	csv_file.parent.mkdir(parents=True, exist_ok=True)
	dataframe = pd.DataFrame(captions)
	dataframe.to_csv(csv_file, index=False)


if __name__ == "__main__":
	audios_dir = Path(
		"/Users/ayoub/Desktop/Projects/darija-tts/data/sample-data/audios",
	)
	captions_path = Path(
		"/Users/ayoub/Desktop/Projects/darija-tts/data/sample-data/captions.csv",
	)
	# get all audios files
	audios_files = [f for f in audios_dir.iterdir() if f.is_file()]
	# transcribe each audio file
	transcribe_files(audios_files, captions_path)
