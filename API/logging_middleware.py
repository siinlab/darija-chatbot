"""Middleware to log input-output pairs of requests."""

from pathlib import Path

from data_uploader import enqueue_file_upload
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):  # noqa: D101
	async def dispatch(self, request: Request, call_next):  # noqa: ANN001, ANN201, D102
		# Process request
		response = await call_next(request)

		path = Path(__file__).parent.resolve() / "logs.json"
		with path.open("w") as file:
			file.write("{'A': [1]}")
		enqueue_file_upload(path)

		return response
