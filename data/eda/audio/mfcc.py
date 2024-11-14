"""Extract Mel-Frequency Cepstral Coefficients (MFCCs) from the audio."""
import librosa
import numpy as np


def extract_mfcc(audio_path: str, sr: int=16000) -> np.ndarray:
    """Extract Mel-Frequency Cepstral Coefficients (MFCCs) from the audio.

    Args:
        audio_path (str): Path to the audio file.
        sr (int): Sampling rate. Defaults to 16000.

    Returns:
        np.ndarray: Extracted MFCCs.
    """
    y, sr = librosa.load(audio_path, sr=sr)
    return librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
