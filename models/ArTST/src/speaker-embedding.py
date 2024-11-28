"""This module takes care of computing speaker embedding for each audio."""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import torchaudio
from lgg import logger
from speechbrain.inference.speaker import EncoderClassifier
from tqdm import tqdm

# Parse arguments
parser = argparse.ArgumentParser(description="Compute speaker embedding for audios.")
parser.add_argument(
    "--tsv_file",
    type=str,
    help="The path to the tsv file containing the audio paths.",
    required=True,
)
parser.add_argument(
    "--output_dir",
    type=str,
    help="The path where the speaker embeddings will be saved.",
    required=True,
)
args = parser.parse_args()
tsv_file = args.tsv_file
output_dir = args.output_dir

# Ensure TSV file exists
tsv_file = Path(tsv_file)
if not tsv_file.exists():
    msg = f"Invalid path: {tsv_file}"
    raise FileNotFoundError(msg)

# Create the output directory if it does not exist
output_dir = Path(output_dir)
output_dir.mkdir(parents=True, exist_ok=True)

# Load the TSV file
tsv = pd.read_csv(tsv_file, sep="\t", header=None, names=["audio_path", "duration"])

# Extract the root directory from the first line and remove it from the data
root_dir = Path(tsv.iloc[0, 0])
tsv = tsv.iloc[1:].reset_index(drop=True)  # Remove the first line and reset index

# change duration column type to int
tsv["duration"] = tsv["duration"].astype(int)

# Resolve full audio paths using the root directory
audio_paths = tsv["audio_path"].apply(lambda x: str(root_dir / x))

# Load the speaker encoder
classifier = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb", run_opts={"device": "cuda"},
)

# Compute speaker embedding for each audio and save them
embedding_paths = []
for path in tqdm(audio_paths):
    # Load audio
    signal, fs = torchaudio.load(path)

    # Compute speaker embedding
    embeddings = classifier.encode_batch(signal)

    # Save the speaker embedding as a numpy file
    filename = Path(path).stem
    output_path = output_dir / f"{filename}.npy"
    embeddings = embeddings.cpu().numpy()
    with output_path.open("wb") as file:
        np.save(file, embeddings)

    embedding_paths.append(output_path.resolve().as_posix())

# Add embedding paths to the TSV file
tsv["embedding_path"] = embedding_paths

# Add the root directory to the audio paths
tsv["audio_path"] = audio_paths

# Add root directory to the first line of the TSV file
tsv = pd.concat([pd.DataFrame([["/", None, None]], columns=tsv.columns), tsv])

# Save the updated TSV file
tsv.to_csv(tsv_file, sep="\t", index=False, header=False)

# Log completion
logger.info(f"Speaker embeddings saved in {output_dir}.")
logger.info(f"Updated TSV file saved in {tsv_file}.")
