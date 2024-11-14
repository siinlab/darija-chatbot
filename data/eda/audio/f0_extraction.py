"""Extract the fundamental frequency (F0) from an audio file."""
import librosa
import matplotlib.pyplot as plt
import numpy as np
import pyworld as pw


def extract_pitch(audio_path: str, sr: int=16000) -> np.ndarray:
    """Extract the fundamental frequency (F0) from the audio.

    Args:
        audio_path (str): Path to the audio file.
        sr (int): Sampling rate. Defaults to 16000.

    Returns:
        np.ndarray: Extracted pitch (F0) values.
    """
    y, sr = librosa.load(audio_path, sr=sr)

    # Convert to float64
    y = y.astype(np.float64)

    # Perform pitch extraction using WORLD
    f0, *_ = pw.wav2world(y, sr)

    return f0

def plot_pitch(f0: np.ndarray) -> None:
    """Plot the extracted pitch (F0) over time.

    Args:
        f0 (np.ndarray): Extracted pitch values.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(f0, label="F0 (Fundamental Frequency)", color="blue")
    plt.title("Pitch (F0) over Time")
    plt.xlabel("Time Frames")
    plt.ylabel("Frequency (Hz)")
    plt.grid()
    plt.legend()
    plt.show()
