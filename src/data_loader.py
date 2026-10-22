"""Load and clean the insurance dataset."""

import pandas as pd
import streamlit as st

DEFAULT_DATA_PATH = "data/insurance.csv"


def load_raw_data(path: str = DEFAULT_DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates().reset_index(drop=True)


@st.cache_data
def get_clean_data(path: str = DEFAULT_DATA_PATH) -> pd.DataFrame:
    return clean_data(load_raw_data(path))


if __name__ == "__main__":
    raw = load_raw_data()
    clean = clean_data(raw)
    print(f"Raw rows: {len(raw)}")
    print(f"Clean rows: {len(clean)}")
    print(f"Duplicates dropped: {len(raw) - len(clean)}")
    print(clean.head())
