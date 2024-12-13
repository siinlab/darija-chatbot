import argparse

import torchaudio

from models.fastpitch import FastPitch2Wave


# read ckpt_path using argparse
parser = argparse.ArgumentParser("Test FastPitch2Wave checkpoint")
parser.add_argument("--ckpt_path", type=str, required=True)
args = parser.parse_args()
ckpt_path = args.ckpt_path

model = FastPitch2Wave(ckpt_path)#.cuda()

text = "السلام عليكم صاحبي"

wave = model.tts(text, speaker_id=0, phonemize=False)

# save the wave to a file
wave = wave.unsqueeze(0)  # Add channel dimension if missing

torchaudio.save("test.wav", wave.cpu(), 22050)
