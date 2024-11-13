import numpy as np
import librosa

def extract_energy(audio_path):
    """Extract energy levels from the audio."""
    y, sr = librosa.load(audio_path, sr=None)  # Load audio
    energy = np.array([
        np.sum(np.abs(y[i:i + 512]**2)) for i in range(0, len(y), 512)
    ])
    return energy

# Example usage
audio_path = 'data/train_data/wav_train/5DxuR1YuhSw-0.2.wav'  # Replace with your audio file path
energy_levels = extract_energy(audio_path)
print(f"Extracted Energy Levels: {energy_levels}")
import matplotlib.pyplot as plt

# Example extracted energy levels (replace this with your actual extracted values)
energy_levels = [
    2.34254301e-02, 9.13245231e-02, 4.08935905e-01, 3.93776965e+00,
    9.14027786e+00, 9.94422722e+00, 1.15286617e+01, 1.61894531e+01,
    # ... (more values)
]

# Plotting the energy levels
plt.figure(figsize=(12, 6))
plt.plot(energy_levels, color='green', linewidth=1)
plt.title('Energy Levels over Time')
plt.xlabel('Time Frames')
plt.ylabel('Energy (Amplitude)')
plt.grid()
plt.xlim(0, len(energy_levels))
plt.ylim(0, max(energy_levels) + 5)  # Adjust the y-limit for better visualization
plt.show()
