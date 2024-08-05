"""This module is used to run the EDA module from the command line."""

import argparse
from pathlib import Path
from sys import exit

import pandas as pd
from lgg import logger
from plot import Plotter
from text.analysis import (
	alphabets_number,
	arabic_words_number,
	characters_distribution,
	characters_number,
	digit_words_number,
	digits_number,
	latin_words_number,
	paragraphs_length_distribution,
	punctuation_words_number,
	punctuations_number,
	sentences_length_distribution,
	symbols_number,
    white_spaces_number,
	words_distribution,
	words_length_distribution,
	words_number,
)

parser = argparse.ArgumentParser(description="Run the EDA module.")
parser.add_argument(
	"--data",
	type=str,
	help="The path to the data folder.",
	required=True,
)
parser.add_argument(
	"--run-dir",
	type=str,
	help="The path where the logs and plots will be saved.",
	default="."
)
args = parser.parse_args()
data = args.data
run_dir = args.run_dir
run_dir = Path(run_dir)
if run_dir.exists():
    run_dir.rmdir()
run_dir.mkdir(parents=True)

# Read the csv file in the data folder
csv_files = list(Path(data).glob("*.csv"))
if len(csv_files) == 0:
	logger.error(f"No csv files found in {data}.")
	exit(1)
elif len(csv_files) > 1:
	logger.warning(f"Multiple csv files found in {data}.")
csv_file = csv_files[0]

captions = None
try:
	dataframe = pd.read_csv(csv_file)
	captions_column = dataframe.columns[0]
	captions = dataframe[captions_column].tolist()
	logger.debug(f"Read {len(captions)} captions from {csv_file}.")
	logger.debug(f"First caption: {captions[0]}")
	captions = "\n".join(captions)
except Exception as e:  # noqa: BLE001
	logger.error(f"Error reading the csv file: {e}")
	exit(1)

# Compute character-level numbers
n_chars = characters_number(captions)
n_white_spaces = white_spaces_number(captions)
n_punctuation = punctuations_number(captions)
n_alphabets = alphabets_number(captions)
n_digits = digits_number(captions)
n_symbols = symbols_number(captions)
logger.info(f"{n_chars=}")
logger.info(f"{n_white_spaces=}")
logger.info(f"{n_punctuation=}")
logger.info(f"{n_alphabets=}")
logger.info(f"{n_digits=}")
logger.info(f"{n_symbols=}")

# Compute word-level numbers
n_words = words_number(captions)
n_arabic_words = arabic_words_number(captions)
n_latin_words = latin_words_number(captions)
n_digit_words = digit_words_number(captions)
n_punctuation_word = punctuation_words_number(captions)
logger.info(f"{n_words=}")
logger.info(f"{n_arabic_words=}")
logger.info(f"{n_latin_words=}")
logger.info(f"{n_digit_words=}")
logger.info(f"{n_punctuation_word=}")

# Compute distributions
chars_hist = characters_distribution(captions)
words_hist = words_distribution(captions)
words_length_hist = words_length_distribution(captions)
sentences_length_hist = sentences_length_distribution(captions)
paragraphs_length_hist = paragraphs_length_distribution(captions)

# Print number of unique characters and words
logger.info(f"Number of unique characters: {len(chars_hist)}")
logger.info(f"Number of unique words: {len(words_hist)}")
logger.info(f"Number of paragraphs: {sum(paragraphs_length_hist.values())}")

# Log the results
topk = 30
plotter = Plotter(run_dir)
plotter.histogram(chars_hist, filename="characters-frequency", k=topk)
plotter.histogram(chars_hist, filename="characters-frequency", k=topk, top=False)

plotter.histogram(words_hist, filename="words-frequency", k=topk)
plotter.histogram(words_hist, filename="words-frequency", k=topk, top=False)

plotter.histogram(words_length_hist, filename="words-length-frequency", k=topk)
plotter.histogram(words_length_hist, filename="words-length-frequency", k=topk,
                  top=False)

plotter.histogram(sentences_length_hist, filename="sentences-length-frequency", k=topk)
plotter.histogram(
	sentences_length_hist, filename="sentences-length-frequency", k=topk, top=False,
)

plotter.histogram(paragraphs_length_hist, filename="paragraphs-length-frequency",
                  k=topk)
plotter.histogram(
	paragraphs_length_hist, filename="paragraphs-length-frequency", k=topk, top=False,
)
