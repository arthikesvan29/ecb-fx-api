import io
import zipfile
from pathlib import Path

import pandas as pd
import requests


ECB_URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip"

DATA_FILE = Path("data/ecb_rates.csv")


def update_ecb_data():
    response = requests.get(ECB_URL, timeout=30)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
        csv_file = zip_file.namelist()[0]

        with zip_file.open(csv_file) as file:
            df = pd.read_csv(file)

    DATA_FILE.parent.mkdir(exist_ok=True)

    df.to_csv(DATA_FILE, index=False)

    print("ECB data updated successfully.")


if __name__ == "__main__":
    update_ecb_data()