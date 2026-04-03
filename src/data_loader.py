from __future__ import annotations

import subprocess
from pathlib import Path
import zipfile

import pandas as pd


def load_online_retail_data() -> pd.DataFrame:
    dataset_dir = Path("data/raw")
    zip_path = dataset_dir / "online-retail-dataset.zip"
    csv_path = dataset_dir / "online_retail.csv"

    # create folder if not exists
    dataset_dir.mkdir(parents=True, exist_ok=True)

    # download dataset if not exists
    if not zip_path.exists():
        print("Downloading dataset from Kaggle...")
        subprocess.run([
            "kaggle", "datasets", "download",
            "-d", "ulrikthygepedersen/online-retail-dataset",
            "-p", str(dataset_dir),
            "--force"
        ], check=True)

    # extract only if csv not exists
    if not csv_path.exists():
        print("Extracting dataset...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(dataset_dir)

    # load csv
    print("Loading dataset...")
    df = pd.read_csv(csv_path)

    return df


if __name__ == "__main__":
    df = load_online_retail_data()
    print(df.head())