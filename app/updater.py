import io
import zipfile
import requests
import pandas as pd

ECB_URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip"


def download_ecb_data(output_file):
    response = requests.get(ECB_URL, timeout=30)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
        file_name = zip_file.namelist()[0]

        with zip_file.open(file_name) as csv_file:
            df = pd.read_csv(csv_file)

    df.to_csv(output_file, index=False)

    print(f"ECB data downloaded successfully to {output_file}")