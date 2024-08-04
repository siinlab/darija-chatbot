from pytube import Playlist, YouTube
import audiosegment
import os
import re
from tqdm import tqdm
import requests
import logging

class AudioDownloader:
    def __init__(self, output_dir='raw-data'):
        self.output_dir = output_dir
        self.setup_logging()
        self.create_output_directory()

    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("audio_downloader.log"),
                logging.StreamHandler()
            ]
        )
        logging.info("Logger initialized.")

    def create_output_directory(self):
        """Create the output directory if it doesn't exist."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logging.info(f"Created directory: {self.output_dir}")

    def download_video_audios(self, video_ids):
        """Download audio from a list of video IDs."""
        logging.info(f"Downloading audio from {len(video_ids)} videos.")
        logging.info(f"Saving audio in {self.output_dir}")
        
        audio_paths = []

        for video_id in tqdm(video_ids):
            if video_id:
                try:
                    video_url = f'https://www.youtube.com/watch?v={video_id}'
                    yt = YouTube(video_url)
                    video = yt.streams.filter(only_audio=True).first()

                    if not video:
                        logging.warning(f"No audio stream found for video: {video_id}")
                        continue

                    out_file = video.download(output_path=self.output_dir)

                    # Convert to wav format
                    audio = audiosegment.from_file(path=out_file)
                    new_file = os.path.join(self.output_dir, f'{video_id}.wav')
                    audio.export(new_file, format='wav')
                    audio_paths.append(new_file)

                    os.remove(out_file)
                except Exception as e:
                    logging.error(f"Error downloading {video_id}: {e}")

        logging.info("Audio download completed.")
        return audio_paths

    @staticmethod
    def extract_youtube_video_ids(url_list):
        """Extract video IDs from a list of YouTube URLs."""
        logging.info(f"Extracting video IDs from {len(url_list)} URLs.")
        pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com/[^/]+/|youtu\.be/|youtube\.com/watch\?v=|youtube\.com/v/|youtube\.com/e/|youtube\.com/user/[^/]+#p/[^/]+/|youtube\.com/sports/[^/]+/|youtube\.com/[^/]+/videos/|youtube\.com/feeds/videos.xml\?user=[^&]+&|youtube\.com/playlist\?list=)([^"&?/]+)'
        video_id_list = []
        video_id_pattern = re.compile(pattern=pattern)

        try:
            for url in url_list:
                match = video_id_pattern.search(url)
                if match:
                    video_id = match.group(1)
                    video_id_list.append(video_id)
            logging.info(f"Extracted {len(video_id_list)} video IDs.")
        except Exception as e:
            logging.error(f"Error extracting video IDs: {e}")

        return video_id_list

    @staticmethod
    def get_videos_from_playlist(playlist_url):
        """Retrieve all video URLs from a YouTube playlist."""
        logging.info(f"Getting videos from playlist {playlist_url}.")
        try:
            playlist = Playlist(playlist_url)
            logging.info(f"Found {len(playlist)} videos in the playlist.")
            return list(playlist.video_urls)
        except Exception as e:
            logging.error(f"Error retrieving playlist videos: {e}")
            return []

    @staticmethod
    def get_videos_from_channel(channel_url):
        """Retrieve video URLs from a YouTube channel."""
        try:
            response = requests.get(channel_url)
            if response.status_code == 200:
                html_code = response.text
                video_url_strings = re.findall(r'(?<=/watch\?v=)[^&"\s]+', html_code)
                unique_video_url_strings = list(set(video_url_strings))
                logging.info(f"Found {len(unique_video_url_strings)} unique video IDs.")
                video_urls = [f'https://www.youtube.com/watch?v={video_id}' for video_id in unique_video_url_strings]
                return video_urls
            else:
                logging.error(f"Failed to retrieve the page. Status code: {response.status_code}")
                return []
        except requests.RequestException as e:
            logging.error(f"Request error: {e}")
            return []
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return []

if __name__ == '__main__':
    downloader = AudioDownloader(output_dir='./raw-data')
    playlist_url = 'https://www.youtube.com/playlist?list=PLxt59R_fWVzT9bDxA76AHm3ig0Gg9S3So'
    
    video_urls = downloader.get_videos_from_playlist(playlist_url)
    video_ids = downloader.extract_youtube_video_ids(video_urls)
    downloader.download_video_audios(video_ids)
