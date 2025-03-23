"""This module cleans up the transcription of audios.
It processes data.csv files in the specified runs directory,
filters the data based on predefined criteria, and saves the filtered data.
"""  # noqa: D205

import argparse
import sys
from pathlib import Path

import polars as pl
from digits_to_alphabets import transform_number_to_darija
from lgg import logger

logger.setLevel("INFO")

parser = argparse.ArgumentParser(description="Run the EDA module.")
parser.add_argument(
	"--runs_dir",
	type=Path,
	help="The path to the runs folder.",
	required=True,
)
args = parser.parse_args()
runs_dir = args.runs_dir

# ensure the runs directory exists
if not runs_dir.exists():
	logger.error(f"Directory {runs_dir} does not exist.")
	sys.exit(1)

# get all insights.csv files
insights = sorted(runs_dir.rglob("**/insights.csv"))
if len(insights) == 0:
	logger.error(f"No insights.csv files found in {runs_dir}.")
	sys.exit(1)

logger.info(f"Found {len(insights)} insights.csv files in {runs_dir}.")

# Iterate over all insights.csv files
for insight in insights:
	# Load the insights.csv file
	dataframe = pl.read_csv(insight)
	logger.info(f"Loaded {len(dataframe)} rows from {insight}.")

	new_dataframe = dataframe.with_columns(
		pl.col("caption")
		.map_elements(
			transform_number_to_darija,
			return_dtype=pl.Utf8,
		)  # Convert numbers
		.str.replace_all("%", " فالمية ")  # Replace "%" with " فالمية "
		.str.strip_chars()  # Trim leading/trailing spaces
		.str.replace_all(r"\s+", " "),  # Remove redundant spaces
	)

	# Find the row indices where the value changed
	changed_indices = dataframe.with_columns(
		pl.arange(0, dataframe.height).alias("row_id"),  # Add row indices
	).filter(new_dataframe["caption"] != dataframe["caption"])["row_id"]
	num_changed = changed_indices.shape[0]
	logger.info(f"{num_changed} rows have changed.")
	for index in changed_indices:
		old_value = dataframe["caption"][index]
		new_value = new_dataframe["caption"][index]
		logger.debug(
			f"row index: {index} \n- old value: {old_value} \n- new value: {new_value}",
		)

	# save the cleaned up data
	new_dataframe.write_csv(insight)
	logger.info(f"Saved cleaned up data to {insight}.")
