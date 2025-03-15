"""This module contains utility functions used to analyze text data."""

import string
from collections import Counter, OrderedDict
from collections.abc import Callable

from joblib import Parallel, delayed

NUMBER_OF_CONCURRENT_JOBS = 8


def is_punctuation(char: str) -> bool:
	"""Check if a character is a punctuation mark.

	Args:
		char (str): The character to check.

	Returns:
		bool: True if the character is a punctuation mark, False otherwise.
	"""
	return char in string.punctuation


def is_arabic(char: str) -> bool:
	"""Check if a character is an Arabic character.

	Args:
		char (str): The character to check.

	Returns:
		bool: True if the character is an Arabic character, False otherwise.
	"""
	return char in "ابتثجحخدذرزسشصضطظعغفقكلمنهويءآأإة"


def is_latin(char: str) -> bool:
	"""Check if a character is a Latin character.

	Args:
		char (str): The character to check.

	Returns:
		bool: True if the character is a Latin character, False otherwise.
	"""
	return "a" <= char.lower() <= "z"


def is_alphabet(char: str) -> bool:
	"""Check if a character is an alphabet character.

	Args:
		char (str): The character to check.

	Returns:
		bool: True if the character is an alphabet character, False otherwise.
	"""
	return is_arabic(char) or is_latin(char)


def is_arabic_word(word: str) -> bool:
	"""Check if a word consists only of Arabic characters.

	Args:
		word (str): The word to check.

	Returns:
		bool: True if the word consists only of Arabic characters, False otherwise.
	"""
	return all(is_arabic(char) for char in word)


def is_latin_word(word: str) -> bool:
	"""Check if a word consists only of Latin characters.

	Args:
		word (str): The word to check.

	Returns:
		bool: True if the word consists only of Latin characters, False otherwise.
	"""
	return all(is_latin(char) for char in word)


def is_digit_word(word: str) -> bool:
	"""Check if a word consists only of digits.

	Args:
		word (str): The word to check.

	Returns:
		bool: True if the word consists only of digits, False otherwise.
	"""
	return all(is_digit(char) for char in word)


def is_punctuation_word(word: str) -> bool:
	"""Check if a word consists only of punctuation marks.

	Args:
		word (str): The word to check.

	Returns:
		bool: True if the word consists only of punctuation marks, False otherwise.
	"""
	return all(is_punctuation(char) for char in word)


def is_digit(char: str) -> bool:
	"""Check if a character is a digit.

	Args:
		char (str): The character to check.

	Returns:
		bool: True if the character is a digit, False otherwise.
	"""
	return char.isdigit()


def is_space(char: str) -> bool:
	"""Check if a character is a white space.

	Args:
		char (str): The character to check.

	Returns:
		bool: True if the character is a white space, False otherwise.
	"""
	return char.isspace()


def is_symbol(char: str) -> bool:
	"""Check if a character is a symbol.

	A symbol is a character that is not an alphabet character, a digit, or
	a punctuation mark.

	Args:
		char (str): The character to check.

	Returns:
		bool: True if the character is a symbol, False otherwise.
	"""
	return not (
		is_alphabet(char) or is_punctuation(char) or is_digit(char) or is_space(char)
	)


def split_to_words(text: str) -> list[str]:
	"""Split a text into a list of words.

	Args:
		text (str): The text to split.

	Returns:
		list[str]: The list of words.
	"""
	return list(text.split())


def split_to_sentences(text: str) -> list[str]:
	"""Split a text into a list of sentences.

	Args:
		text (str): The text to split.

	Returns:
		list[str]: The list of sentences.
	"""
	return text.split(".")


def split_to_paragraphs(text: str) -> list[str]:
	"""Split a text into a list of paragraphs.

	Args:
		text (str): The text to split.

	Returns:
		list[str]: The list of paragraphs.
	"""
	return text.split("\n")


def parallel_sum(lst: list[any], condition_fn: callable) -> int:
	"""Calculate the sum of elements in a list that satisfy a given condition function.

	Args:
		lst (list[any]): The list of elements.
		condition_fn (callable): The filter function to apply.

	Returns:
		int: The sum of elements that satisfy the filter function.
	"""

	def process_chunk(chunk: list[any]) -> int:
		return sum(1 for x in chunk if condition_fn(x))

	step = len(lst) // NUMBER_OF_CONCURRENT_JOBS
	step = max(1, step)
	chunks = [
		lst[i * step : (i + 1) * step] for i in range(NUMBER_OF_CONCURRENT_JOBS + 1)
	]

	# Compute sub-results
	results = Parallel(n_jobs=8)(delayed(process_chunk)(chunk) for chunk in chunks)

	# Combine the results
	return sum(results)


def parallel_distribution(
	lst: list[any],
	map_fn: Callable | None = None,
) -> OrderedDict:
	"""Calculate the distribution of elements in a list.

	Args:
		lst (list[any]): The list of elements.
		map_fn (callable | None): The mapping function to apply to each element.

	Returns:
		OrderedDict: The distribution of elements.
	"""

	def process_chunk(chunk: list[any]) -> Counter:
		if map_fn is not None:
			chunk = [map_fn(x) for x in chunk]
		return Counter(chunk)

	def aggregate_results(counts: list[Counter]) -> OrderedDict:
		total_count = Counter()
		for count in counts:
			total_count.update(count)
		# sort the result by value in descending order
		return OrderedDict(
			sorted(total_count.items(), key=lambda x: x[1], reverse=True),
		)

	step = len(lst) // NUMBER_OF_CONCURRENT_JOBS
	step = max(1, step)
	chunks = [
		lst[i * step : (i + 1) * step] for i in range(NUMBER_OF_CONCURRENT_JOBS + 1)
	]

	# Compute sub-results
	results = Parallel(n_jobs=8)(delayed(process_chunk)(chunk) for chunk in chunks)

	# Aggregate the results
	return aggregate_results(results)
