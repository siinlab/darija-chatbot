import string
from collections import Counter, OrderedDict
from collections.abc import Callable
from typing import Optional
from joblib import Parallel, delayed

NUMBER_OF_CONCURRENT_JOBS = 8

def is_punctuation(char: str) -> bool:
    return char in string.punctuation

def is_arabic(char: str) -> bool:
    return char in "ابتثجحخدذرزسشصضطظعغفقكلمنهويءآأإة"

def is_latin(char: str) -> bool:
    return "a" <= char.lower() <= "z"

def is_digit(char: str) -> bool:
    return char.isdigit()

def is_alphabet(char: str) -> bool:
    return is_arabic(char) or is_latin(char)

def is_arabic_word(word: str) -> bool:
    return all(is_arabic(char) for char in word)

def is_latin_word(word: str) -> bool:
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

def is_space(char: str) -> bool:
    return char.isspace()

def is_symbol(char: str) -> bool:
    return not (is_alphabet(char) or is_punctuation(char) or is_digit(char) or is_space(char))

def split_to_words(text: str) -> list[str]:
    return list(text.split())

def split_to_sentences(text: str) -> list[str]:
    return text.split(".")

def split_to_paragraphs(text: str) -> list[str]:
    return text.split("\n")

def parallel_sum(lst: list[any], condition_fn: callable) -> int:
    def process_chunk(chunk: list[any]) -> int:
        return sum(1 for x in chunk if condition_fn(x))

    step = len(lst) // NUMBER_OF_CONCURRENT_JOBS
    step = max(1, step)
    chunks = [lst[i * step:(i + 1) * step] for i in range(NUMBER_OF_CONCURRENT_JOBS + 1)]

    results = Parallel(n_jobs=-1)(delayed(process_chunk)(chunk) for chunk in chunks)
    return sum(results)

def parallel_distribution(lst: list[any], map_fn: Optional[Callable] = None) -> OrderedDict:
    def process_chunk(chunk: list[any]) -> Counter:
        if map_fn is not None:
            chunk = [map_fn(x) for x in chunk]
        return Counter(chunk)

    def aggregate_results(counts: list[Counter]) -> OrderedDict:
        total_count = Counter()
        for count in counts:
            total_count.update(count)
        return OrderedDict(sorted(total_count.items(), key=lambda x: x[1], reverse=True))

    step = len(lst) // NUMBER_OF_CONCURRENT_JOBS
    step = max(1, step)
    chunks = [lst[i * step:(i + 1) * step] for i in range(NUMBER_OF_CONCURRENT_JOBS + 1)]

    results = Parallel(n_jobs=-1)(delayed(process_chunk)(chunk) for chunk in chunks)
    return aggregate_results(results)
