"""This module takes care of computing speaker embedding for each audio."""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import torchaudio
from lgg import logger
from speechbrain.inference.speaker import EncoderClassifier
from tqdm import tqdm

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

# ensure tsv file exists
tsv_file = Path(tsv_file)
if not tsv_file.exists():
    msg = f"Invalid path: {tsv_file}"
    raise FileNotFoundError(msg)

# create the output directory if it does not exist
output_dir = Path(output_dir)
output_dir.mkdir(parents=True, exist_ok=True)

# load the tsv file: audio_path, caption without header
tsv = pd.read_csv(tsv_file, sep="\t")
audio_paths = tsv.iloc[:, 0]

# load the speaker encoder
classifier = EncoderClassifier.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb", run_opts={"device":"cuda"})

# compute speaker embedding for each audio and save them
embedding_paths = []
for path in tqdm(audio_paths):
    # load audio
    signal, fs =torchaudio.load(path)
    # compute speaker embedding
    embeddings = classifier.encode_batch(signal)
    # save the speaker embedding as numpy file
    filename = Path(path).stem
    output_path = output_dir / f"{filename}.npy"
    embeddings = embeddings.cpu().numpy()
    with output_path.open("wb") as file:
        np.save(file, embeddings)
    embedding_paths.append(output_path.resolve().as_posix())

# add embedding paths to the tsv file
tsv["embedding_path"] = embedding_paths
tsv.to_csv(tsv_file, sep="\t", index=False, header=False)
logger.info(f"Speaker embeddings saved in {output_dir}.")
logger.info(f"Updated tsv file saved in {tsv_file}.")
