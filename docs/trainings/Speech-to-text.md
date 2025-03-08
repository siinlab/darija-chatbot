# Training Speech to Text using Whisper

## Introduction

This document will guide you through the process of training a Speech-to-Text model using Whisper. The training will cover the following topics:

0. Data validation
1. Data preparation
2. Model training
3. Model prediction

> You can customize each step by modifying the shell scripts used to execute it.

## Data validation (Optional)

You can validate the data before training the model. Please refer to the [Data validation](../data-validation.md) document for more information.

## Data preparation

To prepare the data for training the Speech-to-Text model, you can run the following command:

```bash
cd models/whisper_asr/src
bash prepate-data.sh
```

## Model training

To train the Speech-to-Text model, you can run the following command:

```bash
cd models/whisper_asr/src
bash train.sh
```

## Model prediction

To transcribe test audios using the trained model, you can run the following command:

```bash
cd models/whisper_asr/checkpoints
cp checkpoint-XXXX/* . # copy the content of the checkpoint directory you want to test to the current directory
cd ../src
bash predict.sh
```