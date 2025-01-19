from pathlib import Path
import os
import torchaudio
import sys

import shutil
import torch
import uuid
from models.fastpitch import FastPitch2Wave
from enum import Enum

import librosa
import torch
from transformers import Wav2Vec2CTCTokenizer, Wav2Vec2ForCTC, Wav2Vec2Processor, TrainingArguments, Wav2Vec2FeatureExtractor, Trainer
from transformers import pipeline

# Define paths
_here = Path(__file__).resolve().parent
female_checkpoints_dir = _here.parent / "checkpoints"
male_checkpoints_dir = _here.parent / "checkpoints-mohamed"
vocab_path = str(_here / "vocab.json") # https://huggingface.co/boumehdi/wav2vec2-large-xlsr-moroccan-darija/resolve/main/vocab.json

# check if there's a cuda device
use_cuda = torch.cuda.is_available()

# cache models
models = {}

# Transcription model: https://huggingface.co/boumehdi/wav2vec2-large-xlsr-moroccan-darija
transcription_tokenizer = Wav2Vec2CTCTokenizer(vocab_path, unk_token="[UNK]", pad_token="[PAD]", word_delimiter_token="|")
transcription_processor = Wav2Vec2Processor.from_pretrained('boumehdi/wav2vec2-large-xlsr-moroccan-darija', tokenizer=transcription_tokenizer)
transcription_model = Wav2Vec2ForCTC.from_pretrained('boumehdi/wav2vec2-large-xlsr-moroccan-darija')

# Chat model: https://huggingface.co/MBZUAI-Paris/Atlas-Chat-2B
chat_pipeline = pipeline(
    "text-generation",
    model="MBZUAI-Paris/Atlas-Chat-2B",
    model_kwargs={"torch_dtype": torch.bfloat16},
    device="cuda" if use_cuda else "cpu",
)


class Voice(str, Enum):
	MALE = "Male"
	FEMALE = "Female"

	def __str__(self):
		return self.value

	def __repr__(self):
		return self.value


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


def transcribe(wav_path: str):
	# load the audio data (use your own wav file here!)
	input_audio, sr = librosa.load(wav_path, sr=16000)

	# tokenize
	input_values = transcription_processor(input_audio, return_tensors="pt", padding=True).input_values

	# retrieve logits
	logits = transcription_model(input_values).logits

	# take argmax and decode
	tokens = torch.argmax(logits, axis=-1)

	# decode using n-gram
	transcription = transcription_tokenizer.batch_decode(tokens)

	# return the output
	return transcription

import anthropic
client = anthropic.Anthropic(
    api_key=ANTHROPIC_API_KEY,
)

def respond(messages):
	# outputs = chat_pipeline(messages, max_new_tokens=256, temperature=0.1)
	# assistant_response = outputs[0]["generated_text"][-1]["content"].strip()
    messages[0]["content"] = "انا كندوي بالدارجة و بغيت تبقى تجاوبني بها و بغيتك تبقى تجاوبني بلا حروف لاتينية و بلا ارقام:\n" + messages[0]["content"]
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=512,
        messages=messages
    )
    assistant_response = message.content[0].text
    
    return assistant_response

if __name__ == "__main__":
	# test the function
	text = "السلام عليكم صاحبي"
	model_name = "states_6000"
	wav_path = generate_wav(text, model_name)
	print(f"Saved wav file to {wav_path}")
	print("Done")
