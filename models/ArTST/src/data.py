"""This module takes care of preparing the data for the model training."""

import argparse
from pathlib import Path

import pandas as pd
from lgg import logger
import soundfile

logger.setLevel("INFO")

parser = argparse.ArgumentParser(
    description="Prepare data for the model training.")
parser.add_argument("--csv_path", type=str, required=True,
                    help="Path to the csv file containing the data")
parser.add_argument("--audios_dir", type=str, required=True,
                    help="Path to the directory containing the audio files")
parser.add_argument("--train_path", type=str, required=True,
                    help="Path to the train csv file")
parser.add_argument("--valid_path", type=str, required=True,
                    help="Path to the validation csv file")
parser.add_argument("--val_size", type=float, required=True,
help="The size of the validation set as a fraction of "
    "the total number of transcriptions.",
)
args = parser.parse_args()

csv_path = args.csv_path
audios_dir = args.audios_dir
train_path = args.train_path
valid_path = args.valid_path
val_size = args.val_size

# check if all paths are valid
if not Path(csv_path).exists():
	msg = f"Invalid path: {csv_path}"
	raise FileNotFoundError(msg)
if not Path(audios_dir).exists():
    msg = f"Invalid path: {audios_dir}"
    raise FileNotFoundError(msg)

# Ensure that audios_dir is absolute path
audios_dir = Path(audios_dir).resolve()

# create a directory for the manifest file
Path(train_path).parent.mkdir(parents=True, exist_ok=True)
Path(valid_path).parent.mkdir(parents=True, exist_ok=True)

# print runtime arguments
logger.info(f"csv_path: {csv_path}")
logger.info(f"audios_dir: {audios_dir}")
logger.info(f"train_path: {train_path}")
logger.info(f"valid_path: {valid_path}")
logger.info(f"val_size: {val_size}")

# read the csv file
try:
    dataframe = pd.read_csv(csv_path)
except pd.errors.ParserError:
    dataframe = pd.read_csv(csv_path, sep=";")
columns = ["audio", "caption"]

# ensure that the dataframe has the required columns
if not all(col in dataframe.columns for col in columns):
    msg = f"Columns {columns} not found in the csv file"
    raise ValueError(msg)
dataframe = dataframe[columns]

# Drop rows with missing values
logger.info(f"Number of rows before dropping missing values: {len(dataframe)}")
dataframe = dataframe.dropna(subset=columns)
logger.info(f"Number of rows after dropping missing values: {len(dataframe)}")

# check if all audio files exist
for audio in dataframe["audio"]:
    audio_path = Path(audios_dir) / audio
    if not audio_path.exists():
        logger.warning(f"Missing audio file: {audio_path}. Removing the row.")
        dataframe = dataframe[dataframe["audio"] != audio]

# shuffle the dataframe
dataframe = dataframe.sample(frac=1).reset_index(drop=True)

# split the dataframe into train and validation sets
val_size = int(val_size * len(dataframe))
train_df = dataframe[val_size:]
valid_df = dataframe[:val_size]

# write the train and validation dataframes to files
for df, path in zip([train_df, valid_df], [train_path, valid_path], strict=False):
    df.to_csv(path, index=False)

# read captions from both train and validation dataframes
# and save them in separate text files
for df, path in zip([train_df, valid_df], [train_path, valid_path], strict=False):
    with path.with_suffix(".txt").open("w") as file:
        for caption in df["caption"]:
            file.write(caption + "\n")

# Create manifest file per split
# manifest contains audio path and number of frames
for df, path in zip([train_df, valid_df], [train_path, valid_path], strict=False):
    manifest = []
    for audio in df["audio"]:
        audio_path = Path(audios_dir) / audio
        frames = soundfile.info(audio_path).frames
        manifest.append(f"{audio_path}\t{frames}")
    # save manifest to tsv file
    with path.with_suffix(".tsv").open("w") as file:
        file.write("/\n")
        file.write("\n".join(manifest))

# print the number of rows in the manifest file
logger.info(f"Number of rows in the manifest file: {len(dataframe)}")
