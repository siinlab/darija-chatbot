"""This module runs the data filtering module.
It processes insights.csv files in the specified runs directory,
filters the data based on predefined criteria, and saves the filtered data.
"""  # noqa: D205

import argparse
import sys
from pathlib import Path

import pandas as pd
from criteria import CRITERIA
from lgg import logger

logger.setLevel("INFO")

parser = argparse.ArgumentParser(description="Run the EDA module.")
parser.add_argument(
	"--runs_dir",
	type=str,
	help="The path to the runs folder.",
	required=True,
)
args = parser.parse_args()
runs_dir = Path(args.runs_dir)

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
	logger.info(f"Processing {insight}...")
	# Load the insights.csv file
	dataframe = pd.read_csv(insight)
	logger.info(f"Loaded {len(dataframe)} rows from {insight}.")

	# filter the data based on the criteria
	for key, value in CRITERIA.items():
		if key not in dataframe.columns:
			continue
		min_value = value.get("min", None)
		max_value = value.get("max", None)
		logger.debug(f"Filtering {key} between {min_value} and {max_value}...")
		if min_value is not None:
			dataframe = dataframe[dataframe[key] >= min_value]
		if max_value is not None:
			dataframe = dataframe[dataframe[key] <= max_value]
		logger.debug(f"Remaining rows: {len(dataframe)}.")
	logger.info(f"Filtered data: {len(dataframe)} remaining rows.")

	# save the filtered data
	filtered_path = insight.parent / "filtered.csv"
	dataframe.to_csv(filtered_path, index=False)
	logger.info(f"Saved filtered data to {filtered_path}.")
