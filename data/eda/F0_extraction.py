import numpy as np
import pyworld as pw
import librosa

def extract_pitch(audio_path, sr=16000):
    """Extract the fundamental frequency (F0) from the audio."""
    y, sr = librosa.load(audio_path, sr=sr)

    # Convert to float64
    y = y.astype(np.float64)

    # Perform pitch extraction using WORLD
    f0, time_axis, _ = pw.wav2world(y, sr)  # Adjust unpacking to include the additional return value
    
    return f0

# Example usage
audio_path = 'data/train_data/wav_train/5DxuR1YuhSw-0.2.wav'  # Replace with your audio file path
pitch = extract_pitch(audio_path)
print(f"Extracted Pitch (F0): {pitch}")
import matplotlib.pyplot as plt

def visualize_pitch(f0):
    plt.figure(figsize=(10, 5))
    plt.plot(f0, label='F0 (Fundamental Frequency)', color='blue')
    plt.title('Pitch (F0) over Time')
    plt.xlabel('Time Frames')
    plt.ylabel('Frequency (Hz)')
    plt.grid()
    plt.legend()
    plt.show()

# Visualizing the extracted pitch
visualize_pitch(pitch)
