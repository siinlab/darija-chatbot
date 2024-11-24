"""This module takes care of training a tokenizer using sentencepiece."""

import argparse
from pathlib import Path

import sentencepiece as spm
from lgg import logger

logger.setLevel("INFO")

# Define the function to train the tokenizer
def train_tokenizer(corpus_path: str, model_prefix: str, vocab_size: int,
                    character_coverage: float = 0.9995,
                    model_type: str = "unigram") -> None:
    """Train a tokenizer using sentencepiece.

    Args:
        corpus_path (str): Path to the corpus file.
        model_prefix (str): Prefix for the model files.
        vocab_size (int): Size of the vocabulary.
        character_coverage (float): Character coverage for the tokenizer.
        model_type (str): Type of the tokenizer model.
    """
    logger.info(f"Training tokenizer with vocab_size={vocab_size}")
    spm.SentencePieceTrainer.train(
        input=corpus_path,
        model_prefix=model_prefix,
        vocab_size=vocab_size,
        character_coverage=character_coverage,
        model_type=model_type,
    )
    logger.info("Tokenizer training completed. Tokenizer model saved.")

# Define the function to tokenize the text
def tokenize_text(text_path: str, model_prefix: str, output_path: str) -> None:
    """Tokenize the given text using the sentencepiece model.

    Args:
        text_path (str): Path to the text file.
        model_prefix (str): Prefix for the model files.
        output_path (str): Path to save the tokenized text.
    """
    sp = spm.SentencePieceProcessor()
    sp.load(model_prefix + ".model")

    # Read the text file and tokenize each line
    with Path(text_path).open() as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            tokens = sp.encode(line.strip(), out_type=str)
            lines[i] = " ".join(tokens)

    # Save the tokenized text
    with Path(output_path).open("w") as file:
        file.write("\n".join(lines))


parser = argparse.ArgumentParser(
    description="Train a tokenizer using sentencepiece.")
parser.add_argument("--corpus_path", type=str, required=True,
                    help="Path to the corpus file")
parser.add_argument("--output_text_path", type=str, required=True,
                    help="Path to save the tokenized text")
parser.add_argument("--model_prefix", type=str, required=True,
                    help="Prefix for the model files")
parser.add_argument("--vocab_size", type=int, default=4000,
                    help="Size of the vocabulary")
parser.add_argument("--character_coverage", type=float, default=0.9995,
                    help="Character coverage for the tokenizer")
parser.add_argument("--model_type", type=str, default="unigram",
                    help="Type of the tokenizer model")
args = parser.parse_args()

corpus_path = args.corpus_path
output_text_path = args.output_text_path
model_prefix = args.model_prefix
vocab_size = args.vocab_size

# check if the tsv file exists
if not Path(corpus_path).exists():
    msg = f"Invalid path: {corpus_path}"
    raise FileNotFoundError(msg)

# make the output directory
Path(output_text_path).parent.mkdir(parents=True, exist_ok=True)

# train the tokenizer
train_tokenizer(corpus_path, model_prefix, vocab_size, 
                args.character_coverage, args.model_type)

# tokenize the text
tokenize_text(corpus_path, model_prefix, output_text_path)

# print runtime arguments
logger.info(f"corpus_path: {corpus_path}")
logger.info(f"model_prefix: {model_prefix}")
logger.info(f"vocab_size: {vocab_size}")

