import pandas as pd


def load_transcripts(file_path: str = "data/transcripts.xlsx"):
    df = pd.read_excel(file_path)
    return df
