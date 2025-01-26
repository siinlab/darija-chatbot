import tempfile  # noqa: D100
import uuid
from enum import Enum
from pathlib import Path

import torch
import torchaudio

from models.fastpitch import FastPitch2Wave

# Define paths
_here = Path(__file__).resolve().parent
female_checkpoints_dir = _here.parent / "checkpoints"
male_checkpoints_dir = _here.parent / "checkpoints-mohamed"

# check if there's a cuda device
use_cuda = torch.cuda.is_available()

# cache models
models = {}


class Voice(str, Enum):  # noqa: D101
	MALE = "Male"
	FEMALE = "Female"

	def __str__(self) -> str:  # noqa: D105
		return self.value

	def __repr__(self) -> str:  # noqa: D105
		return self.value


def generate_path() -> Path:
	"""Generate a random wav file path.

	Returns:
		Path: The path to the generated wav file.
	"""
	# function to generate a random wav file
	name = f"test-{uuid.uuid4()!s}.wav"
	out_dir = tempfile.gettempdir()
	return (Path(out_dir) / name).as_posix()


def generate_wav(text: str, voice: Voice, checkpoint: str = "states_6000") -> str:
	"""Generate a wav file from the given text using the specified voice and checkpoint.

	Args:
		text (str): The text to convert to speech.
		voice (Voice): The voice to use for the speech synthesis.
		checkpoint (str): The checkpoint to use for the model.

	Returns:
		str: The path to the generated wav file.
	"""
	model_name = f"{voice}_{checkpoint}"
	if model_name not in models:
		if voice == Voice.MALE:
			ckpt_path = male_checkpoints_dir / f"{checkpoint}.pth"
		elif voice == Voice.FEMALE:
			ckpt_path = female_checkpoints_dir / f"{checkpoint}.pth"
		else:
			msg = "Unknown voice"
			raise ValueError(msg)
		model = FastPitch2Wave(ckpt_path)
		if use_cuda:
			model = model.cuda()
		models[model_name] = model
	else:
		model = models[model_name]
	wav = model.tts(text, speaker_id=0, phonemize=False)
	# save the wave to a file
	wav_path = generate_path()
	torchaudio.save(wav_path, wav.unsqueeze(0).cpu(), 22050)
	return wav_path
