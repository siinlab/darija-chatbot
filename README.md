# 🎙️ Moroccan Darija TTS Project: EDA Overview

This README gives an overview of the EDA done for the Moroccan Darija TTS project. It covers the main features of the dataset, including audio and text details, along with key sound features needed to train the TTS model.

## Setup environment

1. Clone the repository
2. Install [DVC](https://dvc.org/doc/install) and set it up.
3. Optionally, request the storage credentials from the project owner, set the storage credentials using this command: `dvc remote modify --local bunny password <api-key>` and pull the data using `dvc pull`.
4. Ensure that you're using Python 3.10 or later.
5. Install the required packages using `pip install -r requirements.txt`.

## EDA

> You can find an available EDA report of the datasets in the [eda.md](docs/eda.md) file.

To run the EDA (assuming you have pulled the datasets from the CDN using DVC), use the following command
```bash
bash scripts/run-eda.sh
```

This script will compute the EDA metrics and save them in the `runs/eda` directory.


## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. To view a copy of this license, visit [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).
