import tempfile  # noqa: D100
import uuid
from enum import Enum
from pathlib import Path

import torch
import torchaudio

from .utils import append_to_sys_path

append_to_sys_path()

from models.fastpitch import FastPitch2Wave  # noqa: E402


class Speaker(str, Enum):  # noqa: D101
	MALE = "Male"
	FEMALE = "Female"
	RANDOM = "Random"

	def __str__(self) -> str:  # noqa: D105
		return self.value

	def __repr__(self) -> str:  # noqa: D105
		return self.value


# Define paths
_here = Path(__file__).resolve().parent

# check if there's a cuda device
use_cuda = torch.cuda.is_available()

# Define where the model is stored for each speaker
speaker_models = {
	Speaker.MALE: _here.parent / "checkpoints-male" / "states_6000.pth",
	Speaker.FEMALE: _here.parent / "checkpoints-female" / "states_6000.pth",
	Speaker.RANDOM: _here.parent / "checkpoints" / "states.pth",
}

# cache models
models_cache = {}


def generate_path() -> Path:
	"""Generate a random wav file path.

	Returns:
		Path: The path to the generated wav file.
	"""
	# function to generate a random wav file
	name = f"test-{uuid.uuid4()!s}.wav"
	out_dir = tempfile.gettempdir()
	return (Path(out_dir) / name).as_posix()


def generate_wav(text: str, speaker: Speaker) -> str:
	"""Generate a wav file from the given text using the specified speaker.

	Args:
		text (str): The text to convert to speech.
		speaker (Speaker): The speaker to use.

	Returns:
		str: The path to the generated wav file.
	"""
	if speaker not in models_cache:
		if speaker in speaker_models:
			ckpt_path = speaker_models[speaker]
		else:
			msg = "Unknown voice"
			raise ValueError(msg)
		model = FastPitch2Wave(ckpt_path)
		if use_cuda:
			model = model.cuda()
		models_cache[speaker] = model
	else:
		model = models_cache[speaker]
	# Split the text into parts based on delimeters
	texts, silence_durations = split_text(text)
	# Generate the wav file
	waves = model.tts(
		texts,
		speaker_id=0,
		phonemize=False,
		speed=1,
		denoise=0.005,
		pitch_add=0,
		pitch_mul=1,
		batch_size=8,
	)
	# add silence between parts
	sample_rate = 22050
	wav = waves[0]
	for i in range(1, len(waves)):
		silence_duration = silence_durations[i - 1]
		silence = torch.zeros(int(silence_duration / 1000 * sample_rate))
		wav = torch.cat([wav, silence, waves[i]], dim=0)
	# save the wav to a file
	wav_path = generate_path()
	torchaudio.save(wav_path, wav.unsqueeze(0).cpu(), sample_rate)
	return wav_path


def split_text(text: str) -> tuple[list[str], list[int]]:
	"""Split the text into parts based on delimeters.

	Args:
		text (str): The text to split.

	Returns:
		tuple: A tuple containing a list of text parts
			and a list of silence durations in ms.
	"""
	delimeters = {
		".": 200,
		"،": 100,
		"?": 200,
		"؟": 200,
		"!": 200,
		"\n": 200,
	}
	# Remove redundant spaces
	text = " ".join(text.split())
	# Remove redundant delimeters
	for delim in delimeters:
		text = delim.join(list(text.split(delim)))
	# Split the text by delimeters
	texts = []
	current_text = ""
	silence_durations = []
	for i in range(len(text)):
		char = text[i]
		current_text += char
		if char in delimeters:
			texts.append(current_text)
			silence_durations.append(delimeters[char])
			current_text = ""
	if current_text:
		texts.append(current_text)
		silence_durations.append(0)
	return texts, silence_durations
