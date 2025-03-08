# Data preparation

## Introduction

This document will guide you through the process of preparing data for training both the Speech-to-Text and Text-to-Speech models.

Given that not all audio & text pairs available in this project are validated by a professional, it's only fair to assume that some of the data might be noisy or incorrect. Therefore, it's important to clean and validate the data before training the models. As a result, this document will cover the following topics:
1. Exploratory Data Analysis (EDA)
2. Data filtering

## Exploratory Data Analysis (EDA)

Exploratory Data Analysis (EDA) is an approach to analyzing data sets to summarize their main characteristics, often with visual methods. It's a crucial step in the data preparation process as it helps to understand the data better and identify any issues that might need to be addressed before training the models.

### EDA steps

To compute the dataset features, you can run the following command:

```bash
bash scripts/run-eda.sh
```

The script will create a `runs` directory containing several files with the dataset features. Among the features computed are the following:
* Duration of audio files
* Number of characters in the text
* SNR ration
* Percentage of silence in the audio files
  
### Data filtering

Based on the results of the EDA, you can filter the data to remove any noisy or incorrect samples. To filter the data, you can run the following command:

```bash
bash scripts/run-data-filter.sh
```

The script will overwrite all `data.csv` files in the `dataset` directory with the filtered data. The filtering process is based on the criteria defined in the [data/filter/criteria.py](data/filter/criteria.py) file. You can customize the criteria to suit your needs.

## TODO

Among the tasks that need to be done in the future are the following:
* Clean the text data: for eg. replace digits with alphabets, etc.
* Implement a data augmentation pipeline: for eg. changing the speed of the audio, etc.