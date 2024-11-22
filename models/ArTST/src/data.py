"""This module takes care of preparing the data for the model training."""

import argparse
from pathlib import Path

import pandas as pd
from lgg import logger

logger.setLevel("INFO")

parser = argparse.ArgumentParser(
    description="Prepare data for the model training.")
parser.add_argument("--csv_path", type=str, required=True,
                    help="Path to the csv file containing the data")
parser.add_argument("--audios_dir", type=str, required=True,
                    help="Path to the directory containing the audio files")
parser.add_argument("--manifest_path", type=str, required=True,
                    help="Path to the manifest file")
parser.add_argument("--transcription_path", type=str, required=False,
                    help="Path to the transcription file")
args = parser.parse_args()

csv_path = args.csv_path
audios_dir = args.audios_dir
manifest_path = args.manifest_path
transcription_path = args.transcription_path

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
Path(manifest_path).parent.mkdir(parents=True, exist_ok=True)
if transcription_path:
    Path(transcription_path).parent.mkdir(parents=True, exist_ok=True)

# print runtime arguments
logger.info(f"csv_path: {csv_path}")
logger.info(f"audios_dir: {audios_dir}")
logger.info(f"manifest_path: {manifest_path}")
logger.info(f"transcription_path: {transcription_path}")

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

# check if transcription file is provided
if transcription_path:
    # save captions to a transcription file
    captions = dataframe["caption"].tolist()
    with Path(transcription_path).open("w") as f:
        f.write("\n".join(captions))

# create tsv file where audio contains absolute paths
dataframe["audio"] = dataframe["audio"].apply(lambda x: str(Path(audios_dir) / x ))
dataframe.to_csv(manifest_path, sep="\t", index=False, header=False)

# print the number of rows in the manifest file
logger.info(f"Number of rows in the manifest file: {len(dataframe)}")
