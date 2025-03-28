"""This module contains the main entry point for the Darija TTS API."""

from fastapi import FastAPI
from util import append_to_sys_path

append_to_sys_path()

# import routers from model's API directories
from chat.API.main import router as chat_router  # noqa: E402
from embedding.API.main import router as embedding_router  # noqa: E402
from tts.API.main import router as tts_asr_router  # noqa: E402
from whisper_asr.API.main import router as whisper_asr_router  # noqa: E402

app = FastAPI()

# include routers in the app
app.include_router(whisper_asr_router, tags=["Darija ASR"])
app.include_router(tts_asr_router, tags=["Darija TTS"])
app.include_router(chat_router, tags=["Darija Chat"])
app.include_router(embedding_router, tags=["Text Embedding"])
