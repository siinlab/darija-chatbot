"""This module is used to compute the duration of silence in the audio."""

import librosa
import numpy as np
import statsmodels.api as sm
from joblib import Parallel, delayed

from eda.utils import time_execution


def _compute_silence_proportion(audio_path: str) -> tuple[float, float]:
	"""Compute the duration of silence in the audio file.

	Args:
		audio_path (str): Path to the audio file.

	Returns:
		tuple[float, float]: Percentage of silence and total duration.
	"""
	y, sr = librosa.load(audio_path)
	if np.max(y) < 0.01:  # noqa: PLR2004
		return 100.0, librosa.get_duration(y=y, sr=sr)
	total_duration = librosa.get_duration(y=y, sr=sr)
	non_silent_segments = librosa.effects.split(y, top_db=40)
	non_silence_proportion = 0.0
	for start, end in non_silent_segments:
		non_silence_proportion += (end - start) / sr
	return (1 - non_silence_proportion / total_duration) * 100, total_duration


def _analyze_amplitude_trend(audio_path: str) -> tuple[float, float]:
	"""Analyze the amplitude trend of the audio file.

	Args:
		audio_path (str): Path to the audio file.

	Returns:
		tuple[float, float]: Bias and slope of the amplitude trend.
	"""
	# Load audio
	y, _ = librosa.load(audio_path)

	# Calculate amplitude envelope
	amplitude_envelope = np.abs(y)

	# get audio mean
	mean = np.mean(amplitude_envelope)

	# get audio max amplitude
	max_amplitude = np.max(amplitude_envelope)

	# Analyze trend
	x = np.arange(len(amplitude_envelope)).reshape(-1, 1)
	x = sm.add_constant(x)
	model = sm.OLS(amplitude_envelope, x).fit()
	slope = model.params[1] / (max_amplitude + 1e-9)
	bias = model.params[0]
	return bias, slope, mean


# Signal-to-Noise Ratio (SNR)
def _snr(y: np.ndarray, y_noise: np.ndarray) -> float:
	"""Calculate the Signal-to-Noise Ratio (SNR).

	Args:
		y (np.ndarray): Original audio signal.
		y_noise (np.ndarray): Noisy audio signal.

	Returns:
		float: The SNR value in decibels.
	"""
	return 10 * np.log10(np.mean(y**2) / (np.mean((y - y_noise) ** 2) + 1e-9) + 1e-9)


def _compute_snr_ratio(audio_path: str) -> float:
	"""Compute the Signal-to-Noise Ratio (SNR) ratio of the audio file.

	Args:
		audio_path (str): Path to the audio file.

	Returns:
		float: SNR ratio in decibels.
	"""
	y, sr = librosa.load(audio_path)
	rng = np.random.default_rng()
	y_noise = y + rng.normal(0, 0.1, len(y))  # Add some random noise
	return _snr(y, y_noise)


@time_execution
def compute_silence_proportions(audio_paths: list[str]) -> list[tuple[float, float]]:
	"""Compute silence proportions for a list of audio files.

	Args:
		audio_paths (list[str]): List of paths to audio files.

	Returns:
		list[tuple[float, float]]: List of tuples containing silence percentage and total duration.
	"""  # noqa: E501
	return Parallel(n_jobs=8, backend="multiprocessing")(
		delayed(_compute_silence_proportion)(path) for path in audio_paths
	)


@time_execution
def analyze_amplitude_trend(audio_paths: list[str]) -> list[tuple[float, float]]:
	"""Analyze amplitude trends for a list of audio files.

	Args:
		audio_paths (list[str]): List of paths to audio files.

	Returns:
		list[tuple[float, float]]: List of tuples containing bias and slope.
	"""
	return Parallel(n_jobs=8, backend="multiprocessing")(
		delayed(_analyze_amplitude_trend)(path) for path in audio_paths
	)


@time_execution
def compute_snr_ratio(audio_paths: list[str]) -> list[float]:
	"""Compute SNR ratios for a list of audio files.

	Args:
		audio_paths (list[str]): List of paths to audio files.

	Returns:
		list[float]: List of SNR ratios.
	"""
	return Parallel(n_jobs=8, backend="multiprocessing")(
		delayed(_compute_snr_ratio)(path) for path in audio_paths
	)
