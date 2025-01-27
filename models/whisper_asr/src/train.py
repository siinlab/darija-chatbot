"""Train the Whisper model on the Arabic ASR task."""

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import evaluate
import psutil
import torch
from datasets import DatasetDict, load_from_disk
from lgg import logger
from transformers import (
	Seq2SeqTrainer,
	Seq2SeqTrainingArguments,
	WhisperFeatureExtractor,
	WhisperForConditionalGeneration,
	WhisperProcessor,
	WhisperTokenizer,
)

# get number of physical CPU cores
num_cores = psutil.cpu_count(logical=False) // 2

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
# Add hyperparameter arguments
parser.add_argument(
	"--per_device_train_batch_size",
	type=int,
	default=16,
	help="Batch size per device during training",
)
parser.add_argument(
	"--gradient_accumulation_steps",
	type=int,
	default=1,
	help="Number of gradient accumulation steps",
)
parser.add_argument(
	"--learning_rate",
	type=float,
	default=1e-5,
	help="Learning rate for the optimizer",
)
parser.add_argument(
	"--warmup_steps",
	type=int,
	default=500,
	help="Number of warmup steps for the scheduler",
)
parser.add_argument(
	"--max_steps",
	type=int,
	default=150,
	help="Total number of training steps",
)
parser.add_argument(
	"--fp16",
	action="store_true",
	help="Use fp16 mixed precision training",
)
parser.add_argument(
	"--evaluation_strategy",
	type=str,
	default="steps",
	help="Evaluation strategy to adopt during training",
)
parser.add_argument(
	"--per_device_eval_batch_size",
	type=int,
	default=8,
	help="Batch size per device for evaluation",
)
parser.add_argument(
	"--predict_with_generate",
	action="store_true",
	help="Use generate to calculate generative metrics",
)
parser.add_argument(
	"--generation_max_length",
	type=int,
	default=225,
	help="Maximum length of the sequence to be generated",
)
parser.add_argument(
	"--save_steps",
	type=int,
	default=1000,
	help="Number of update steps between two checkpoints",
)
parser.add_argument(
	"--eval_steps",
	type=int,
	default=1000,
	help="Number of steps between evaluations",
)
parser.add_argument(
	"--logging_steps",
	type=int,
	default=25,
	help="Log every X updates steps",
)

args = parser.parse_args()

data_dir = Path(args.data_dir)
output_dir = Path(args.output_dir)
whisper_version = args.whisper_version

IGNORE_INDEX = -100

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
	"""A data collator that pads the input features and labels for speech Seq2Seq tasks.

	Attributes:
		processor (Any): The processor used for feature extraction and tokenization.

	Methods:
		__call__(features: list[dict[str, list[int] | torch.Tensor]]) -> dict[str, torch.Tensor]:
			Collate and pad the input features and labels.

				features (list[dict[str, list[int] | torch.Tensor]]): A list of dictionaries containing input features and labels.

				dict[str, torch.Tensor]: A dictionary containing the padded input features and labels.
	processor: Any
	"""  # noqa: E501

	processor: Any

	def __call__(
		self,
		features: list[dict[str, list[int] | torch.Tensor]],
	) -> dict[str, torch.Tensor]:
		"""Collate and pad the input features and labels.

		Args:
			features (list[dict[str, list[int] | torch.Tensor]]): A list of dictionaries

		Returns:
			dict[str, torch.Tensor]: A dict containing the input features and labels.
		"""
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
			labels_batch.attention_mask.ne(1),
			IGNORE_INDEX,
		)

		# if bos token is appended in previous tokenization step,
		# cut bos token here as it's append later anyways
		if (labels[:, 0] == self.processor.tokenizer.bos_token_id).all().cpu().item():
			labels = labels[:, 1:]

		batch["labels"] = labels

		return batch


def compute_metrics(pred) -> dict[str, float]:  # noqa: ANN001
	"""Compute the Word Error Rate (WER) for the given predictions and labels.

	Args:
		pred (transformers.EvalPrediction): A named tuple with two fields:
			- predictions: The predicted token IDs.
			- label_ids: The true token IDs.

	Returns:
		dict: A dictionary containing the WER score with the key "wer".
	"""
	pred_ids = pred.predictions
	label_ids = pred.label_ids

	pred_ids = pred_ids[0]
	pred_ids = torch.tensor(pred_ids, device="cuda:0").argmax(axis=-1).cpu()  # 18s

	# replace -100 with the pad_token_id
	label_ids[label_ids == IGNORE_INDEX] = tokenizer.pad_token_id  # 1s

	# we do not want to group tokens when computing the metrics
	pred_str = tokenizer.batch_decode(pred_ids, skip_special_tokens=True)  # 9s
	label_str = tokenizer.batch_decode(label_ids, skip_special_tokens=True)  # 9s

	wer = 100 * metric.compute(predictions=pred_str, references=label_str)
	return {"wer": wer}


# load dataset from disk: data_dir
dataset = load_from_disk(data_dir)
logger.debug(dataset)

# split the dataset into train and test
train_test = dataset["train"].train_test_split(test_size=0.05)
dataset = DatasetDict({"train": train_test["train"], "test": train_test["test"]})

data_collator = DataCollatorSpeechSeq2SeqWithPadding(processor=processor)
metric = evaluate.load("wer")

training_args = Seq2SeqTrainingArguments(
	output_dir=output_dir,  # change to a repo name of your choice
	per_device_train_batch_size=args.per_device_train_batch_size,
	gradient_accumulation_steps=args.gradient_accumulation_steps,
	learning_rate=args.learning_rate,
	warmup_steps=args.warmup_steps,
	max_steps=args.max_steps,
	fp16=args.fp16,
	evaluation_strategy=args.evaluation_strategy,
	per_device_eval_batch_size=args.per_device_eval_batch_size,
	predict_with_generate=args.predict_with_generate,
	generation_max_length=args.generation_max_length,
	save_steps=args.save_steps,
	eval_steps=args.eval_steps,
	logging_steps=args.logging_steps,
	report_to=["tensorboard"],
	load_best_model_at_end=False,
	metric_for_best_model="wer",
	greater_is_better=False,
	push_to_hub=False,
	dataloader_num_workers=num_cores,
)


trainer = Seq2SeqTrainer(
	args=training_args,
	model=model,
	train_dataset=dataset["train"],
	eval_dataset=dataset["test"],
	data_collator=data_collator,
	# compute_metrics=compute_metrics,  # noqa: ERA001
	tokenizer=processor.feature_extractor,
)

processor.save_pretrained(training_args.output_dir)
trainer.train()
