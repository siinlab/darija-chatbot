"""This module splits transcription in the text file into train and val text files."""

import argparse
import random
from pathlib import Path

from lgg import logger

random.seed(42)

parser = argparse.ArgumentParser(
    description="Split text file into train and val text files.")
parser.add_argument(
    "--text_file",
    type=str,
    help="The path to the text file containing the transcriptions.",
    required=True,
)
parser.add_argument(
    "--train_file",
    type=str,
    help="The path where the train text file will be saved.",
    required=True,
)
parser.add_argument(
    "--val_file",
    type=str,
    help="The path where the val text file will be saved.",
    required=True,
)
parser.add_argument(
    "--val_size",
    type=float,
    help="The size of the validation set as a fraction of "
    "the total number of transcriptions.",
    required=True,
)
args = parser.parse_args()

# ensure text file exists
text_file = Path(args.text_file)
if not text_file.exists():
    msg = f"Invalid path: {text_file}"
    raise FileNotFoundError(msg)

# ensure val_size is between 0 and 1
val_size = args.val_size
if not 0 < val_size < 1:
    msg = f"Invalid value for val_size: {val_size}. It should be between 0 and 1."
    raise ValueError(msg)

# read the text file
with text_file.open() as file:
    lines = file.readlines()

# ensure there are transcriptions in the text file
if not lines:
    msg = f"Empty text file: {text_file}"
    raise ValueError(msg)
logger.info(f"Read {len(lines)} transcriptions from {text_file}")

# shuffle the transcriptions
random.shuffle(lines)

# split the transcriptions into train and val sets
val_size = int(val_size * len(lines))
logger.info(
    f"Splitting transcriptions into train and val sets with val size: {val_size}")
train_lines = lines[val_size:]
val_lines = lines[:val_size]

# write the train and val transcriptions to files
train_file = Path(args.train_file)
val_file = Path(args.val_file)
train_file.write_text("\n".join(train_lines))
val_file.write_text("\n".join(val_lines))
logger.info(f"Train transcriptions saved to {train_file}")
logger.info(f"Val transcriptions saved to {val_file}")
