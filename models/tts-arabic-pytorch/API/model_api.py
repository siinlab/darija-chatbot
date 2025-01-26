import tempfile  # noqa: D100
import uuid
from enum import Enum
from os import environ
from pathlib import Path

import anthropic
import librosa
import torch
import torchaudio
from lgg import logger
from transformers import (
	Wav2Vec2CTCTokenizer,
	Wav2Vec2ForCTC,
	Wav2Vec2Processor,
)

from models.fastpitch import FastPitch2Wave

# Define paths
_here = Path(__file__).resolve().parent
female_checkpoints_dir = _here.parent / "checkpoints"
male_checkpoints_dir = _here.parent / "checkpoints-mohamed"
vocab_path = str(
	_here / "vocab.json",
)  # https://huggingface.co/boumehdi/wav2vec2-large-xlsr-moroccan-darija/resolve/main/vocab.json

# check if there's a cuda device
use_cuda = torch.cuda.is_available()

# cache models
models = {}

# Transcription model: https://huggingface.co/boumehdi/wav2vec2-large-xlsr-moroccan-darija
transcription_tokenizer = Wav2Vec2CTCTokenizer(
	vocab_path,
	unk_token="[UNK]",  # noqa: S106
	pad_token="[PAD]",  # noqa: S106
	word_delimiter_token="|",  # noqa: S106
)
transcription_processor = Wav2Vec2Processor.from_pretrained(
	"boumehdi/wav2vec2-large-xlsr-moroccan-darija",
	tokenizer=transcription_tokenizer,
)
transcription_model = Wav2Vec2ForCTC.from_pretrained(
	"boumehdi/wav2vec2-large-xlsr-moroccan-darija",
)


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


def transcribe(wav_path: str) -> str:
	"""Transcribe the given wav file to text.

	Args:
		wav_path (str): The path to the wav file.

	Returns:
		str: The transcribed text.
	"""
	input_audio, sr = librosa.load(wav_path, sr=16000)

	# tokenize
	input_values = transcription_processor(
		input_audio,
		return_tensors="pt",
		padding=True,
	).input_values

	# retrieve logits
	logits = transcription_model(input_values).logits

	# take argmax and decode
	tokens = torch.argmax(logits, axis=-1)

	# decode using n-gram
	return transcription_tokenizer.batch_decode(tokens)


ANTHROPIC_API_KEY = environ["ANTHROPIC_API_KEY"]

client = anthropic.Anthropic(
	api_key=ANTHROPIC_API_KEY,
)


def respond(messages: list) -> str:
	"""Respond to messages using the Claude model.

	Args:
		messages (list): A list of message dictionaries.

	Returns:
		str: The response text from the Claude model.
	"""
	messages[0]["content"] = (
		"انا كندوي بالدارجة و بغيت تبقى تجاوبني بها و بغيتك تبقى تجاوبني بلا حروف لاتينية و بلا ارقام:\n"  # noqa: E501
		+ messages[0]["content"]
	)
	message = client.messages.create(
		model="claude-3-5-sonnet-20241022",
		max_tokens=512,
		messages=messages,
	)
	return message.content[0].text


if __name__ == "__main__":
	# test the function
	text = "السلام عليكم صاحبي"
	model_name = "states_6000"
	wav_path = generate_wav(text, model_name)
	logger.info(f"Saved wav file to {wav_path}")
	logger.info("Done")
