import sounddevice as sd
from models.fastpitch import FastPitch2Wave
import argparse

def remove_diacrits(text: str): 
    return ''.join([c for c in text if c not in ['َ', 'ِ', 'ُ' , 'ٍ', 'ٌ', 'ْ' , 'ٰ']])


# read ckpt_path using argparse
parser = argparse.ArgumentParser("Test FastPitch2Wave checkpoint")
parser.add_argument("--ckpt_path", type=str, required=True)
args = parser.parse_args()
ckpt_path = args.ckpt_path

model = FastPitch2Wave(ckpt_path)#.cuda()

text = "اَلسَّلامُ عَلَيكُم يَا صَدِيقِي."
text = "أَتَاحَتْ لِلْبَائِعِ المُتَجَوِّلِ أنْ يَكُونَ جَاذِباً لِلمُوَاطِنِ الأقَلِّ دَخْلاً."

wave = model.tts(text, speaker_id=0, phonemize=False)

sd.play(wave, 22050)

text_ = remove_diacrits(text)

wave = model.tts(text_, speaker_id=0, phonemize=False)

sd.play(wave.cpu(), 22050)
