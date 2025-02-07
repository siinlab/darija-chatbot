"""Module to interact with the Claude model using the anthropic API."""

from os import environ

import anthropic

ANTHROPIC_API_KEY = environ["ANTHROPIC_API_KEY"]

client = anthropic.Anthropic(
	api_key=ANTHROPIC_API_KEY,
)

DEFAUTL_PROMPT = "انا كندوي بالدارجة و بغيت تبقى تجاوبني بها و بغيتك تبقى تجاوبني بلا حروف لاتينية و بلا ارقام:\n"  # noqa: E501


def predict(messages: list, prompt: str = DEFAUTL_PROMPT) -> str:
	"""Respond to messages using the Claude model.

	Args:
		messages (list): A list of message dictionaries.
		prompt (str, optional): The prompt to use for the Claude model.

	Returns:
		str: The response text from the Claude model.
	"""
	messages[0]["content"] = prompt + messages[0]["content"]
	message = client.messages.create(
		model="claude-3-5-sonnet-20241022",
		max_tokens=512,
		messages=messages,
	)
	return message.content[0].text
