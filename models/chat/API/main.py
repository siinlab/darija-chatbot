"""Main API module for the Whisper ASR."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .predict import predict

router = APIRouter()


class Message(BaseModel):  # noqa: D101
	role: str
	content: str


class Dialog(BaseModel):  # noqa: D101
	messages: list[Message]


@router.post("/chat")
def respond_to_dialog(dialog: Dialog) -> str:
	"""Process a dialog and generate a response.

	Args:
		dialog (Dialog): An instance of the Dialog class containing the
		conversation messages.

	Returns:
		str: The predicted response based on the dialog messages.

	Raises:
		HTTPException: If an error occurs during processing, an HTTPException is
		raised with status code 500 and the error details.
	"""
	try:
		# convert dialog to python dict
		messages = dialog.model_dump()["messages"]
		return predict(messages)
	except Exception as e:  # noqa: BLE001
		raise HTTPException(status_code=500, detail=str(e))  # noqa: B904
