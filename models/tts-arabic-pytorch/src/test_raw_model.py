import argparse  # noqa: D100
import os
import shutil

import torchaudio

from models.fastpitch import FastPitch2Wave

# read ckpt_path using argparse
parser = argparse.ArgumentParser("Test FastPitch2Wave checkpoint")
parser.add_argument("--ckpt_path", type=str, required=True)
parser.add_argument("--use_cuda", action="store_true", default=False)
parser.add_argument("--out_dir", type=str, required=True)
args = parser.parse_args()
ckpt_path = args.ckpt_path
use_cuda = args.use_cuda
out_dir = args.out_dir

# delete out_dir if it exists

shutil.rmtree(out_dir, ignore_errors=True)

# create out_dir
os.makedirs(out_dir, exist_ok=True)  # noqa: PTH103

model = FastPitch2Wave(ckpt_path)
if use_cuda:
    model = model.cuda()

texts = ["السلام عليكم صاحبي",
         "انا البارح مشيت نعس، ولكن مبغاش يديني نعاس",
            "الله يرحم الشهداء",
            "واش نتا مصطي؟",
            "الله يهديك ا صاحبي",  # noqa: RUF001
            "تا ش كتقول؟",
            "واش كتفهم؟",
            "داك الكلاس كيخليك تشوف حياتك فين غادا",
            "الله يخليك لينا",
            "ماشي بزاف",
            "الله يستر",
            "ماشي مشكل",
            "واحد النهار كنت جالس مابيا ماعليا حتى وقف عليا بوليسي",
            "هدا واحد المغربي و الجزائري مشاو لفرنسا ففلوكة",
            "واش فراسك بلي كااع الناس كيتسناو فيك؟",
            "لا لا لا ا صاحبي، ماكاينش هاد القضية. راك مشيتي غالط و بعيد بزاااااف",  # noqa: RUF001
         ]
for i, text in enumerate(texts):
    wave = model.tts(text, speaker_id=0, phonemize=False)
    # save the wave to a file
    wave = wave.unsqueeze(0)  # Add channel dimension if missing
    wav_path = os.path.join(out_dir, f"test-{i}.wav")  # noqa: PTH118
    torchaudio.save(wav_path, wave.cpu(), 22050)
