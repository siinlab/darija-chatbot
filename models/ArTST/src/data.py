"""This module takes care of preparing the data for the model training."""

import argparse
from pathlib import Path

import pandas as pd

parser = argparse.ArgumentParser(
    description="Prepare data for the model training.")
parser.add_argument("--csv_path", type=str, required=True,
                    help="Path to the csv file containing the data")
parser.add_argument("--audios_dir", type=str, required=True,
                    help="Path to the directory containing the audio files")
parser.add_argument("--manifest_path", type=str, required=True,
                    help="Path to the manifest file")
args = parser.parse_args()

csv_path = args.csv_path
audios_dir = args.audios_dir
manifest_path = args.manifest_path

# check if all paths are valid
if not Path(csv_path).exists():
	msg = f"Invalid path: {csv_path}"
	raise FileNotFoundError(msg)
if not Path(audios_dir).exists():
    msg = f"Invalid path: {audios_dir}"
    raise FileNotFoundError(msg)

# create a directory for the manifest file
Path(manifest_path).parent.mkdir(parents=True, exist_ok=True)

# read the csv file
dataframe = pd.read_csv(csv_path)
columns = ["audio", "caption"]

# ensure that the dataframe has the required columns
if not all(col in dataframe.columns for col in columns):
    msg = f"Columns {columns} not found in the csv file"
    raise ValueError(msg)

# check if all audio files exist
for audio in dataframe["audio"]:
    audio_path = Path(audios_dir) / audio
    if not audio_path.exists():
        msg = f"Invalid path: {audio_path}"
        raise FileNotFoundError(msg)

# create tsv file where audio contains absolute paths
dataframe["audio"] = dataframe["audio"].apply(lambda x: str(Path(audios_dir) / x ))
dataframe.to_csv(manifest_path, sep="\t", index=False, header=False)
