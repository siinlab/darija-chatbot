"""This module takes care of creating a config file for the model to be generated.

A similar config file can be found in `tts-arabic-pytorch/configs/nawar_fp_adv_raw.yaml`
"""

import argparse
from pathlib import Path

import yaml
from lgg import logger


def generate_yaml(file_path: str, epochs: int, # noqa: PLR0913
                  n_save_states_iter: int, n_save_backup_iter: int,
                  train_data_path: str, checkpoint_dir: str,
                  restore_model: str,
                  f0_mean: float = 0.0, f0_std: float = 1.0) -> None:
    """Generate a YAML configuration file with the given parameters.

    Args:
        file_path (str): Path to save the YAML file.
        epochs (int): Number of epochs.
        n_save_states_iter (int): Number of iterations to save states.
        n_save_backup_iter (int): Number of iterations to save backups.
        train_data_path (str): Path to the directory containing training dataset.
        checkpoint_dir (str): Path to the directory for saving checkpoints.
        restore_model (str): Path to the model to finetune.
        f0_mean (float): Mean of the F0 values.
        f0_std (float): Standard deviation of the F0 values.

    Returns:
        None
    """
    train_data_path = Path(train_data_path).absolute().resolve()
    restore_model = Path(restore_model).absolute().resolve().as_posix()
    logs_dir = (Path(checkpoint_dir ) / "../logs/") \
            .absolute().resolve().as_posix()
    checkpoint_dir = Path(checkpoint_dir).absolute().resolve().as_posix()
    train_wavs_path = (train_data_path / "audios").as_posix()
    train_labels = (train_data_path / "data.csv").as_posix()
    f0_folder_path = (train_data_path / "audios" / "pitches_penn").as_posix()
    data = {
        "restore_model": restore_model,
        "log_dir": logs_dir,  # for tensorboard
        "checkpoint_dir": checkpoint_dir,
        "train_wavs_path": train_wavs_path,
        "train_labels": train_labels,
        "label_pattern": r'(?P<filename>.*)\,(?P<raw>.*)',
        "f0_folder_path": f0_folder_path,
        "f0_mean": f0_mean,
        "f0_std": f0_std,
        "gan_loss_weight": 3.0,
        "feat_loss_weight": 1.0,
        "max_lengths": [20, 30, 40, 50, 80, 100, 160, 210, 300, 5000],
        "batch_sizes": [32, 32, 32, 32, 16, 16, 10, 8, 6, 4],
        "g_lr": 1.0e-4,
        "g_beta1": 0.0,
        "g_beta2": 0.99,
        "d_lr": 1.0e-4,
        "d_beta1": 0.0,
        "d_beta2": 0.99,
        "n_save_states_iter": n_save_states_iter,
        "n_save_backup_iter": n_save_backup_iter,
        "epochs": epochs,
    }
    with Path(file_path).open("w") as file:
        yaml.dump(data, file, sort_keys=False)

    logger.info(f"YAML file '{file_path}' has been created.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a YAML configuration file.")

    parser.add_argument(
        "--train_data_path",
        type=str,
        help="Path to the directory containing training dataset",
        required=True,
    )
    parser.add_argument(
        "--output_path",
        help="Path to save the YAML file",
        required=True,
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=100,
        help="Number of epochs",
    )
    parser.add_argument(
        "--n_save_states_iter",
        type=int,
        default=100,
        help="Number of iterations to save states",
    )
    parser.add_argument(
        "--n_save_backup_iter",
        type=int,
        default=1000,
        help="Number of iterations to save backups",
    )
    parser.add_argument(
        "--checkpoint_dir",
        type=str,
        default="./checkpoints/",
        help="Path to the directory for saving checkpoints",
    )
    parser.add_argument(
        "--restore_model",
        type=str,
        default="./pretrained/fastpitch_raw_ms.pth",
        help="Path to the model to restore",
    )
    parser.add_argument(
        "--f0_mean",
        type=float,
        required=True,
        help="Mean of the F0 values",
    )
    parser.add_argument(
        "--f0_std",
        type=float,
        required=True,
        help="Standard deviation of the F0 values",
    )

    args = parser.parse_args()

    generate_yaml(
        file_path=args.output_path,
        epochs=args.epochs,
        n_save_states_iter=args.n_save_states_iter,
        n_save_backup_iter=args.n_save_backup_iter,
        train_data_path=args.train_data_path,
        checkpoint_dir=args.checkpoint_dir,
        restore_model=args.restore_model,
        f0_mean=args.f0_mean,
        f0_std=args.f0_std,
    )


