# Moroccan Darija TTS

## Project Overview

This project includes several components to facilitate the development and usage of a Moroccan Darija TTS system:

### Datasets
The project provides curated datasets necessary for training the TTS models. These datasets include audio recordings and their corresponding transcriptions in Moroccan Darija.

### Trained Models
Pre-trained models are available for immediate use. These models have been trained on the provided datasets and can be used to generate speech from text in Moroccan Darija.

### Finetuning Scripts
For users who wish to improve or adapt the TTS models, finetuning scripts are included. These scripts allow for further training of the models on additional data or specific use cases.

### API
An API is provided to enable easy integration of the TTS system into other applications. This API allows users to input text and receive the generated speech as output.

### UI
A user-friendly interface is available to quickly test the TTS model. This UI allows users to input text and listen to the generated speech, making it easy to evaluate the performance of the TTS system.

## Environment

This repository has a rebuilt Docker image that contains all the necessary dependencies to run the TTS system. To pull the Docker image, use the following command:

```bash
docker pull ghcr.io/siinlab/darija-tts:main
```

The content of the repository is mounted in the `/app` directory of the Docker container. To run the Docker container, use the following command:

```bash
docker run -it ghcr.io/siinlab/darija-tts:main
```

Due to the size of the datasets or pretrained models, they are not included in the Docker image. To download them, use the following command within the Docker container:

```bash
# download datasets & models
dvc pull
# install dependencies for the TTS system
bash models/scripts/setup-tts.sh
bash models/scripts/setup-whisper-asr.sh
```

Once you have downloaded the datasets and models, and set up the dependencies, you can use the trained models through the API and/or UI. Moreover, you can re-train the models on your own dataset using the provided scripts.

### API

To run the API, use the following commands:

```bash
export ANTHROPIC_API_KEY=<your-api-key>
bash API/start_api.sh
```

### UI

After API has been started, you can run the UI using the following command:

```bash
bash UI/start_ui.sh
```

### Finetuning

Currently, this repository provides scripts to finetune the TTS and ASR models.   
To finetune the TTS model, please checkout the files in the [models/tts](models/tts/src) folder.   
To finetune the ASR model, please checkout the files in the [models/whisper_asr](models/whisper_asr/src) folder.


## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. To view a copy of this license, visit [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).


## Disclaimer

This repository is provided for educational and research purposes only. The author(s) and contributors of this project are not responsible for any misuse, unintended consequences, or unethical applications of the code, datasets, or trained models provided herein. 

By using this repository, you agree that:
- You are solely responsible for how you use the materials.
- You will not use the datasets, models, or any derivative works for harmful, illegal, deceptive, or unethical purposes.
- You acknowledge that the maintainers and contributors assume no liability for any direct or indirect damage resulting from the use of this repository.

If you do not agree with these terms, you must refrain from using this repository.
