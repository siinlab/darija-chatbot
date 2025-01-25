"""Train the Whisper model on the Arabic ASR task."""

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Union

import evaluate
import torch
from datasets import load_from_disk
from lgg import logger
from transformers import (
	Seq2SeqTrainer,
	Seq2SeqTrainingArguments,
	WhisperFeatureExtractor,
	WhisperForConditionalGeneration,
	WhisperProcessor,
	WhisperTokenizer,
)

parser = argparse.ArgumentParser(
	description="Train the Whisper model on the Arabic ASR task.",
)
parser.add_argument("--data-dir", type=str, required=True, help="HF dataset directory")
parser.add_argument(
	"--output-dir",
	type=str,
	required=True,
	help="output dir of model checkpoint",
)
parser.add_argument(
	"--whisper-version",
	type=str,
	default="openai/whisper-small",
	help="Whisper model version",
)
args = parser.parse_args()

data_dir = Path(args.data_dir)
output_dir = Path(args.output_dir)
whisper_version = args.whisper_version

# load the Whisper tokenizer and feature extractor
tokenizer = WhisperTokenizer.from_pretrained(
	whisper_version,
	language="Arabic",
	task="transcribe",
)
processor = WhisperProcessor.from_pretrained(
	whisper_version,
	language="Arabic",
	task="transcribe",
)
feature_extractor = WhisperFeatureExtractor.from_pretrained(whisper_version)
model = WhisperForConditionalGeneration.from_pretrained(whisper_version)
model.config.forced_decoder_ids = None
model.config.suppress_tokens = []

# check if the data directory exists
if not data_dir.exists():
	logger.error(f"Data directory {data_dir} does not exist.")
	sys.exit(1)

# create the output directory if it doesn't exist
if not output_dir.exists():
	logger.debug(f"Output directory {output_dir} doesn't exist. Creating it.")
	output_dir.mkdir(parents=True, exist_ok=False)


@dataclass
class DataCollatorSpeechSeq2SeqWithPadding:
	processor: Any

	def __call__(
		self, features: List[Dict[str, Union[List[int], torch.Tensor]]]
	) -> Dict[str, torch.Tensor]:
		# split inputs and labels since they have to be of different lengths
		# and need different padding methods
		# first treat the audio inputs by simply returning torch tensors  # noqa: ERA001
		input_features = [
			{"input_features": feature["input_features"]} for feature in features
		]
		batch = self.processor.feature_extractor.pad(
			input_features,
			return_tensors="pt",
		)

		# get the tokenized label sequences
		label_features = [{"input_ids": feature["labels"]} for feature in features]
		# pad the labels to max length
		labels_batch = self.processor.tokenizer.pad(label_features, return_tensors="pt")

		# replace padding with -100 to ignore loss correctly
		labels = labels_batch["input_ids"].masked_fill(
			labels_batch.attention_mask.ne(1), -100
		)

		# if bos token is appended in previous tokenization step,
		# cut bos token here as it's append later anyways
		if (labels[:, 0] == self.processor.tokenizer.bos_token_id).all().cpu().item():
			labels = labels[:, 1:]

		batch["labels"] = labels

		return batch


def compute_metrics(pred):
	pred_ids = pred.predictions
	label_ids = pred.label_ids

	# replace -100 with the pad_token_id
	label_ids[label_ids == -100] = tokenizer.pad_token_id

	# we do not want to group tokens when computing the metrics
	pred_str = tokenizer.batch_decode(pred_ids, skip_special_tokens=True)
	label_str = tokenizer.batch_decode(label_ids, skip_special_tokens=True)

	wer = 100 * metric.compute(predictions=pred_str, references=label_str)

	return {"wer": wer}


# load dataset from disk: data_dir
dataset = load_from_disk(data_dir)

data_collator = DataCollatorSpeechSeq2SeqWithPadding(processor=processor)
metric = evaluate.load("wer")

training_args = Seq2SeqTrainingArguments(
	output_dir="./whisper-large-v3-ur",  # change to a repo name of your choice
	per_device_train_batch_size=16,
	gradient_accumulation_steps=1,  # increase by 2x for every 2x decrease in batch size
	learning_rate=1e-5,
	warmup_steps=500,
	max_steps=150,
	gradient_checkpointing=True,
	fp16=True,
	evaluation_strategy="steps",
	per_device_eval_batch_size=8,
	predict_with_generate=True,
	generation_max_length=225,
	save_steps=1000,
	eval_steps=1000,
	logging_steps=25,
	report_to=["tensorboard"],
	load_best_model_at_end=True,
	metric_for_best_model="wer",
	greater_is_better=False,
	push_to_hub=False,
)


trainer = Seq2SeqTrainer(
	args=training_args,
	model=model,
	train_dataset=dataset["train"],
	eval_dataset=dataset["train"],
	data_collator=data_collator,
	compute_metrics=compute_metrics,
	tokenizer=processor.feature_extractor,
)

processor.save_pretrained(training_args.output_dir)
