"""This module contains the main entry point for the Darija TTS API."""

from fastapi import FastAPI

from .utils import append_sys_path

append_sys_path(whisper_asr=True)

# import routers from model's API directories
from API.main import router as whisper_asr_router  # noqa: E402

app = FastAPI()

# include routers in the app
app.include_router(whisper_asr_router, tags=["Whisper ASR"])
