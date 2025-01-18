from pathlib import Path
import os
import torchaudio
import sys

import shutil
import torch
import uuid
from models.fastpitch import FastPitch2Wave
from enum import Enum


class Voice(str, Enum):
	MALE = "Male"
	FEMALE = "Female"

	def __str__(self):
		return self.value

	def __repr__(self):
		return self.value


_here = Path(__file__).resolve().parent
female_checkpoints_dir = _here.parent / "checkpoints"
male_checkpoints_dir = _here.parent / "checkpoints-mohamed"

# check if there's a cuda device
use_cuda = torch.cuda.is_available()

# cache models
models = {}


def generate_path():
	# function to generate a random wav file
	name = f"test-{str(uuid.uuid4())}.wav"
	out_dir = "/tmp"
	return os.path.join(out_dir, name)


def generate_wav(text: str, voice: Voice, checkpoint: str = "states_6000") -> str:
	model_name = f"{voice}_{checkpoint}"
	if model_name not in models:
		if voice == Voice.MALE:
			ckpt_path = male_checkpoints_dir / f"{checkpoint}.pth"
		elif voice == Voice.FEMALE:
			ckpt_path = female_checkpoints_dir / f"{checkpoint}.pth"
		else:
			raise ValueError("Unknown voice")
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


if __name__ == "__main__":
	# test the function
	text = "السلام عليكم صاحبي"
	model_name = "states_6000"
	wav_path = generate_wav(text, model_name)
	print(f"Saved wav file to {wav_path}")
	print("Done")
