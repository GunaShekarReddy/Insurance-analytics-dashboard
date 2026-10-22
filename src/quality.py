"""Data quality checks for the Data Quality tab. Always runs on the raw dataset."""

import pandas as pd

CATEGORICAL_COLS = ["sex", "smoker", "region"]
NUMERIC_COLS = ["age", "bmi", "children", "charges"]

VARIABLE_TYPES = {
    "age": "Discrete",
    "children": "Discrete",
    "bmi": "Continuous",
    "charges": "Continuous",
    "sex": "Nominal",
    "smoker": "Nominal",
    "region": "Nominal",
}


def null_summary(df: pd.DataFrame) -> pd.Series:
    return df.isnull().sum()


def duplicate_summary(df: pd.DataFrame) -> tuple[int, pd.DataFrame]:
    dup_mask = df.duplicated(keep=False)
    return int(df.duplicated().sum()), df[dup_mask]


def dtype_summary(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "column": df.columns,
            "dtype": [str(dt) for dt in df.dtypes],
            "variable_type": [VARIABLE_TYPES[col] for col in df.columns],
        }
    )


def numeric_profile(df: pd.DataFrame) -> pd.DataFrame:
    return df[NUMERIC_COLS].describe()


def categorical_profile(df: pd.DataFrame) -> dict[str, pd.Series]:
    return {col: df[col].value_counts() for col in CATEGORICAL_COLS}


if __name__ == "__main__":
    from data_loader import load_raw_data, clean_data

    raw = load_raw_data()
    clean = clean_data(raw)

    print("--- Null summary (raw) ---")
    print(null_summary(raw))

    dup_count, dup_rows = duplicate_summary(raw)
    print(f"\n--- Duplicates (raw): {dup_count} ---")
    print(dup_rows)

    print("\n--- Dtype summary (raw) ---")
    print(dtype_summary(raw))

    print("\n--- Numeric profile (clean) ---")
    print(numeric_profile(clean))

    print("\n--- Categorical profile (raw) ---")
    for col, counts in categorical_profile(raw).items():
        print(f"\n{col}:")
        print(counts)
