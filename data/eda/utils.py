"""This module contains utility functions used in the EDA module."""

import time

from lgg import logger


# Python decorator to measure the execution time of a function and catch exceptions
def exception_decorator(func: callable) -> callable:
	"""Decorator to catch exceptions.

	Args:
		func (callable): The function to be decorated.

	Returns:
		callable: The decorated function.
	"""

	def wrapper(*args: tuple, **kwargs: dict) -> any:
		try:
			return func(*args, **kwargs)
		except Exception as e:  # noqa: BLE001
			logger.warn(f"An error occurred {func.__name__} ({args}): {e}")

	return wrapper


def time_execution(func: callable) -> callable:
	"""Decorator to measure the execution time of a function.

	Args:
		func (callable): The function to be decorated.

	Returns:
		callable: The decorated function
	"""
	def wrapper(*args: tuple, **kwargs: dict) -> any:
		start_time = time.time()
		result = func(*args, **kwargs)
		end_time = time.time()
		logger.debug(
			f"Execution time of {func.__name__}: "
			f"{end_time - start_time:.4f} seconds",
		)
		return result

	return wrapper
