"""Transcribe audio files using the Wav2Vec2 model."""
from pathlib import Path

import librosa
import pandas as pd
import torch
from transformers import (
	Wav2Vec2CTCTokenizer,
	Wav2Vec2ForCTC,
	Wav2Vec2Processor,
)

_here = Path(__file__).resolve().parent
_vocab_path = _here / "vocab.json"

_tokenizer = Wav2Vec2CTCTokenizer(
	_vocab_path,
	unk_token="[UNK]",  # noqa: S106
	pad_token="[PAD]",  # noqa: S106
	word_delimiter_token="|",  # noqa: S106
)
_processor = Wav2Vec2Processor.from_pretrained(
	"boumehdi/wav2vec2-large-xlsr-moroccan-darija",
	tokenizer=_tokenizer,
)
_model = Wav2Vec2ForCTC.from_pretrained("boumehdi/wav2vec2-large-xlsr-moroccan-darija")


def transcribe_audios(
	audio_paths: list[str],
	output_path: str,
	batch_size: int = 8,
) -> None:
	"""Transcribes the audio file located at the given audio_path.

	Args:
		audio_paths (list[str]): The path to the audio files.
		output_path (str): The path to the CSV file where the captions will be saved.
		batch_size (int): The batch size to use for transcribing the audio.
	"""
	captions = []
	for i in range(0, len(audio_paths), batch_size):
		audios = []
		for audio_path in audio_paths[i : i + batch_size]:
			# load the audio data
			input_audio, sr = librosa.load(audio_path, sr=16000)

			audios.append(input_audio)

		# tokenize
		input_values = _processor(
			audios,
			return_tensors="pt",
			padding=True,
		).input_values

		# retrieve logits
		logits = _model(input_values).logits

		tokens = torch.argmax(logits, axis=-1)

		# decode using n-gram
		transcription = _tokenizer.batch_decode(tokens)

		# append the transcription
		captions.extend(transcription)

	captions = [
		{"caption": caption, "audio_path": audio}
		for caption, audio in zip(captions, audio_paths, strict=False)
	]

	# save the captions in a CSV file
	csv_file = Path(output_path)
	csv_file.parent.mkdir(parents=True, exist_ok=True)
	dataframe = pd.DataFrame(captions)
	dataframe.to_csv(csv_file, index=False)


if __name__ == "__main__":
	audios_dir = Path(
		"/Users/ayoub/Desktop/Projects/darija-tts/data/sample-data/audios",
	)
	captions_path = Path(
		"/Users/ayoub/Desktop/Projects/darija-tts/data/sample-data/captions2.csv",
	)
	# get all audios files
	audios_files = [f for f in audios_dir.iterdir() if f.is_file()]
	# transcribe each audio file
	transcribe_audios(audios_files, captions_path)
