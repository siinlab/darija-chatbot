import logging  # noqa: D100
import os
import re

import audiosegment  # type: ignore  # noqa: PGH003
import requests
from pytubefix import Playlist, YouTube  # type: ignore  # noqa: PGH003
from tqdm import tqdm  # type: ignore  # noqa: PGH003


class AudioDownloader:  # noqa: D101
	def __init__(self, output_dir="raw-data") -> None:  # noqa: ANN001, D107
		self.output_dir = output_dir
		self.setup_logging()
		self.create_output_directory()

	def setup_logging(self) -> None:
		"""Setup logging configuration."""
		logging.basicConfig(
			level=logging.DEBUG,
			format="%(asctime)s - %(levelname)s - %(message)s",
			handlers=[
				logging.FileHandler("audio_downloader.log"),
				logging.StreamHandler(),
			],
		)
		logging.info("Logger initialized.")

	def create_output_directory(self) -> None:
		"""Create the output directory if it doesn't exist."""
		if not os.path.exists(self.output_dir):  # noqa: PTH110
			os.makedirs(self.output_dir)  # noqa: PTH103
			logging.info(f"Created directory: {self.output_dir}")  # noqa: G004

	def download_video_audios(self, video_ids):  # noqa: ANN001, ANN201
		"""Download audio from a list of video IDs."""
		logging.info(f"Downloading audio from {len(video_ids)} videos.")  # noqa: G004
		logging.info(f"Saving audio in {self.output_dir}")  # noqa: G004

		audio_paths = []

		for video_id in tqdm(video_ids):
			if video_id:
				try:
					# if mp3 file exists, skip
					if os.path.exists(os.path.join(self.output_dir, f"{video_id}.mp3")):  # noqa: PTH110, PTH118
						logging.info(
							"Skipping video %s as it already exists.",
							video_id,
						)
						continue
					video_url = f"https://www.youtube.com/watch?v={video_id}"
					yt = YouTube(video_url)
					video = yt.streams.filter(only_audio=True).first()

					if not video:
						logging.warning(f"No audio stream found for video: {video_id}")  # noqa: G004
						continue

					out_file = video.download(output_path=self.output_dir)

					# Convert to mp3 format
					audio = audiosegment.from_file(path=out_file)
					new_file = os.path.join(self.output_dir, f"{video_id}.mp3")  # noqa: PTH118
					audio.export(new_file, format="mp3")
					audio_paths.append(new_file)

					os.remove(out_file)  # noqa: PTH107
				except Exception as e:
					logging.exception(f"Error downloading {video_id}: {e}")  # noqa: G004, TRY401

		logging.info("Audio download completed.")
		return audio_paths

	@staticmethod
	def extract_youtube_video_ids(url_list):  # noqa: ANN001, ANN205
		"""Extract video IDs from a list of YouTube URLs."""
		logging.info(f"Extracting video IDs from {len(url_list)} URLs.")  # noqa: G004
		pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com/[^/]+/|youtu\.be/|youtube\.com/watch\?v=|youtube\.com/v/|youtube\.com/e/|youtube\.com/user/[^/]+#p/[^/]+/|youtube\.com/sports/[^/]+/|youtube\.com/[^/]+/videos/|youtube\.com/feeds/videos.xml\?user=[^&]+&|youtube\.com/playlist\?list=)([^"&?/]+)'
		video_id_list = []
		video_id_pattern = re.compile(pattern=pattern)

		try:
			for url in url_list:
				match = video_id_pattern.search(url)
				if match:
					video_id = match.group(1)
					video_id_list.append(video_id)
			logging.info(f"Extracted {len(video_id_list)} video IDs.")  # noqa: G004
		except Exception as e:
			logging.exception(f"Error extracting video IDs: {e}")  # noqa: G004, TRY401

		return video_id_list

	@staticmethod
	def get_videos_from_playlist(playlist_url):  # noqa: ANN001, ANN205
		"""Retrieve all video URLs from a YouTube playlist."""
		logging.info(f"Getting videos from playlist {playlist_url}.")  # noqa: G004
		try:
			playlist = Playlist(playlist_url)
			logging.info(f"Found {len(playlist)} videos in the playlist.")  # noqa: G004
			return list(playlist.video_urls)
		except Exception as e:
			logging.exception(f"Error retrieving playlist videos: {e}")  # noqa: G004, TRY401
			return []

	@staticmethod
	def get_videos_from_channel(channel_url):  # noqa: ANN001, ANN205
		"""Retrieve video URLs from a YouTube channel."""
		try:
			response = requests.get(channel_url)  # noqa: S113
			if response.status_code == 200:  # noqa: PLR2004
				html_code = response.text
				video_url_strings = re.findall(r'(?<=/watch\?v=)[^&"\s]+', html_code)
				unique_video_url_strings = list(set(video_url_strings))
				logging.info(f"Found {len(unique_video_url_strings)} unique video IDs.")  # noqa: G004
				return [
					f"https://www.youtube.com/watch?v={video_id}"
					for video_id in unique_video_url_strings
				]
			else:  # noqa: RET505
				logging.error(
					f"Failed to retrieve the page. Status code: {response.status_code}",  # noqa: G004
				)
				return []
		except requests.RequestException as e:
			logging.exception(f"Request error: {e}")  # noqa: G004, TRY401
			return []
		except Exception as e:
			logging.exception(f"Unexpected error: {e}")  # noqa: G004, TRY401
			return []


if __name__ == "__main__":
	downloader = AudioDownloader(output_dir="./raw-data")
	playlist_url = (
		"https://www.youtube.com/playlist?list=PLqDxnEgiB7q3oEOy1mVqf6vt137G55eqY"
	)

	video_urls = downloader.get_videos_from_playlist(playlist_url)
	video_ids = downloader.extract_youtube_video_ids(video_urls)
	downloader.download_video_audios(video_ids)
