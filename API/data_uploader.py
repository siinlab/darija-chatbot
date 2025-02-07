"""Module for pushing API's data in storage."""

import queue
import sys
import threading
from datetime import datetime, timezone
from os import environ
from pathlib import Path

import requests
from lgg import logger

# define variable to choose whether to collect data or not
COLLECT_DATA = True

if COLLECT_DATA:
	logger.info("Data collection is enabled.")
else:
	logger.info("Data collection is disabled.")

# get the storage URL and API key from the environment
STORAGE_URL = environ.get("STORAGE_URL", None)
STORAGE_API_KEY = environ.get("STORAGE_API_KEY", None)

if STORAGE_URL is None and COLLECT_DATA:
	logger.error("STORAGE_URL environment variable is not set. Exiting...")
	sys.exit(1)
if STORAGE_API_KEY is None and COLLECT_DATA:
	logger.error("STORAGE_API_KEY environment variable is not set. Exiting...")
	sys.exit(1)

# Initialize a global queue for files to be uploaded
_upload_queue = queue.Queue()

# Start the background worker thread for uploads
_worker_thread = None


def enqueue_file_upload(file_path: Path) -> None:
	"""Add a file path to the upload queue.

	Warns:
		The file will be deleted after uploading.

	Args:
		file_path (Path): The path to the file to be uploaded.
	"""
	if not COLLECT_DATA:
		logger.info("Data collection is disabled. Deleting file...")
		# delete the file_path
		file_path.unlink()
		return
	global _worker_thread  # noqa: PLW0603
	if _worker_thread is None:
		_worker_thread = threading.Thread(target=_upload_worker, daemon=True)
		_worker_thread.start()
	_upload_queue.put(file_path)


def _upload_worker() -> None:
	"""Worker that continuously processes file uploads from the queue."""
	logger.info("Upload worker started.")
	while True:
		logger.info("Waiting for file to upload...")
		file_path = _upload_queue.get()
		if file_path is None:  # option to exit worker
			break
		_upload_file(file_path)
		_upload_queue.task_done()
	logger.info("Upload worker stopped.")


def _get_current_time() -> str:
	"""Get the current time in a human-readable format.

	Returns:
		str: The current time in a human-readable format.
	"""
	return datetime.now(timezone.utc).strftime("%Y-%m-%d_%H")


def _upload_file(file_path: Path) -> None:
	"""Upload a file to storage.

	Args:
		file_path (str): The path to the file to upload.
	"""
	logger.info(f"Uploading file: {file_path}")
	try:
		# check if the file exists
		if not file_path.exists():
			logger.error(f"File {file_path} does not exist.")
			return
		# extract the file name from the file path
		remote_file_name = file_path.name
		# define the remote file path
		remote_file_path = f"{_get_current_time()}/{remote_file_name}"
		# build the target URL
		url = f"{STORAGE_URL}/{remote_file_path}"

		headers = {
			"AccessKey": STORAGE_API_KEY,
			"Content-Type": "application/octet-stream",
			"accept": "application/json",
		}

		with file_path.open("rb") as file_data:
			response = requests.put(url, headers=headers, data=file_data, timeout=5)
			response.raise_for_status()
		logger.info(f"File uploaded successfully to {url}")
	except Exception as e:  # noqa: BLE001
		logger.error(f"Failed to upload file to storage due to: {e}")
	finally:
		# delete the file_path
		file_path.unlink()
