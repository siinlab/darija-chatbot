"""Denoise audio files using the DeepFilterNet model."""

from pathlib import Path

import torch
import torchaudio
from df import enhance, init_df
from df.enhance import load_audio, save_audio
from speechbrain.inference.enhancement import SpectralMaskEnhancement

_model, _df_state, _ = init_df()  # Load default model
_speech_model = SpectralMaskEnhancement.from_hparams(
	source="speechbrain/metricgan-plus-voicebank",
	savedir="pretrained_models/metricgan-plus-voicebank",
	run_opts={"device": "cuda"},
)


def denoise(audio_path: Path, output_path: Path) -> None:
	"""Denoise an audio file using the whisper model.

	Args:
		audio_path: Path to the input audio file
		output_path: Path to save the denoised audio file
	"""
	noisy_audio, _ = load_audio(audio_path, sr=_df_state.sr())

	enhanced_audio = enhance(_model, _df_state, noisy_audio)

	save_audio(output_path, enhanced_audio, _df_state.sr())


def enhance_speech(audio_path: Path, output_path: Path) -> None:
	"""Enhance speech in an audio file using the whisper model.

	Args:
		audio_path: Path to the input audio file
		output_path: Path to save the enhanced audio file
	"""
	# Load and add fake batch dimension
	noisy = _speech_model.load_audio(
		audio_path.as_posix(),
	).unsqueeze(0)

	# Add relative length tensor
	enhanced = _speech_model.enhance_batch(noisy, lengths=torch.tensor([1.0]))

	# Saving enhanced signal on disk
	torchaudio.save(output_path, enhanced.cpu(), 16000)
