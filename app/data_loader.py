import pandas as pd

def load_rates(file_path:str) ->pd.DataFrame:
    df = pd.read_csv(file_path)

    df["Date"] = pd.to_datetime(df["Date"])

    return df