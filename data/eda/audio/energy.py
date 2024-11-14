"""This module is used to extract energy levels from the audio."""

import librosa
import matplotlib.pyplot as plt
import numpy as np


def extract_energy(audio_path: str) -> np.ndarray:
    """Extract energy levels from the audio."""
    y, sr = librosa.load(audio_path, sr=None)  # Load audio
    return np.array([
        np.sum(np.abs(y[i:i + 512]**2)) for i in range(0, len(y), 512)
    ])

def plot_energy(energy_levels: np.ndarray) -> None:
    """Plot energy levels over time.

    Args:
        energy_levels (np.ndarray): List of energy levels.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(energy_levels, color="green", linewidth=1)
    plt.title("Energy Levels over Time")
    plt.xlabel("Time Frames")
    plt.ylabel("Energy (Amplitude)")
    plt.grid()
    plt.xlim(0, len(energy_levels))
    plt.ylim(0, max(energy_levels) + 5)  # Adjust the y-limit for better visualization
    plt.show()
