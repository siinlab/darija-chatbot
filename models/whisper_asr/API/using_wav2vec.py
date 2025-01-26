"""Transcribe audio to text using Wav2Vec2 model."""

from pathlib import Path

import librosa
import torch
from transformers import (
	Wav2Vec2CTCTokenizer,
	Wav2Vec2ForCTC,
	Wav2Vec2Processor,
)

_here = Path(__file__).resolve().parent

vocab_path = str(
	_here / "vocab.json",
)  # https://huggingface.co/boumehdi/wav2vec2-large-xlsr-moroccan-darija/resolve/main/vocab.json


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


def transcribe(wav_path: str) -> str:
	"""Transcribe the given wav file to text.

	Args:
		wav_path (str): The path to the wav file.

	Returns:
		str: The transcribed text.
	"""
	input_audio, _ = librosa.load(wav_path, sr=16000)

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
