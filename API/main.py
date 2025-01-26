"""This module contains the main entry point for the Darija TTS API."""

from fastapi import FastAPI

# import routers from model's API directories
from models.whisper_asr.API.main import router as whisper_asr_router

app = FastAPI("Darija TTS API")

# include routers in the app
app.include_router(whisper_asr_router, tags=["Whisper ASR"])
