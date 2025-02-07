"""Module to interact with the Claude model using the anthropic API."""

from os import environ

import anthropic

ANTHROPIC_API_KEY = environ["ANTHROPIC_API_KEY"]

client = anthropic.Anthropic(
	api_key=ANTHROPIC_API_KEY,
)

DEFAUTL_PROMPT = "انا كندوي بالدارجة و بغيت تبقى تجاوبني بها و بغيتك تبقى تجاوبني بلا حروف لاتينية و بلا ارقام:\n"  # noqa: E501


def predict(messages: list, prompt: str | None = None) -> str:
	"""Respond to messages using the Claude model.

	Args:
		messages (list): A list of message dictionaries.
		prompt (str, optional): The prompt to use for the Claude model.

	Returns:
		str: The response text from the Claude model.
	"""
	if prompt is None:
		prompt = DEFAUTL_PROMPT
	messages[0]["content"] = prompt + messages[0]["content"]
	message = client.messages.create(
		model="claude-3-5-sonnet-20241022",
		max_tokens=512,
		messages=messages,
	)
	text = message.content[0].text
	# replace duplicate "\n" with single "\n"
	text = "\n".join(line for line in text.split("\n") if line.strip())
	# replace duplicate '"' with single '"'
	text = '"'.join(line for line in text.split('"') if line.strip())
	return text  # noqa: RET504
