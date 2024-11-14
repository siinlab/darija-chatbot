import os
import librosa
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Importing all necessary utility functions
from data.eda.text.utils import (
    is_arabic_word,
    is_latin_word,
    is_digit_word,
    is_punctuation_word,
    # other utility functions as needed
)

# Paths
audio_dir = os.path.join('data', 'train_data', 'wav_train')
captions_file = os.path.join('data', 'train_data', 'training_captions.csv')

# Load the audio files and proceed with the rest of your EDA code...

# Step 1: Load the audio files
audio_files = [f for f in os.listdir(audio_dir) if f.endswith('.wav')]
audio_durations = []
sample_rates = []

for audio_file in audio_files:
    file_path = os.path.join(audio_dir, audio_file)
    audio, sr = librosa.load(file_path, sr=None)  # Load with original sample rate
    audio_durations.append(librosa.get_duration(y=audio, sr=sr))
    sample_rates.append(sr)

# Step 2: Analyze audio data
print(f"Total audio files: {len(audio_files)}")
print(f"Average duration (s): {sum(audio_durations) / len(audio_durations):.2f}")
print(f"Sample rates: {set(sample_rates)}")

# Visualize audio duration distribution
plt.figure(figsize=(12, 6))
plt.hist(audio_durations, bins=30, color='blue', alpha=0.7)
plt.title('Audio Duration Distribution')
plt.xlabel('Duration (seconds)')
plt.ylabel('Frequency')
plt.grid()
plt.show()

# Step 3: Load transcriptions
captions_df = pd.read_csv(captions_file)

# Print the column names to confirm
print("Columns in captions DataFrame:", captions_df.columns)

# Use the correct column name
transcriptions = captions_df['caption'].tolist()  # Accessing the 'caption' column

# Step 4: Analyze transcriptions
n_chars = sum(len(transcription) for transcription in transcriptions)
n_words = sum(len(transcription.split()) for transcription in transcriptions)
n_arabic_words = sum(is_arabic_word(word) for transcription in transcriptions for word in transcription.split())

print(f"Total characters: {n_chars}")
print(f"Total words: {n_words}")
print(f"Total Arabic words: {n_arabic_words}")

# Distribution of words length
word_lengths = [len(word) for transcription in transcriptions for word in transcription.split()]
plt.figure(figsize=(12, 6))
plt.hist(word_lengths, bins=30, color='green', alpha=0.7)
plt.title('Word Length Distribution')
plt.xlabel('Word Length')
plt.ylabel('Frequency')
plt.grid()
plt.show()

# Check for unique words
all_words = [word for transcription in transcriptions for word in transcription.split()]
word_counts = Counter(all_words)
print(f"Number of unique words: {len(word_counts)}")
