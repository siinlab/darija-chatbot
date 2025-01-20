"""Functions to plot figures."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


class Plotter:
	"""Class for plotting figures."""

	def __init__(self, save_dir: str = ".") -> None:
		"""Initialize the Plotter object.

		Args:
			save_dir (str, optional): The directory to save the figures.
										Defaults to ".".
		"""
		self._figures = Path(save_dir) / "figures"
		self._figures.mkdir(parents=True, exist_ok=True)

	def histogram(
		self,
		hist: dict,
		filename: str,
		*,
		k: int = -1,
		top: bool = True,
		show: bool = False,
	) -> None:
		"""Plot a histogram.

		Args:
			hist (dict): The histogram data.
			filename (str): The filename of the histogram.
			k (int, optional): The number of keys/values to include in the plot.
								Defaults to -1 (all keys/values).
			top (bool, optional): Whether to include the top or bottom keys/values.
								Defaults to True (top).
			show (bool, optional): Whether to display the plot. Defaults to False.
		"""
		keys = list(hist.keys())
		values = list(hist.values())
		if k > 0:
			if top:
				keys = keys[:k]
				values = values[:k]
			else:
				keys = keys[-k:]
				values = values[-k:]

		# replace white spaces in keys with characters
		white_spaces_tokenizer = {" ": "<space>", "\t": "<tab>", "\n": "<newline>"}
		for space, token in white_spaces_tokenizer.items():
			if space in keys:
				index = keys.index(space)
				keys[index] = token

		plt.figure(figsize=(12, 6))
		plt.bar(keys, values)
		plt.xticks(rotation=-45)  # Rotate labels by -45 degrees
		plt.xlabel("Values")
		plt.ylabel("Frequency")
		plt.title("Histogram: " + filename + (" Top" if top else " Bottom") + f" {k}")
		sign = "+" if top else "-"
		plt.savefig(self._figures / f"{filename}{sign}{k}.png")
		if show:
			plt.show()
		plt.close()

	def line_plot(
		self, y: list, filename: str, show: bool = False, x: list = None
	) -> None:
		"""Plot a line plot.

		Args:
			x (list): The x-axis data.
			y (list): The y-axis data.
			filename (str): The filename of the line plot.
			show (bool, optional): Whether to display the plot. Defaults to False.
		"""
		plt.figure(figsize=(12, 6))
		if x is not None:
			plt.plot(x, y)
		else:
			plt.plot(np.arange(len(y)), y)
		plt.xlabel("Index")
		plt.ylabel("Values")
		plt.title("Line Plot: " + filename)
		plt.savefig(self._figures / f"{filename}.png")
		if show:
			plt.show()
		plt.close()

	def box_plot(self, dataframe, filename: str, show: bool = False) -> None:
		"""Plot a box plot.

		Args:
			dataframe (pd.DataFrame): The dataframe containing the data.
			filename (str): The filename of the box plot.
			show (bool, optional): Whether to display the plot. Defaults to False.
		"""
		dataframe.plot(kind="box", subplots=True, layout=(len(dataframe.columns)//3, 4),
                   figsize=(10, 7))
		plt.title("Box Plot: " + filename)
		plt.savefig(self._figures / f"{filename}.png")
		if show:
			plt.show()
		plt.close()
