"""Major text analysis functions."""

from eda.text.utils import (
	is_alphabet,
	is_arabic_word,
	is_digit,
	is_digit_word,
	is_latin,
	is_latin_word,
	is_punctuation,
	is_punctuation_word,
	is_space,
	is_symbol,
	parallel_distribution,
	parallel_sum,
	split_to_paragraphs,
	split_to_sentences,
	split_to_words,
)
from eda.utils import time_execution

__all__ = [
	"characters_number",
	"white_spaces_number",
	"alphabets_number",
	"punctuations_number",
	"digits_number",
	"symbols_number",
	"words_number",
	"arabic_words_number",
	"latin_words_number",
	"digit_words_number",
	"punctuation_words_number",
	"characters_distribution",
	"words_distribution",
	"words_length_distribution",
	"sentences_length_distribution",
	"paragraphs_length_distribution",
]


@time_execution
def characters_number(text: str) -> int:
	"""Compute the number of characters in a text.

	Args:
		text (str): Text

	Returns:
		int: Number of characters
	"""
	return len(text)


@time_execution
def white_spaces_number(text: str) -> int:
	"""Compute the number of white spaces in a text.

	Args:
		text (str): Text

	Returns:
		int: Number of white spaces
	"""
	return parallel_sum(text, is_space)

@time_execution
def latin_number(text: str) -> int:
	"""Compute the number of latin characters in a text.

	Note:
		Latin characters are a to z characters

	Args:
		text (str): Text

	Returns:
		int: Number of latin characters
	"""
	return parallel_sum(text, is_latin)

@time_execution
def alphabets_number(text: str) -> int:
	"""Compute the number of alphabets in a text.

	Note:
		Alphabets are arabic and latin (a to z) characters

	Args:
		text (str): Text

	Returns:
		int: Number of alphabets
	"""
	return parallel_sum(text, is_alphabet)


@time_execution
def punctuations_number(text: str) -> int:
	"""Compute the number of punctuations in a text.

	Note:
		Punctuations are any characters in `string.punctuation`.

	Args:
		text (str): Text

	Returns:
		int: Number of punctuations
	"""
	return parallel_sum(text, is_punctuation)


@time_execution
def digits_number(text: str) -> int:
	"""Compute the number of digits in a text.

	Args:
		text (str): Text

	Returns:
		int: Number of digits
	"""
	return parallel_sum(text, is_digit)


@time_execution
def symbols_number(text: str) -> int:
	"""Compute the number of symbols in a text.

	Note:
		Symbols are characters that are not alphabets, punctuations or digits.

	Args:
		text (str): Text

	Returns:
		int: Number of symbols
	"""
	return parallel_sum(text, is_symbol)


@time_execution
def words_number(text: str) -> int:
	"""Compute the number of words in a text.

	Note:
		Words are separated by spaces.

	Args:
		text (str): Text

	Returns:
		int: Number of words
	"""
	words = split_to_words(text)
	return len(words)


@time_execution
def arabic_words_number(text: str) -> int:
	"""Compute the number of arabic words in a text.

	Note:
		Arabic words are words that are made up of arabic characters.

	Args:
		text (str): Text

	Returns:
		int: Number of arabic words
	"""
	words = split_to_words(text)
	return parallel_sum(words, is_arabic_word)


@time_execution
def latin_words_number(text: str) -> int:
	"""Compute the number of latin words in a text.

	Note:
		Latin words are words that are made up of latin characters: a to z.

	Args:
		text (str): Text

	Returns:
		int: Number of latin words
	"""
	words = split_to_words(text)
	return parallel_sum(words, is_latin_word)


@time_execution
def digit_words_number(text: str) -> int:
	"""Compute the number of digit words in a text.

	Args:
		text (str): Text

	Returns:
		int: Number of digit words
	"""
	words = split_to_words(text)
	return parallel_sum(words, is_digit_word)


@time_execution
def punctuation_words_number(text: str) -> int:
	"""Compute the number of punctuation words in a text.

	Args:
		text (str): Text

	Returns:
		int: Number of punctuation words
	"""
	words = split_to_words(text)
	return parallel_sum(words, is_punctuation_word)


@time_execution
def characters_distribution(text: str) -> dict[str, int]:
	"""Compute the distribution of characters in a text.

	Note:
		The distribution is sorted in descending order of number of occurences.

	Args:
		text (str): Text

	Returns:
		dict[str, int]: Number of occurrences of each character.
	"""
	return parallel_distribution(text)


@time_execution
def words_distribution(text: str) -> dict[str, int]:
	"""Compute the distribution of words in a text.

	Note:
		The distribution is sorted in descending order of number of occurences.

	Args:
		text (str): Text

	Returns:
		dict[str, int]: Number of occurrences of each unique word.
	"""
	words = split_to_words(text)
	return parallel_distribution(words)


@time_execution
def words_length_distribution(text: str) -> dict[int, int]:
	"""Compute the distribution of words length in a text.

	Note:
		The distribution is sorted in descending order of words length.

	Args:
		text (str): Text

	Returns:
		dict[int, int]: Number of words of each word length value.
	"""
	words = split_to_words(text)
	return parallel_distribution(words, lambda x: len(x))


@time_execution
def sentences_length_distribution(text: str) -> dict[int, int]:
	"""Compute the distribution of sentences length in a text.

	Note:
		- A sentence ends with a period (.)
		- Sentence length refers to the number of characters in the sentence.
		- The distribution is sorted in descending order of sentence length.

	Args:
		text (str): Text

	Returns:
		dict[int, int]: Number of words of each sentence length value.
	"""
	sentences = split_to_sentences(text)
	return parallel_distribution(sentences, lambda x: len(x))


@time_execution
def paragraphs_length_distribution(text: str) -> dict[int, int]:
	r"""Compute the distribution of paragraphs length in a text.

	Note:
		- A paragraph ends with a new line (\n).
		- Paragraph length refers to the number of characters in the sentence.
		- The distribution is sorted in descending order of paragraph length.

	Args:
		text (str): Text

	Returns:
		dict[int, int]: Number of words of each paragraph length value.
	"""
	paragraphs = split_to_paragraphs(text)
	return parallel_distribution(paragraphs, lambda x: len(x))
