"""This module takes care of computing speaker embedding for each audio."""

import argparse
from pathlib import Path

import pandas as pd
import torch
import torchaudio
from speechbrain.inference.speaker import EncoderClassifier
from tqdm import tqdm


def compute_speaker_embedding(audio_path: str)->torch.Tensor:
    """Compute the speaker embedding for the given audio.

    Args:
        audio_path (str): The path to the audio file.

    Returns:
        torch.Tensor: The speaker embedding.
    """
    classifier = EncoderClassifier.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb", run_opts={"device":"cuda"})
    signal, fs =torchaudio.load(audio_path)
    return classifier.encode_batch(signal)


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
audios_dir = args.audios_dir
output_dir = args.output_dir

# ensure tsv file exists
tsv_file = Path(args.tsv_file)
if not tsv_file.exists():
    msg = f"Invalid path: {tsv_file}"
    raise FileNotFoundError(msg)

# create the output directory if it does not exist
output_dir = Path(output_dir)
output_dir.mkdir(parents=True, exist_ok=True)

# load the tsv file: audio_path, caption
tsv = pd.read_csv(tsv_file, sep="\t")
audio_paths = tsv["audio_path"].tolist()

# compute speaker embedding for each audio
for audio_path in tqdm(audio_paths):
    # compute the speaker embedding
    speaker_embedding = compute_speaker_embedding(audio_path)
    # save the speaker embedding
    output_path = output_dir / Path(audio_path).stem
    speaker_embedding.save(output_path)
