"""Module to merge TTS datasets.

Usage:
    python merge-datasets.py --datasets <dataset1> <dataset2> --output <output>
"""

import argparse
import shutil
from pathlib import Path

import pandas as pd
from lgg import logger
from tqdm import tqdm

parser = argparse.ArgumentParser(description="Merge TTS datasets.")
parser.add_argument(
	"--datasets",
	type=str,
	nargs="+",
	help="List of datasets to merge.",
	required=True,
)
parser.add_argument("--output", type=str, help="Output directory.", required=True)
args = parser.parse_args()

datasets = args.datasets
output = args.output

# Create output directory if it does not exist
if Path(output).exists():
	shutil.rmtree(output)
Path(output).mkdir(parents=True, exist_ok=True)

# Check that all dataset folders contain a csv file and an audios folder
for dataset in datasets:
	if not Path(dataset).is_dir():
		msg = f"Dataset {dataset} not found."
		raise FileNotFoundError(msg)
	csv_files = list(Path(dataset).glob("*.csv"))
	if len(csv_files) != 1:
		logger.debug(csv_files)
		msg = f"Dataset {dataset} must contain exactly one csv file."
		raise ValueError(msg)
	audios_dir = Path(dataset) / "audios"
	if not audios_dir.is_dir():
		msg = f"Dataset {dataset} must contain an audios folder."
		raise FileNotFoundError(msg)

# Create audios directory in output folder
out_audios_dir = Path(output) / "audios"
out_audios_dir.mkdir(parents=True, exist_ok=True)

# Merge datasets
merged_data = []
for dataset in datasets:
	csv_file = next(iter(Path(dataset).rglob("*.csv")))
	audios_dir = Path(dataset) / "audios"
	dataset_name = Path(dataset).name
	# Read csv file using pandas
	try:
		csv = pd.read_csv(csv_file)
	except Exception:  # noqa: BLE001
		csv = pd.read_csv(csv_file, delimiter=";")
	# Drop rows with missing values
	csv = csv.dropna()
	# Iterate over rows in csv file
	for _i, row in tqdm(csv.iterrows(), desc=f"Merging {dataset_name}"):
		audio_name = row["audio"]
		new_audio_name = f"{dataset_name}_{audio_name}"
		caption = row["caption"]
		# Copy audio file to output directory
		audio_file = audios_dir / audio_name
		out_audio_file = out_audios_dir / new_audio_name
		shutil.copy(audio_file, out_audio_file)
		# add row to merged data
		merged_data.append({"audio": new_audio_name, "caption": caption})

# Save merged data to csv file
merged_csv = pd.DataFrame(merged_data)
merged_csv.to_csv(Path(output) / "data.csv", index=False)

logger.info(f"Datasets merged successfully in {output}.")
