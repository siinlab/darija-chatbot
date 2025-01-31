"""Middleware to log input-output pairs of requests."""

import time

from data_uploader import enqueue_file_upload  # noqa: F401
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):  # noqa: D101
	async def dispatch(self, request: Request, call_next):  # noqa: ANN001, ANN201, D102
		start_time = time.time()

		# Read request body
		request_body = await request.body()
		request_data = request_body.decode("utf-8") if request_body else None

		# Process request
		response = await call_next(request)

		# Read response body
		response_body = b"".join([chunk async for chunk in response.body_iterator])
		response_data = response_body.decode("utf-8") if response_body else None

		# Logging input-output pair
		log_entry = {  # noqa: F841
			"path": request.url.path,
			"method": request.method,
			"request": request_data,
			"response": response_data,
			"status_code": response.status_code,
			"latency": time.time() - start_time,
		}

		# Return original response
		response.body_iterator = iter([response_body])
		return response
