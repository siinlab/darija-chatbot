"""Middleware to log input-output pairs of requests."""

import json
import tempfile
from collections.abc import Awaitable, Callable
from datetime import datetime, timezone
from pathlib import Path

from data_uploader import enqueue_file_upload
from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

_temp = Path(tempfile.gettempdir())
_temp.mkdir(parents=True, exist_ok=True)


def get_new_file_path(extension: str = "") -> str:
	"""Get a new file path in the temporary directory."""
	file_name = datetime.now(timezone.utc).strftime("%H:%M:%S:%f") + extension
	return _temp / file_name


async def handle_incoming_request(
	path: str,
	request: Request,
	file_path: Path,
	cached_body: bytes,
) -> None:
	"""Handle incoming request logging."""
	if path in ["/generate", "/chat", "/embedding"]:
		body = json.loads(cached_body or b"{}")
		request_data = json.dumps(body, indent=4, ensure_ascii=False)
		_file_path = file_path.with_suffix(".request.json")
		with _file_path.open("w") as file:
			file.write(request_data)
		enqueue_file_upload(_file_path)

	if path == "/transcribe":
		form = await request.form()
		for file_key in form:
			for uploaded_file in form.getlist(file_key):
				_file_path = file_path.with_suffix(".request.wav")
				with _file_path.open("wb") as file:
					file.write(await uploaded_file.read())
				enqueue_file_upload(_file_path)


async def handle_outgoing_response(
	path: str,
	response: Response,
	file_path: Path,
) -> Response:
	"""Handle outgoing response logging."""
	if response.status_code != status.HTTP_200_OK:
		return response

	if path in ["/transcribe", "/chat"]:
		chunks = [chunk async for chunk in response.body_iterator]
		body = b"".join(chunks)
		content = body.decode("utf-8", errors="replace")
		_file_path = file_path.with_suffix(".response.txt")
		with _file_path.open("w") as file:
			file.write(content)
		enqueue_file_upload(_file_path)
		return Response(
			content=body,
			status_code=response.status_code,
			headers=dict(response.headers),
			media_type=response.media_type,
		)

	if path == "/generate":
		chunks = [chunk async for chunk in response.body_iterator]
		body = b"".join(chunks)
		_file_path = file_path.with_suffix(".response.wav")
		with _file_path.open("wb") as file:
			file.write(body)
		enqueue_file_upload(_file_path)
		return Response(
			content=body,
			status_code=response.status_code,
			headers=dict(response.headers),
			media_type=response.media_type,
		)

	return response


class LoggingMiddleware(BaseHTTPMiddleware):
	"""Middleware for logging incoming requests and outgoing responses."""

	async def dispatch(
		self,
		request: Request,
		call_next: Callable[[Request], Awaitable[Response]],
	) -> Response:
		"""Receive the request, log incoming data, pass to the next handler, then log outgoing response."""  # noqa: E501
		file_path = get_new_file_path()
		cached_body = await request.body()

		async def receive() -> dict:
			return {"type": "http.request", "body": cached_body, "more_body": False}

		request = Request(request.scope, receive)
		path = request.url.path

		await handle_incoming_request(path, request, file_path, cached_body)
		response = await call_next(request)
		return await handle_outgoing_response(path, response, file_path)
