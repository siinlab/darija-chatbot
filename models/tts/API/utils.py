"""Utility functions for the API."""

from pathlib import Path
from sys import path

_here = Path(__file__).resolve().parent


def append_to_sys_path() -> None:
	"""Appends specific directories to the system path based on the provided flags.

	Returns:
		None
	"""
	models_path = (_here.parent / "tts-arabic-pytorch").as_posix()
	path.insert(0, models_path)
