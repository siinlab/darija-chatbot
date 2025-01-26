"""This module contains the main entry point for the Darija TTS API."""

from os import environ
from pathlib import Path

from fastapi import FastAPI

# import routers from model's API directories
from models.whisper_asr.API.main import router as whisper_asr_router

root_dir = Path(__file__).resolve().parent

# Define paths
environ["PATH"] = environ["PATH"] + ":" + root_dir.as_posix()
print(environ["PATH"])  # noqa: T201


app = FastAPI("Darija TTS API")

# include routers in the app
app.include_router(whisper_asr_router, tags=["Whisper ASR"])
