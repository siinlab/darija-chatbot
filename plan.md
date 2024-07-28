
### Dataset theory (Suggestion)


#### 1. Update Exploratory Data Analysis (EDA)
- Enhance the EDA to provide more insightful information about the dataset.
- Verify the quality of different versions of the dataset.
- Concentrate on the presence of phonemes in the sample (the more balanced representaion the better). 
- Compare the size of the vocabulary to larger datasets, such as speech-to-text datasets.

#### 2. Audio Quality Enhancement
![audio quality enhancement](https://github.com/siinlab/darija-tts/blob/develop/images/audio_cleaning.png)
- Utilize the Auphonic API to enhance the audio quality of the dataset.
- Use Librosa to split audios or extract features for the dataset EDA. 

#### 3. Darija Vocalization and Diacritization Dataset
- Collect and annotate a Darija vocalization and diacritization dataset.
- Train a model based on Shakkelha, developed for Arabic text diacritization.
- Consider making a custom model suitable for darija if Shakkelha didn't work well.

#### 4. Customized Buckwalter Transliteration
![audio quality enhancement](https://github.com/siinlab/darija-tts/blob/develop/images/buckwalter.png)
- Add the diacritization to the dataset for better phonetic representation (using buckwalter).
- Add new alphabets to the Buckwalter transliteration for better orthographic and phonetic representation of Arabic Darija.
  - Include the letter ڴ
  - Include the letter پ
  - Include the letter ڤ

#### 5. Update the Processing Pipeline
- Enhance the audio cleaning pipeline.
- Integrate the diacritization model into the pipeline.
- Incorporate the modified Buckwalter script to generate the phonetic representation of the captions.

### Repository Structure

```
Darija-TTS/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   └── workflows/
├── data/
│   ├── raw/
│   └── processed/
└── images/
├── models/
│   ├── checkpoints/
│   └── scripts/
├── theories/
│   └── dataset_theory.md
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── .gitignore
└── DATA.md

```


# NOTE
This file is to be removed once we set up things.
