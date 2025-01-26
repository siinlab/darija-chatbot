"""Utility functions for the API."""

import os
from pathlib import Path
from sys import path

_here = Path(__file__).resolve().parent


def append_to_sys_path() -> None:
	"""Appends specific directories to the system path based on the provided flags."""
	models_path = (_here.parent / "tts-arabic-pytorch").as_posix()
	path.insert(0, models_path)
	os.chdir(models_path)
