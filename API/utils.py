"""Utility functions for the API."""

from pathlib import Path
from sys import path

_here = Path(__file__).resolve().parent


def append_sys_path(*, whisper_asr: bool = False) -> None:
	"""Appends specific directories to the system path based on the provided flags.

	Args:
		whisper_asr (bool): If True, appends the path to the Whisper ASR model directory
		to the system path.

	Returns:
		None
	"""
	if whisper_asr:
		whisper_asr_path = (_here.parent / "models/whisper_asr").as_posix()
		path.insert(0, whisper_asr_path)
