"""This module takes care of training a tokenizer using sentencepiece."""

import argparse
from pathlib import Path

import pandas as pd
import sentencepiece as spm
from lgg import logger

logger.setLevel("INFO")


def train_tokenizer(corpus_path: str, model_prefix: str, vocab_size: int) -> None:
    """Train a tokenizer using sentencepiece.

    Args:
        corpus_path (str): Path to the corpus file.
        model_prefix (str): Prefix for the model files.
        vocab_size (int): Size of the vocabulary.
    """
    logger.info(f"Training tokenizer with vocab_size={vocab_size}")
    spm.SentencePieceTrainer.train(
        input=corpus_path,
        model_prefix=model_prefix,
        vocab_size=vocab_size,
    )
    logger.info("Tokenizer training completed. Tokenizer model saved.")

parser = argparse.ArgumentParser(
    description="Train a tokenizer using sentencepiece.")
parser.add_argument("--csv_path", type=str, required=True,
                    help="Path to the corpus file")
parser.add_argument("--model_prefix", type=str, required=True,
                    help="Prefix for the model files")
parser.add_argument("--vocab_size", type=int, required=True,
                    help="Size of the vocabulary")

args = parser.parse_args()

csv_path = args.csv_path
model_prefix = args.model_prefix
vocab_size = args.vocab_size

# check if the corpus file exists
if not Path(csv_path).exists():
    msg = f"Invalid path: {csv_path}"
    raise FileNotFoundError(msg)

# Read captions from TSV file and write to a text file
corpus_path = Path("/tmp/corpus.txt")  # noqa: S108
with corpus_path.open("w") as f:
    try:
        dataframe = pd.read_csv(csv_path)
    except pd.errors.ParserError:
        dataframe = pd.read_csv(csv_path, sep=";")
    for caption in dataframe["caption"]:
        f.write(caption + "\n")

# train the tokenizer
train_tokenizer(corpus_path, model_prefix, vocab_size)

# print runtime arguments
logger.info(f"corpus_path: {corpus_path}")
logger.info(f"model_prefix: {model_prefix}")
logger.info(f"vocab_size: {vocab_size}")

