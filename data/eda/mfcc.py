import os
import librosa
import numpy as np

def extract_mfcc(audio_path, sr=16000):
    """Extract Mel-Frequency Cepstral Coefficients (MFCCs) from the audio."""
    y, sr = librosa.load(audio_path, sr=sr)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return mfccs

# Directory containing the audio files
audio_dir = 'data/train_data/wav_train'

# Initialize a list to store extracted MFCC features
mfcc_features = []

# Iterate over all .wav files in the directory
for audio_file in os.listdir(audio_dir):
    if audio_file.endswith('.wav'):
        audio_path = os.path.join(audio_dir, audio_file)

        # Extract features
        mfccs = extract_mfcc(audio_path)

        # Append the features to the list
        mfcc_features.append(mfccs)

# Print the shape of MFCC features for each file
for idx, mfcc in enumerate(mfcc_features):
    print(f"MFCCs for {os.listdir(audio_dir)[idx]}: shape {mfcc.shape}")

# Save features to a text file
with open('mfcc_features.txt', 'w') as f:
    for idx, mfcc in enumerate(mfcc_features):
        f.write(f"MFCCs for {os.listdir(audio_dir)[idx]}:\n")
        np.savetxt(f, mfcc, fmt='%.6f')  # Save the MFCC array with 6 decimal places
        f.write("\n")  # Add a newline for separation

print("MFCC features saved successfully in 'mfcc_features.txt'.")
