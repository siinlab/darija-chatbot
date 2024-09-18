## How to use

This folder contains Python scripts useful for exploratory data analysis (EDA) of the dataset. The scripts are written in Python and use the libraries mentioned in the `requirements.txt` file. To install the required libraries, run the following command:

```bash
pip install -r requirements.txt
```

To use run the scripts, run the following command:

```bash
python eda/cli.py --data <dataset path> --run-dir <directory to save the results>
```
- `<dataset path>`: Path to the dataset folder where a CSV file is stored.
- `<directory to save the results>`: Directory to save the results of the EDA. By default the results are saved in the present working directory.